# 🚀 PathFinder AI — Intelligent Campus Placement ERP

> AI-powered campus placement management system that matches students with job drives — fairly, transparently, and without any external API.

**Team algoRhythmss | Hackathon 2026**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Frontend-7c3aed?style=for-the-badge)](https://pathfinder-ai-prototype-1.onrender.com)
[![Backend API](https://img.shields.io/badge/Backend%20API-Docs-06b6d4?style=for-the-badge)](https://pathfinder-ai-prototype.onrender.com/docs)

---

## 🌐 Live Links

| Service | URL |
|---------|-----|
| 🖥️ Frontend App | https://pathfinder-ai-prototype-1.onrender.com |
| ⚙️ Backend API | https://pathfinder-ai-prototype.onrender.com |
| 📖 API Docs (Swagger) | https://pathfinder-ai-prototype.onrender.com/docs |

> ⚠️ **Note:** The backend is hosted on Render's free tier and may take up to 50 seconds to wake up on the first request.

---

## 📌 What Is This?

PathFinder AI is a full-stack campus placement management system powered by a **hybrid AI pipeline**. The system works in two stages:

1. **Policy Gateway** — Hard rule engine (CGPA, backlogs, branch). If a student fails here, AI never runs.
2. **AI Semantic Matcher** — Uses `all-MiniLM-L6-v2` (HuggingFace) to compute a Career Readiness Score (CRS) based on resume, skills, and projects vs the job description.

Every decision is logged in an **immutable audit trail** — who was selected, why, and by whom.

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TailwindCSS |
| Backend | Python FastAPI |
| Database | SQLite |
| AI Model | HuggingFace `all-MiniLM-L6-v2` |
| ORM | SQLAlchemy |
| Validation | Pydantic v2 |

---

## 🎭 3 Role Dashboards

| Role | Features |
|------|----------|
| **Student** | View CRS, upload resume, browse drives, apply, see career roadmap |
| **Recruiter** | Create drives, set eligibility rules, view AI-ranked shortlist |
| **Admin/TPO** | Analytics, all students/drives, export audit logs (JSON/CSV) |

---

## 🧠 How the AI Works

### Policy Gateway (runs first)
Hard rules checked before any AI:
```
Rule 1: student.cgpa >= drive.min_cgpa
Rule 2: student.active_backlogs <= drive.max_backlogs
Rule 3: student.branch in drive.eligible_branches

Any rule FAILS → instant rejection. AI never runs.
All rules PASS → proceed to AI matcher.
```

### CRS (Career Readiness Score)
```
CRS = (Semantic Score × 0.50) + (Project Score × 0.30) + (Completeness × 0.20)
```

| Component | Weight | How |
|-----------|--------|-----|
| Semantic Skill Match | 50% | Cosine similarity between resume and JD using `all-MiniLM-L6-v2` |
| Project Relevance | 30% | Semantic similarity between student projects and JD |
| Resume Completeness | 20% | Skills, projects, certifications, contact, resume text |

**Score ranges:**
- 🟢 75–100 → Strong match
- 🟡 50–75 → Good match
- 🟠 25–50 → Skill gaps exist
- 🔴 0–25 → Poor fit

---

## 📁 Project Structure

```
pathfinder-ai/
├── backend/
│   ├── main.py                    ← FastAPI entry point
│   ├── requirements.txt
│   ├── database/
│   │   ├── models.py              ← SQLAlchemy ORM models
│   │   └── seed.py                ← 20 mock students + 5 drives
│   └── ai_engine/
│       ├── policy_gateway.py      ← Rule engine (CGPA, backlogs, branch)
│       ├── matcher.py             ← CRS computation + NLP matching
│       └── audit_logger.py        ← Immutable audit log writer
│
└── frontend/
    ├── package.json
    ├── tailwind.config.js
    └── src/
        ├── App.js                 ← Router + all routes
        ├── services/api.js        ← Axios API layer
        ├── components/
        │   ├── ui.jsx             ← Shared UI components
        │   ├── Sidebar.jsx
        │   └── Layout.jsx
        └── pages/
            ├── Landing.jsx        ← Home with role selector
            ├── student/           ← Dashboard, Resume Upload, Apply, Roadmap
            ├── recruiter/         ← Create Drive, View Shortlist
            └── admin/             ← Analytics, Audit Logs, Export
```

---

## ⚡ How to Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm 9+

### Step 1 — Backend

```bash
cd pathfinder-ai/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

✅ Backend: `http://localhost:8000`
✅ API Docs: `http://localhost:8000/docs`

### Step 2 — Frontend

```bash
cd pathfinder-ai/frontend

npm install
npm start
```

✅ App: `http://localhost:3000`

---

## 🔗 Key API Endpoints

```bash
GET  /students                    # List all students
GET  /drives                      # List all drives
POST /upload-resume               # Upload resume text
GET  /eligibility/{student_id}    # Check eligibility across all drives
POST /apply                       # Apply to drive (runs Policy + CRS)
GET  /shortlist/{drive_id}        # Ranked candidates for a drive
POST /shortlist/approve           # TPO approves a candidate
GET  /audit-logs                  # Full audit trail
GET  /audit-logs/export/csv       # Export as CSV
GET  /audit-logs/export/json      # Export as JSON
GET  /analytics/overview          # Platform-wide analytics
```

---

## 📊 Mock Data (Pre-seeded)

**20 Students** — CGPA range 6.5–9.6, branches CSE/IT/ECE/MCA, varied skills

**5 Drives:**

| Company | Role | Min CGPA | Package |
|---------|------|----------|---------|
| TCS | Software Developer | 6.0 | 7–9 LPA |
| Google | SWE | 8.5 | 30–45 LPA |
| Infosys | Systems Engineer | 6.5 | 3.5–5 LPA |
| Amazon | SDE-1 | 7.5 | 24–32 LPA |
| Deloitte | Data Analyst | 7.0 | 8–12 LPA |

---

## 🎨 UI Theme

Dark cyber aesthetic — Background `#0a0a1a`, Accent violet `#7c3aed`, Cyan `#06b6d4`

---

Built with ❤️ for **Hackathon 2026**