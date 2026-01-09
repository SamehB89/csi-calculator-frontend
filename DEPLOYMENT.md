# CSI Calculator - Deployment Guide 🚀

## 📍 Production URLs

| Service | URL | Provider |
|---------|-----|----------|
| **Frontend** | https://csi-calculator-frontend.vercel.app | Vercel |
| **Backend API** | https://web-production-90db2.up.railway.app | Railway |
| **Database** | PostgreSQL (Neon.tech) | Neon |

---

## 🏗️ Architecture

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   Users (Browser)   │────▶│   Vercel (Frontend)  │────▶│ Railway (API)   │
│                     │     │   Static HTML/JS/CSS │     │ Flask Backend   │
└─────────────────────┘     └──────────────────────┘     └────────┬────────┘
                                                                   │
                                                                   ▼
                                                         ┌─────────────────┐
                                                         │ Neon PostgreSQL │
                                                         │   Database      │
                                                         └─────────────────┘
```

---

## 🔧 Environment Variables

### Railway (Backend)

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Neon PostgreSQL connection string | ✅ Yes |
| `GEMINI_API_KEY` | Google AI API key for AI Planner | Optional |
| `PORT` | Auto-set by Railway | Auto |

### Vercel (Frontend) 

No environment variables needed - uses `vercel.json` rewrites.

---

## 📁 Key Configuration Files

### Frontend: `vercel.json`
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://web-production-90db2.up.railway.app/api/$1"
    }
  ]
}
```

### Backend: `Procfile`
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### Backend: `db_config.py`
- Connects to PostgreSQL when `DATABASE_URL` is set
- Falls back to SQLite for local development

---

## 🚀 Deployment Steps

### Frontend (Vercel)
1. Push changes to `frontend/` on GitHub
2. Vercel auto-deploys from connected repo
3. No manual steps needed

### Backend (Railway)
1. Push changes to `backend/` on GitHub
2. Railway auto-deploys from connected repo
3. Verify: `curl https://web-production-90db2.up.railway.app/health`

---

## 🧪 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check & DB status |
| `/api/divisions` | GET | List main divisions |
| `/api/subdivisions1` | GET | Sub-divisions (level 1) |
| `/api/subdivisions2` | GET | Sub-divisions (level 2) |
| `/api/items` | GET | Search/list items |
| `/api/item/<code>` | GET | Single item details |
| `/api/calculate-crew` | POST | Calculate crew requirements |
| `/api/ai` | POST | AI Planner (Gemini) |

---

## 💾 Database Backup

### Export from Neon
```bash
pg_dump "postgresql://user:pass@host/db" > backup.sql
```

### Import to Neon
```bash
psql "postgresql://user:pass@host/db" < backup.sql
```

### Local Development (SQLite)
```bash
# Use local csi_data.db file in backend/
python app.py  # Runs on http://localhost:5000
```

---

## 🔍 Troubleshooting

### API Returns Error
1. Check Railway logs: Railway Dashboard → Deployments → Logs
2. Verify `DATABASE_URL` is set correctly
3. Test: `curl https://web-production-90db2.up.railway.app/health`

### Frontend Not Loading Data
1. Check browser DevTools → Network tab
2. Verify Vercel deployment completed
3. Check `vercel.json` rewrites are correct

### CORS Issues
Backend has `CORS(app)` enabled - allows all origins.
If issues persist, check browser console for specific errors.

---

## 📊 Current Stats

- **Items in Database**: 5,655
- **Main Divisions**: 15
- **Database Type**: PostgreSQL (production) / SQLite (development)

---

## 👤 Contact

Built by **Sameh Badawy Sayed**

---

*Last Updated: December 11, 2025*
