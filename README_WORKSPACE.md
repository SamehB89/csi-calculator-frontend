# CSI_Joker Workspace

This is the main workspace for the **CSI Crew Calculator** project.

## 📂 Project Structure

```
CSI_Project/
├── frontend/           # Web application frontend
│   ├── index.html     # Main browse page
│   ├── crew-calculator.html  # Calculator page
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
│
├── backend/           # Flask server
│   └── app.py        # Main API server
│
├── database/         # SQLite database
│   └── csi_data.db   # Main database (auto-generated)
│
├── CSI.xlsm          # Excel source data
│
└── Scripts:
    ├── update_database_from_excel.py
    ├── update_database.bat
    ├── run_server.bat
    └── run_app.bat
```

## 🚀 Quick Start

### 1. Open Workspace

```
File → Open Workspace from File → CSI_Joker.code-workspace
```

### 2. Start Server

```bash
# Method 1: Using batch file
run_server.bat

# Method 2: Manual
cd backend
python app.py
```

### 3. Open Application

```
http://127.0.0.1:5000
```

## 🔄 Update Database

When you modify `CSI.xlsm`:

```bash
# Method 1: Double-click
update_database.bat

# Method 2: Command line
python update_database_from_excel.py
```

## 📝 Important Files

| File | Purpose |
|------|---------|
| `CSI.xlsm` | **Excel source** - Update your data here |
| `database/csi_data.db` | **SQLite database** - Auto-updated from Excel |
| `backend/app.py` | **Flask API** - Backend server |
| `frontend/index.html` | **Browse page** - Main interface |
| `frontend/crew-calculator.html` | **Calculator** - Crew calculator interface |

## 🛠️ Development

### VS Code Features

- ✅ Multi-folder workspace (Frontend, Backend, Database)
- ✅ Python debugging configured
- ✅ Auto-save enabled
- ✅ Git integration
- ✅ Recommended extensions

### Debug Configurations

1. **Python: Flask Server** - Run and debug the backend
2. **Python: Update Database** - Debug the database updater

## 📚 Documentation

- [Calculation Methodology](file:///C:/Users/super/.gemini/antigravity/brain/55154199-234c-4e1f-a446-82ad22c3857e/calculation_methodology.md)
- [Database Update Guide](file:///C:/Users/super/.gemini/antigravity/brain/55154199-234c-4e1f-a446-82ad22c3857e/database_update_guide.md)
- [Project Walkthrough](file:///C:/Users/super/.gemini/antigravity/brain/55154199-234c-4e1f-a446-82ad22c3857e/walkthrough.md)

## 🎯 Workflow

```
1. Update CSI.xlsm
   ↓
2. Run update_database.bat
   ↓
3. Restart Flask server
   ↓
4. Refresh browser
   ↓
5. Done! ✓
```

---

**Workspace Name:** CSI_Joker  
**Project:** CSI Crew Calculator  
**Version:** 1.0  
**Last Updated:** 2025-12-05
