# -*- coding: utf-8 -*-
"""
CSI-Based Relevance Reranker
Specialized retrieval & ranking for construction-spec database following CSI MasterFormat (16 Divisions).

Scoring Formula:
Score = 0.35*CodeMatch + 0.30*SemanticSim + 0.15*TitleMatch + 0.10*FieldMatch + 0.10*UnitMatch
"""

import os
import re
import json
from typing import List, Dict, Any, Optional, Tuple
from difflib import SequenceMatcher

# Path to CSI Excel file
CSI_EXCEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "CSI.xlsm")

# Synonym mappings for normalization
SYNONYMS = {
    # Footings
    "isolated footing": ["pad footing", "spread footing", "قواعد منفصلة", "قاعدة منفصلة"],
    "strip footing": ["continuous footing", "wall footing", "قواعد شريطية", "قاعدة شريطية"],
    "raft foundation": ["mat foundation", "لبشة", "حصيرة"],
    
    # Columns
    "column": ["عمود", "أعمدة", "كولون"],
    "round column": ["circular column", "عمود دائري"],
    
    # Beams
    "beam": ["كمرة", "كمرات", "بيم"],
    "grade beam": ["tie beam", "سمل", "ميدة"],
    
    # Slabs
    "slab": ["بلاطة", "سقف", "سلاب"],
    "flat slab": ["فلات سلاب", "سقف مسطح"],
    
    # Work stages
    "formwork": ["forms", "shuttering", "شدة", "نجارة"],
    "reinforcement": ["rebar", "تسليح", "حدادة"],
    "casting": ["concrete", "pouring", "صب", "خرسانة"],
    
    # Plastering
    "plaster": ["plastering", "render", "محارة", "لياسة", "بياض"],
    "cement plaster": ["محارة اسمنتية"],
    "gypsum plaster": ["محارة جبسية"],
}

# Unit compatibility mapping
UNIT_COMPATIBILITY = {
    "SQM": ["M2", "SF", "SQ.M", "م²", "متر مربع"],
    "CUM": ["M3", "CY", "CU.M", "م³", "متر مكعب"],
    "LM": ["M", "LF", "م.ط", "متر طولي"],
    "EA": ["EACH", "NO", "عدد"],
    "MET. TON": ["TON", "MT", "طن"],
}


def normalize_text(text: str) -> str:
    """Normalize text: lowercase, remove diacritics, trim punctuation."""
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove Arabic diacritics
    arabic_diacritics = re.compile(r'[\u064B-\u065F\u0670]')
    text = arabic_diacritics.sub('', text)
    
    # Remove extra punctuation and whitespace
    text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def expand_synonyms(query: str) -> List[str]:
    """Expand query with synonyms."""
    query_lower = query.lower()
    tokens = [query_lower]
    
    for main_term, synonyms in SYNONYMS.items():
        if main_term in query_lower:
            tokens.extend(synonyms)
        for syn in synonyms:
            if syn in query_lower:
                tokens.append(main_term)
                tokens.extend([s for s in synonyms if s != syn])
    
    return list(set(tokens))


def calculate_code_match(query: str, csi_code: str, division: str) -> Tuple[float, str]:
    """
    Calculate CodeMatch score.
    Returns: (score, match_type)
    - 1.0 = exact code match
    - 0.7 = same division
    - 0.0 = no match
    """
    if not csi_code:
        return 0.0, "none"
    
    query_normalized = normalize_text(query)
    code_normalized = normalize_text(csi_code)
    
    # Check for exact code match
    if code_normalized in query_normalized or query_normalized in code_normalized:
        return 1.0, "exact"
    
    # Check for division match (first 2 digits)
    query_div = re.search(r'\b(\d{2})\b', query_normalized)
    code_div = re.search(r'^(\d{2,3})', code_normalized)
    
    if query_div and code_div:
        if query_div.group(1) == code_div.group(1)[:2]:
            return 0.7, "same_division"
    
    return 0.0, "none"


def calculate_title_match(query: str, title: str) -> Tuple[float, List[str]]:
    """
    Calculate TitleMatch score.
    Returns: (score, matched_tokens)
    """
    if not title:
        return 0.0, []
    
    query_tokens = set(normalize_text(query).split())
    title_tokens = set(normalize_text(title).split())
    
    # Expand with synonyms
    expanded_query = set()
    for token in query_tokens:
        expanded_query.add(token)
        for main_term, synonyms in SYNONYMS.items():
            if token in main_term.split() or any(token in s.split() for s in synonyms):
                expanded_query.update(main_term.split())
                for syn in synonyms:
                    expanded_query.update(syn.split())
    
    matched = expanded_query.intersection(title_tokens)
    
    if not query_tokens:
        return 0.0, []
    
    score = len(matched) / len(query_tokens)
    return min(score, 1.0), list(matched)


def calculate_unit_match(query_unit: Optional[str], item_unit: str) -> float:
    """
    Calculate UnitMatch score.
    - 1.0 = exact match
    - 0.5 = compatible
    - 0.0 = no match
    """
    if not query_unit or not item_unit:
        return 0.5  # Neutral if not specified
    
    query_unit_upper = query_unit.upper()
    item_unit_upper = item_unit.upper()
    
    # Exact match
    if query_unit_upper == item_unit_upper:
        return 1.0
    
    # Check compatibility
    for main_unit, compatible in UNIT_COMPATIBILITY.items():
        all_units = [main_unit] + compatible
        all_units_upper = [u.upper() for u in all_units]
        
        if query_unit_upper in all_units_upper and item_unit_upper in all_units_upper:
            return 0.5
    
    return 0.0


def calculate_field_match(query: str, item: Dict[str, Any]) -> Tuple[float, List[str]]:
    """
    Calculate FieldMatch score based on metadata fields.
    Returns: (score, matched_fields)
    """
    matched_fields = []
    total_checks = 0
    matches = 0
    
    query_lower = query.lower()
    
    # Check unit in query
    if item.get('Unit'):
        total_checks += 1
        unit_upper = item['Unit'].upper()
        if unit_upper.lower() in query_lower or any(u.lower() in query_lower for u in UNIT_COMPATIBILITY.get(unit_upper, [])):
            matches += 1
            matched_fields.append(f"Unit:{item['Unit']}")
    
    # Check crew structure
    if item.get('Crew_Structure'):
        crew_lower = item['Crew_Structure'].lower()
        crew_keywords = ['carpenter', 'laborer', 'foreman', 'rodman', 'نجار', 'حداد', 'عامل']
        for kw in crew_keywords:
            if kw in query_lower and kw in crew_lower:
                matches += 1
                matched_fields.append(f"Crew:{kw}")
                break
        total_checks += 1
    
    if total_checks == 0:
        return 0.5, []  # Neutral
    
    return matches / total_checks, matched_fields


def calculate_score(
    query: str,
    item: Dict[str, Any],
    query_unit: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate weighted relevance score for a candidate item.
    
    Score = 0.35*CodeMatch + 0.30*SemanticSim + 0.15*TitleMatch + 0.10*FieldMatch + 0.10*UnitMatch
    """
    # CodeMatch (35%)
    code_score, code_match_type = calculate_code_match(
        query, 
        item.get('CSI_Code', item.get('full_code', '')),
        item.get('Division', '')
    )
    
    # SemanticSim (30%) - use provided or calculate basic similarity
    semantic_score = item.get('embedding_similarity', 0.0)
    if semantic_score == 0:
        # Fallback: basic string similarity
        title = item.get('Title', item.get('description', ''))
        semantic_score = SequenceMatcher(None, normalize_text(query), normalize_text(title)).ratio()
    
    # TitleMatch (15%)
    title = item.get('Title', item.get('description', ''))
    title_score, matched_tokens = calculate_title_match(query, title)
    
    # FieldMatch (10%)
    field_score, field_matches = calculate_field_match(query, item)
    
    # UnitMatch (10%)
    unit_score = calculate_unit_match(query_unit, item.get('Unit', item.get('unit', '')))
    
    # Weighted total
    total_score = (
        0.35 * code_score +
        0.30 * semantic_score +
        0.15 * title_score +
        0.10 * field_score +
        0.10 * unit_score
    )
    
    return {
        "Score": round(total_score, 4),
        "MatchExplanation": {
            "matched_tokens": matched_tokens,
            "semantic_similarity": round(semantic_score, 4),
            "code_match": code_match_type,
            "field_matches": field_matches,
            "notes": ""
        },
        "component_scores": {
            "code_match": round(code_score, 4),
            "semantic_sim": round(semantic_score, 4),
            "title_match": round(title_score, 4),
            "field_match": round(field_score, 4),
            "unit_match": round(unit_score, 4)
        }
    }


def rerank_candidates(
    query: str,
    candidates: List[Dict[str, Any]],
    top_k: int = 7,
    query_unit: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Rerank candidates based on CSI relevance scoring.
    
    Args:
        query: User query text
        candidates: List of candidate items from initial search
        top_k: Number of top results to return
        query_unit: Optional unit filter
        filters: Optional hard filters (e.g., {"man_hours_lt": 5, "division": "03"})
    
    Returns:
        JSON-compatible dict with results, warnings, suggestions
    """
    # Detect language
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    language = "ar" if arabic_pattern.search(query) else "en"
    
    warnings = []
    suggestions = []
    
    # Check if data source is accessible
    if not os.path.exists(CSI_EXCEL_PATH):
        return {
            "query": query,
            "language": language,
            "top_k": 0,
            "results": [],
            "warnings": [f"Data source CSI.xlsm not accessible at {CSI_EXCEL_PATH}. Ensure file exists."],
            "suggestions": [],
            "data_source_missing": True
        }
    
    # Apply hard filters
    filtered_candidates = candidates
    if filters:
        original_count = len(filtered_candidates)
        
        if "division" in filters:
            filtered_candidates = [c for c in filtered_candidates 
                                   if filters["division"] in str(c.get('Division', c.get('main_div_code', '')))]
        
        if "man_hours_lt" in filters:
            threshold = filters["man_hours_lt"]
            filtered_candidates = [c for c in filtered_candidates 
                                   if c.get('ManHours_file', c.get('man_hours', 999)) < threshold]
            
            # Relaxation rules if no results
            if not filtered_candidates and candidates:
                # Try 1.25x
                threshold_125 = threshold * 1.25
                filtered_candidates = [c for c in candidates 
                                       if c.get('ManHours_file', c.get('man_hours', 999)) < threshold_125]
                if filtered_candidates:
                    warnings.append(f"Relaxed man_hours filter from {threshold} to {threshold_125}")
                else:
                    # Try 1.5x
                    threshold_150 = threshold * 1.5
                    filtered_candidates = [c for c in candidates 
                                           if c.get('ManHours_file', c.get('man_hours', 999)) < threshold_150]
                    if filtered_candidates:
                        warnings.append(f"Relaxed man_hours filter from {threshold} to {threshold_150}")
        
        if len(filtered_candidates) < original_count:
            warnings.append(f"Filtered from {original_count} to {len(filtered_candidates)} candidates")
    
    # Score each candidate
    scored_candidates = []
    for item in filtered_candidates:
        score_result = calculate_score(query, item, query_unit)
        scored_item = {
            **item,
            **score_result
        }
        scored_candidates.append(scored_item)
    
    # Sort by score (descending), with tie-breaking
    def sort_key(item):
        score = item.get('Score', 0)
        code_match = 1 if item.get('MatchExplanation', {}).get('code_match') == 'exact' else 0
        semantic = item.get('MatchExplanation', {}).get('semantic_similarity', 0)
        daily_output = item.get('DailyOutput', item.get('daily_output', 0)) or 0
        return (score, code_match, semantic, daily_output)
    
    scored_candidates.sort(key=sort_key, reverse=True)
    
    # Take top_k
    top_results = scored_candidates[:top_k]
    
    # Format results
    results = []
    for rank, item in enumerate(top_results, 1):
        result = {
            "rank": rank,
            "id": item.get('id', rank),
            "CSI_Code": item.get('CSI_Code', item.get('full_code')),
            "Division": item.get('Division', item.get('main_div_name')),
            "Title": item.get('Title', item.get('description')),
            "Unit": item.get('Unit', item.get('unit')),
            "DailyOutput": item.get('DailyOutput', item.get('daily_output')),
            "ManHours_file": item.get('ManHours_file', item.get('man_hours')),
            "EquipHours_file": item.get('EquipHours_file', item.get('equip_hours')),
            "Crew_Structure": item.get('Crew_Structure', item.get('crew_structure')),
            "Score": item.get('Score', 0),
            "MatchExplanation": item.get('MatchExplanation', {}),
            "source_ref": item.get('source_ref', {"file": "csi_data.db", "sheet": "csi_items"})
        }
        results.append(result)
    
    # Add suggestions for ambiguous queries
    query_tokens = normalize_text(query).split()
    if len(query_tokens) <= 3 and not results:
        suggestions = [
            "Try adding more specific terms (e.g., 'isolated footing reinforcement')",
            "Specify the work stage: formwork, reinforcement, or casting",
            "Include the unit if known (e.g., 'CUM', 'SQM')"
        ]
    
    return {
        "query": query,
        "language": language,
        "top_k": len(results),
        "results": results,
        "warnings": warnings,
        "suggestions": suggestions,
        "data_source_missing": False
    }


def search_and_rerank(query: str, top_n: int = 50, return_top_k: int = 7) -> Dict[str, Any]:
    """
    Complete search and rerank pipeline.
    1. Search database for candidates
    2. Rerank using CSI scoring formula
    3. Return JSON results
    """
    import sqlite3
    
    db_path = os.path.join(os.path.dirname(__file__), "csi_data.db")
    
    if not os.path.exists(db_path):
        return {
            "query": query,
            "language": "en",
            "top_k": 0,
            "results": [],
            "warnings": ["Database not found"],
            "suggestions": [],
            "data_source_missing": True
        }
    
    # Expand query with synonyms
    search_terms = expand_synonyms(query)
    
    # Build search conditions
    conditions = []
    for term in search_terms[:5]:  # Limit to avoid too complex query
        conditions.append(f"description LIKE '%{term}%'")
    
    where_clause = " OR ".join(conditions) if conditions else "1=1"
    
    # Search database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    sql = f"""
        SELECT 
            rowid as id,
            full_code as CSI_Code,
            main_div_name as Division,
            description as Title,
            unit as Unit,
            daily_output as DailyOutput,
            man_hours as ManHours_file,
            equip_hours as EquipHours_file,
            crew_structure as Crew_Structure
        FROM csi_items 
        WHERE {where_clause}
        LIMIT {top_n}
    """
    
    try:
        candidates = [dict(row) for row in conn.execute(sql).fetchall()]
    except Exception as e:
        candidates = []
    finally:
        conn.close()
    
    # Rerank
    return rerank_candidates(query, candidates, top_k=return_top_k)
