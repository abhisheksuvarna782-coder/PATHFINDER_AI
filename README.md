# 🚀 PathFinder AI — Intelligent Campus Placement ERP.

AI-powered campus placement management system that matches students with job drives — fairly, transparently, and without any external API

**Team algoRhythmss | Hackathon 2026**

---

## 🔗 Quick Access.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Frontend-7c3aed?style=for-the-badge)](https://pathfinder-ai-v2.onrender.com)
[![Backend API](https://img.shields.io/badge/Backend%20API-Swagger%20Docs-06b6d4?style=for-the-badge)](https://pathfinder-ai-09pz.onrender.com/docs)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

---.

## 🌐 Live Links

| Service | URL |
|--------|-----|
| 🖥️ Frontend App | https://pathfinder-ai-v2.onrender.com |
| ⚙️ Backend API | https://pathfinder-ai-09pz.onrender.com |
| 📖 API Docs (Swagger) | https://pathfinder-ai-09pz.onrender.com/docs |

> ⚠️ Backend is hosted on Render free tier — first request may take 30–60 seconds to wake up.

---

## 📌 What Is PathFinder AI?

PathFinder AI is a full-stack campus placement ERP powered by a **hybrid AI pipeline** connecting:

- 🎓 Students  
- 🏢 Recruiters  
- 🏫 Admin / TPO  

It ensures **transparent, fair, and explainable placement decisions**.

---

## 🧠 System Pipeline

### 1️⃣ Policy Gateway
Hard rule engine checks:

- CGPA
- Backlogs
- Branch eligibility

If a student fails → AI does not run.

---

### 2️⃣ AI Semantic Matcher
Uses local model:
all-MiniLM-L6-v2

Calculates **Career Readiness Score (CRS)** using resume vs job description.

---

### 3️⃣ Audit Logger
Logs every decision with:

- Timestamp  
- Score  
- Reasoning  

Exportable as:

- JSON  
- CSV  

---

## 📊 CRS Formula
CRS = (Semantic Skill Match × 50%)
+ (Project Relevance × 30%)
+ (Resume Completeness × 20%)

+ 
| Score | Meaning |
|-----|------|
| 🟢 75–100 | Strong match |
| 🟡 50–75 | Good match |
| 🟠 25–50 | Skill gaps |
| 🔴 0–25 | Poor fit |

---

## 🎭 Role Dashboards

### 👨‍🎓 Student
- Upload resume (PDF / text)
- Skill extraction
- Apply to drives
- CRS breakdown
- Career roadmap

### 🏢 Recruiter
- Post job drives
- AI skill extraction
- Eligibility rules
- Ranked shortlist

### 🏫 Admin / TPO
- Platform analytics
- Student registry
- Placement drives
- Full audit trail

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + TailwindCSS |
| Backend | FastAPI + Uvicorn |
| Database | SQLite |
| AI Model | all-MiniLM-L6-v2 |
| ORM | SQLAlchemy |
| Deployment | Render |

---

## ⚡ Run Locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

API → http://localhost:8000

Frontend

cd frontend
npm install
npm start

App → http://localhost:3000

❤️ Built For Hackathon 2026

Team algoRhythmss
