from datetime import datetime, timezone
from pathlib import Path

REPORT = Path("report.log")

def log_completion_report(task_id: int, title: str, user_id: str, completed_at: datetime):
    report = (
        f"Task completed | Owner: {user_id} | Task_ID: {task_id} | Title: {title} |Completed at: {completed_at.isoformat()}\n"
    )

    with REPORT.open("a", encoding="utf-8") as file:
        file.write(report)