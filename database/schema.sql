
-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Divisions Table
CREATE TABLE IF NOT EXISTS divisions (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Unit Types Table
CREATE TABLE IF NOT EXISTS unit_types (
    code TEXT PRIMARY KEY
);

-- CSI Items Table
CREATE TABLE IF NOT EXISTS csi_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    csi_code TEXT NOT NULL UNIQUE,
    division_code TEXT,
    description TEXT NOT NULL,
    unit_code TEXT,
    daily_output REAL,
    man_hours REAL,
    equip_hours REAL,
    crew_structure TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (division_code) REFERENCES divisions(code),
    FOREIGN KEY (unit_code) REFERENCES unit_types(code)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_csi_items_code ON csi_items(csi_code);
CREATE INDEX IF NOT EXISTS idx_csi_items_division ON csi_items(division_code);
CREATE INDEX IF NOT EXISTS idx_csi_items_description ON csi_items(description);
