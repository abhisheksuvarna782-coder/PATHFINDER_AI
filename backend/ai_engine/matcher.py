"""
AI Semantic Matcher - Local NLP with sentence-transformers
CRS Formula:
  Semantic Skill Match  → 50%
  Project Relevance     → 30%
  Resume Completeness   → 20%
Uses: all-MiniLM-L6-v2 (local, no external API calls)
"""
from typing import Dict, List, Tuple
import re
import math

# ── Lazy-load model to avoid slow startup ────────────────────────────────────
_model = None

def get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer("all-MiniLM-L6-v2")
            print("✅ Loaded sentence-transformers model: all-MiniLM-L6-v2")
        except Exception as e:
            print(f"⚠️  Could not load sentence-transformers: {e}. Using fallback similarity.")
            _model = "FALLBACK"
    return _model


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Pure-python cosine similarity (fallback)."""
    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = math.sqrt(sum(a * a for a in vec1))
    mag2 = math.sqrt(sum(b * b for b in vec2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings; fall back to keyword-overlap if model unavailable."""
    model = get_model()
    if model == "FALLBACK":
        return _fallback_embeddings(texts)
    try:
        embeddings = model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    except Exception:
        return _fallback_embeddings(texts)


def _fallback_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Simple TF-based bag-of-words vector when sentence-transformers unavailable.
    Returns 300-dim sparse vector.
    """
    vocab = {}
    tokenized = []
    for text in texts:
        tokens = re.findall(r'\b\w+\b', text.lower())
        tokenized.append(tokens)
        for t in tokens:
            if t not in vocab:
                vocab[t] = len(vocab)

    vecs = []
    for tokens in tokenized:
        vec = [0.0] * max(300, len(vocab))
        for t in tokens:
            if t in vocab:
                vec[vocab[t]] += 1.0
        # L2 normalize
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        vecs.append([x / norm for x in vec])
    return vecs


def extract_skills_from_text(text: str) -> List[str]:
    """Extract skill keywords from resume or JD text."""
    # Tech skills dictionary for matching
    KNOWN_SKILLS = {
        "python", "java", "javascript", "typescript", "golang", "go", "c++", "c#",
        "react", "vue", "angular", "next.js", "node.js", "express", "django", "flask",
        "fastapi", "spring", "spring boot", "hibernate", "laravel", "php",
        "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "kafka",
        "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "jenkins", "ci/cd",
        "machine learning", "deep learning", "nlp", "computer vision", "pytorch", "tensorflow",
        "pandas", "numpy", "scikit-learn", "transformers", "hugging face",
        "rest api", "graphql", "grpc", "microservices", "system design",
        "data structures", "algorithms", "oop", "devops", "agile", "scrum",
        "power bi", "tableau", "data analysis", "statistics",
        "android", "kotlin", "ios", "swift", "react native", "flutter",
        "cybersecurity", "ethical hacking", "network security",
        "html", "css", "bootstrap", "tailwind",
        "git", "linux", "bash", "shell scripting",
        "socket.io", "websocket", "redis", "celery",
        "embedded c", "rtos", "arduino", "raspberry pi", "iot", "vlsi", "verilog", "matlab",
    }
    text_lower = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            found.append(skill.title())
    return list(set(found))


def compute_semantic_similarity(text1: str, text2: str) -> float:
    """Compute semantic cosine similarity between two texts."""
    embeddings = embed_texts([text1, text2])
    # Ensure same dimension for fallback
    v1, v2 = embeddings[0], embeddings[1]
    min_len = min(len(v1), len(v2))
    return cosine_similarity(v1[:min_len], v2[:min_len])


def compute_project_relevance(projects: List[str], jd_text: str) -> float:
    """Score how relevant student projects are to the JD."""
    if not projects:
        return 0.3  # some base score if no projects listed
    project_text = " ".join(projects)
    sim = compute_semantic_similarity(project_text, jd_text)
    # Scale: 0.3–1.0 → normalize to 0–100
    normalized = min(1.0, max(0.0, (sim - 0.1) / 0.7))
    return normalized


def compute_completeness_score(student: Dict) -> float:
    """
    Score resume completeness:
    - Has skills listed    → 30 pts
    - Has projects         → 30 pts
    - Has certifications   → 20 pts
    - Has phone/contact    → 10 pts
    - Has resume text      → 10 pts
    """
    score = 0
    if student.get("skills") and len(student["skills"]) >= 3:
        score += 30
    elif student.get("skills"):
        score += 15
    if student.get("projects") and len(student["projects"]) >= 1:
        score += 30
    if student.get("certifications") and len(student["certifications"]) >= 1:
        score += 20
    if student.get("phone"):
        score += 10
    if student.get("resume_text") and len(student["resume_text"]) > 100:
        score += 10
    return score / 100.0


def compute_crs(student: Dict, drive: Dict) -> Dict:
    """
    Compute Career Readiness Score (CRS).

    CRS = (Semantic Skill Match × 0.5) + (Project Relevance × 0.3) + (Resume Completeness × 0.2)
    All components normalized to 0–100. Final CRS is 0–100.
    """
    student_skills = student.get("skills", [])
    drive_skills = drive.get("required_skills", [])
    jd_text = drive.get("jd_text", " ".join(drive_skills))
    student_resume = student.get("resume_text", " ".join(student_skills + student.get("projects", [])))

    # ── Component 1: Semantic Skill Match (50%) ───────────────────────────────
    skill_sim = compute_semantic_similarity(student_resume, jd_text)
    semantic_score = min(100.0, skill_sim * 150)  # scale up for better discrimination

    # Identify matched and missing skills
    student_skills_lower = [s.lower() for s in student_skills]
    matched_skills = [s for s in drive_skills if s.lower() in student_skills_lower or
                     any(s.lower() in sk.lower() or sk.lower() in s.lower() for sk in student_skills_lower)]
    missing_skills = [s for s in drive_skills if s not in matched_skills]

    # Boost score if direct skill matches found
    if drive_skills:
        direct_match_ratio = len(matched_skills) / len(drive_skills)
        semantic_score = max(semantic_score, direct_match_ratio * 100)

    # ── Component 2: Project Relevance (30%) ──────────────────────────────────
    project_relevance = compute_project_relevance(student.get("projects", []), jd_text)
    project_score = project_relevance * 100

    # ── Component 3: Resume Completeness (20%) ────────────────────────────────
    completeness = compute_completeness_score(student)
    completeness_score = completeness * 100

    # ── Final CRS ─────────────────────────────────────────────────────────────
    crs = (semantic_score * 0.5) + (project_score * 0.3) + (completeness_score * 0.2)
    crs = round(min(100.0, max(0.0, crs)), 1)

    return {
        "crs_score": crs,
        "semantic_score": round(semantic_score, 1),
        "project_score": round(project_score, 1),
        "completeness_score": round(completeness_score, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "improvement_suggestions": generate_suggestions(missing_skills, crs),
    }


def generate_suggestions(missing_skills: List[str], crs: float) -> List[str]:
    """Generate career improvement suggestions based on gaps."""
    suggestions = []
    if missing_skills:
        suggestions.append(f"📚 Learn missing skills: {', '.join(missing_skills[:3])}")
    if crs < 50:
        suggestions.append("🔨 Build 2–3 real-world projects to improve project relevance score")
        suggestions.append("📝 Complete relevant online certifications on Coursera or Udemy")
    elif crs < 75:
        suggestions.append("⬆️ Strengthen your portfolio with more domain-specific projects")
        suggestions.append("🏆 Consider getting an industry-recognized certification")
    else:
        suggestions.append("✅ Strong profile! Focus on competitive programming to stand out")
        suggestions.append("🌟 Contribute to open-source to boost visibility")
    return suggestions
