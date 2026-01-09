---
description: Daily CSI.xlsm sync check - verify latest updates are published online
---

## Daily Check (Once per day, unless USER asks for more)

When opening the CSI Calculator project, perform the following check:

1. **Compare local CSI.xlsm modification date** with last known sync date
   - Check file: `D:\SUPERMANn\CSI_Project\RSmeansRelated\CSI.xlsm`
   - Compare with GitHub repo: `csi-calculator-backend`

2. **If updates are needed:**
   - Extract data from CSI.xlsm to csi_data.db
   - Commit and push changes to GitHub
   - Notify user that sync is complete

3. **If already synced today:**
   - Skip check and confirm to user: "CSI data is up to date"

## Notes
- This check should be performed once per day automatically
- User can request additional checks manually
- Last sync date should be tracked
