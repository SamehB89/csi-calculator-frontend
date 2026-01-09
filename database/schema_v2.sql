-- Updated Schema for CSI Data Manager V2

DROP TABLE IF EXISTS csi_items;
DROP TABLE IF EXISTS divisions; -- We might not need this separate table if we store hierarchy in items, but let's keep it for fast lookup if needed. Actually, let's simplify and put everything in one big table for the prototype to ensure all data is captured exactly as CSV.

-- Main Items Table
CREATE TABLE csi_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_code TEXT UNIQUE,
    
    -- Hierarchy
    main_div_code TEXT,
    main_div_name TEXT,
    sub_div1_code TEXT,
    sub_div1_name TEXT,
    sub_div2_code TEXT,
    sub_div2_name TEXT,
    
    -- Item Details
    item_code TEXT,
    description TEXT,
    unit TEXT,
    daily_output REAL,
    man_hours REAL,
    equip_hours REAL,
    crew_structure TEXT,
    
    -- Crew Details (1-12)
    crew_num_1 TEXT, crew_desc_1 TEXT,
    crew_num_2 TEXT, crew_desc_2 TEXT,
    crew_num_3 TEXT, crew_desc_3 TEXT,
    crew_num_4 TEXT, crew_desc_4 TEXT,
    crew_num_5 TEXT, crew_desc_5 TEXT,
    crew_num_6 TEXT, crew_desc_6 TEXT,
    crew_num_7 TEXT, crew_desc_7 TEXT,
    crew_num_8 TEXT, crew_desc_8 TEXT,
    crew_num_9 TEXT, crew_desc_9 TEXT,
    crew_num_10 TEXT, crew_desc_10 TEXT,
    crew_num_11 TEXT, crew_desc_11 TEXT,
    crew_num_12 TEXT, crew_desc_12 TEXT
);

CREATE INDEX idx_full_code ON csi_items(full_code);
CREATE INDEX idx_main_div ON csi_items(main_div_code);
CREATE INDEX idx_sub_div1 ON csi_items(sub_div1_code);
CREATE INDEX idx_sub_div2 ON csi_items(sub_div2_code);
