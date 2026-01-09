-- Schema V3: Assemblies for AI Planner

CREATE TABLE IF NOT EXISTS assemblies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_en TEXT NOT NULL,
    name_ar TEXT NOT NULL,
    description TEXT,
    category TEXT -- e.g., "Concrete", "Finishing"
);

CREATE TABLE IF NOT EXISTS assembly_components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assembly_id INTEGER NOT NULL,
    csi_full_code TEXT NOT NULL, -- Links to csi_items.full_code
    ratio_to_primary REAL NOT NULL, -- e.g., 12.0 (m2 per m3)
    ratio_type TEXT NOT NULL, -- 'area', 'volume', 'weight', 'count'
    component_role_en TEXT, -- e.g., "Formwork", "Rebar"
    component_role_ar TEXT,
    FOREIGN KEY (assembly_id) REFERENCES assemblies (id)
);

-- Seed Data: Independent Footings (Standard Example)
INSERT INTO assemblies (name_en, name_ar, description, category) 
VALUES ('Reinforced Concrete Footings', 'قواعد مسلحة منفصلة', 'Complete activity set for RC Footings including forms, steel, and pouring', 'Concrete');

-- Note: We will populate components programmatically or via SQL after ensuring CSI codes exist
