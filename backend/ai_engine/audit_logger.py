"""
Governance Audit Logger
Immutable, timestamped decision log for every action in the system.
Supports export to JSON and CSV.
"""
import uuid
import datetime
import json
import csv
import io
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from database.models import AuditLog


def create_log(
    db: Session,
    student_id: str,
    drive_id: str,
    action: str,
    policy_check: Optional[str] = None,
    policy_details: Optional[Dict] = None,
    ai_score: Optional[float] = None,
    missing_skills: Optional[List[str]] = None,
    final_decision: Optional[str] = None,
    reasoning: Optional[str] = None,
    actor: str = "SYSTEM",
) -> AuditLog:
    """Write a new immutable audit log entry."""
    log = AuditLog(
        id=str(uuid.uuid4()),
        timestamp=datetime.datetime.utcnow(),
        student_id=student_id,
        drive_id=drive_id,
        action=action,
        policy_check=policy_check,
        policy_details=policy_details or {},
        ai_score=ai_score,
        missing_skills=missing_skills or [],
        final_decision=final_decision,
        reasoning=reasoning,
        actor=actor,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_logs(
    db: Session,
    student_id: Optional[str] = None,
    drive_id: Optional[str] = None,
    limit: int = 100,
) -> List[AuditLog]:
    """Query audit logs with optional filters."""
    q = db.query(AuditLog)
    if student_id:
        q = q.filter(AuditLog.student_id == student_id)
    if drive_id:
        q = q.filter(AuditLog.drive_id == drive_id)
    return q.order_by(AuditLog.timestamp.desc()).limit(limit).all()


def export_logs_json(logs: List[AuditLog]) -> str:
    """Serialize logs to JSON string."""
    data = []
    for log in logs:
        data.append({
            "id": log.id,
            "timestamp": log.timestamp.isoformat() if log.timestamp else None,
            "student_id": log.student_id,
            "drive_id": log.drive_id,
            "action": log.action,
            "policy_check": log.policy_check,
            "policy_details": log.policy_details,
            "ai_score": log.ai_score,
            "missing_skills": log.missing_skills,
            "final_decision": log.final_decision,
            "reasoning": log.reasoning,
            "actor": log.actor,
        })
    return json.dumps(data, indent=2)


def export_logs_csv(logs: List[AuditLog]) -> str:
    """Serialize logs to CSV string."""
    output = io.StringIO()
    fieldnames = [
        "id", "timestamp", "student_id", "drive_id", "action",
        "policy_check", "ai_score", "missing_skills", "final_decision", "reasoning", "actor"
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for log in logs:
        writer.writerow({
            "id": log.id,
            "timestamp": log.timestamp.isoformat() if log.timestamp else "",
            "student_id": log.student_id,
            "drive_id": log.drive_id,
            "action": log.action,
            "policy_check": log.policy_check or "",
            "ai_score": log.ai_score or "",
            "missing_skills": "|".join(log.missing_skills) if log.missing_skills else "",
            "final_decision": log.final_decision or "",
            "reasoning": log.reasoning or "",
            "actor": log.actor or "SYSTEM",
        })
    return output.getvalue()
