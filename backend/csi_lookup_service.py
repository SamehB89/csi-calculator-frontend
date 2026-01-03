"""
CSI Lookup Service - Intelligent Construction Item Matching
============================================================
Maps user queries (Arabic/English) to CSI construction items using:
- Fuzzy matching (difflib/fuzzywuzzy)
- Synonym matching
- Confidence scoring
"""

import json
import os
from difflib import SequenceMatcher
from typing import List, Dict, Optional, Tuple


class CSILookupService:
    """Service for intelligent CSI item lookup and matching"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize CSI Lookup Service
        
        Args:
            db_path: Path to csi-lookup-database.json
        """
        if db_path is None:
            # Default path relative to backend directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, 'static_files', 'data', 'csi-lookup-database.json')
        
        self.db_path = db_path
        self.database = self._load_database()
        self.items_index = self._build_index()
    
    def _load_database(self) -> Dict:
        """Load CSI database from JSON file"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ CSI database not found at {self.db_path}")
            return {"metadata": {}, "categories": []}
    
    def _build_index(self) -> List[Dict]:
        """Build searchable index from all items"""
        index = []
        for category in self.database.get('categories', []):
            for item in category.get('items', []):
                # Add category info to each item
                item_copy = item.copy()
                item_copy['category_id'] = category['category_id']
                item_copy['category_name_ar'] = category['category_name_ar']
                item_copy['category_name_en'] = category['category_name_en']
                item_copy['csi_division'] = category['csi_division']
                index.append(item_copy)
        return index
    
    def _calculate_similarity(self, query: str, text: str) -> float:
        """
        Calculate similarity score between query and text
        Enhanced version with word-level matching
        
        Args:
            query: Search query
            text: Text to compare against
            
        Returns:
            Similarity score (0-100)
        """
        # Normalize both strings (lowercase, strip)
        q = query.lower().strip()
        t = text.lower().strip()
        
        # Exact match
        if q == t:
            return 100.0
        
        # Substring match (complete word)
        if q in t or t in q:
            return 95.0
        
        # Word-level matching for compound queries
        q_words = q.split()
        t_words = t.split()
        
        # Check if all query words are in text
        if len(q_words) > 1:
            matches = sum(1 for qw in q_words if any(qw in tw or tw in qw for tw in t_words))
            if matches == len(q_words):
                return 92.0
            elif matches > 0:
                word_match_ratio = (matches / len(q_words)) * 85
                return word_match_ratio
        
        # Fuzzy match using SequenceMatcher
        similarity = SequenceMatcher(None, q, t).ratio() * 100
        
        # Boost score if key words match
        if any(word in t for word in q_words if len(word) > 3):
            similarity = min(similarity + 10, 100)
        
        return similarity
    
    def _match_item(self, query: str, item: Dict, lang: str = 'ar') -> float:
        """
        Calculate match score for an item against query
        
        Args:
            query: User search query
            item: CSI item dict
            lang: Language ('ar' or 'en')
            
        Returns:
            Match confidence score (0-100)
        """
        scores = []
        
        # Check item name
        name_key = f'item_name_{lang}'
        if name_key in item:
            scores.append(self._calculate_similarity(query, item[name_key]))
        
        # Check synonyms
        synonym_key = f'synonyms_{lang}'
        if synonym_key in item:
            for synonym in item[synonym_key]:
                scores.append(self._calculate_similarity(query, synonym))
        
        # Return best match score
        return max(scores) if scores else 0.0
    
    def search_item(
        self, 
        query: str, 
        lang: str = 'ar', 
        min_confidence: float = 60.0,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search for CSI items matching the query
        
        Args:
            query: User search query
            lang: Language ('ar' or 'en')
            min_confidence: Minimum confidence score to return
            top_k: Number of top results to return
            
        Returns:
            List of matched items with confidence scores
        """
        results = []
        
        for item in self.items_index:
            confidence = self._match_item(query, item, lang)
            
            if confidence >= min_confidence:
                result = item.copy()
                result['match_confidence'] = round(confidence, 2)
                results.append(result)
        
        # Sort by confidence (descending)
        results.sort(key=lambda x: x['match_confidence'], reverse=True)
        
        # Return top K results
        return results[:top_k]
    
    def get_item_by_key(self, item_key: str) -> Optional[Dict]:
        """
        Get item by its unique key
        
        Args:
            item_key: Item key (e.g., 'CONC_FOOT_ISO_PLAIN')
            
        Returns:
            Item dict or None if not found
        """
        for item in self.items_index:
            if item['item_key'] == item_key:
                return item.copy()
        return None
    
    def get_category(self, category_id: str) -> Optional[Dict]:
        """
        Get category by ID
        
        Args:
            category_id: Category ID (e.g., 'CONC', 'EARTH')
            
        Returns:
            Category dict or None
        """
        for category in self.database.get('categories', []):
            if category['category_id'] == category_id:
                return category.copy()
        return None
    
    def get_all_categories(self) -> List[Dict]:
        """Get all categories"""
        return self.database.get('categories', [])
    
    def extract_construction_terms(self, query: str, lang: str = 'ar') -> Tuple[str, Optional[float]]:
        """
        Extract construction item and quantity from natural language query
        
        Examples:
            "لبشة 100 متر مكعب" -> ("لبشة", 100.0)
            "raft foundation 50 m3" -> ("raft foundation", 50.0)
            "قواعد منفصلة" -> ("قواعد منفصلة", None)
        
        Args:
            query: Natural language query
            lang: Language hint
            
        Returns:
            Tuple of (clean_item_term, quantity)
        """
        import re
        
        # Extract numbers (quantity)
        numbers = re.findall(r'[\d.]+', query)
        quantity = float(numbers[0]) if numbers else None
        
        # Remove numbers and common units from query
        units = ['م³', 'متر مكعب', 'متر', 'm3', 'cubic meters', 'meters', 'm²', 'sqm', 'square']
        clean_query = query
        for unit in units:
            clean_query = clean_query.replace(unit, '')
        
        # Remove numbers
        clean_query = re.sub(r'[\d.]+', '', clean_query).strip()
        
        return clean_query, quantity
    
    def smart_search(
        self,
        query: str,
        lang: str = 'ar',
        min_confidence: float = 60.0
    ) -> Dict:
        """
        Smart search that extracts terms and returns structured results
        
        Args:
            query: Natural language query
            lang: Language ('ar' or 'en')
            min_confidence: Minimum confidence for matches
            
        Returns:
            Dict with 'matches', 'query_quantity', 'clean_query'
        """
        # Extract item term and quantity
        clean_query, quantity = self.extract_construction_terms(query, lang)
        
        # Search for matches
        matches = self.search_item(clean_query, lang, min_confidence, top_k=5)
        
        return {
            'matches': matches,
            'query_quantity': quantity,
            'clean_query': clean_query,
            'original_query': query
        }


# Global instance
_csi_lookup = None

def get_csi_lookup() -> CSILookupService:
    """Get or create global CSI lookup service instance"""
    global _csi_lookup
    if _csi_lookup is None:
        _csi_lookup = CSILookupService()
    return _csi_lookup


if __name__ == '__main__':
    # Test the service
    service = CSILookupService()
    
    print("🔍 Testing CSI Lookup Service\n")
    
    test_queries = [
        ("لبشة 100 متر مكعب", 'ar'),
        ("raft foundation", 'en'),
        ("قواعد منفصلة", 'ar'),
        ("isolated footing 50 m3", 'en'),
        ("محارة", 'ar'),
        ("plaster", 'en'),
    ]
    
    for query, lang in test_queries:
        print(f"\n📝 Query: '{query}' (lang={lang})")
        result = service.smart_search(query, lang, min_confidence=50)
        
        print(f"   Clean: '{result['clean_query']}'")
        if result['query_quantity']:
            print(f"   Quantity: {result['query_quantity']}")
        
        print(f"   Matches: {len(result['matches'])}")
        for i, match in enumerate(result['matches'][:3], 1):
            print(f"      {i}. {match['item_name_ar']} ({match['match_confidence']}%)")
            print(f"         CSI: {match['csi_section']}")
