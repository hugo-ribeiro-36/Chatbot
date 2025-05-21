from fastapi import APIRouter
from sqlalchemy import func, case
from app.db.database import db_session
from app.db.models import Feedback
from fastapi.responses import StreamingResponse
import io
import csv

router = APIRouter()

@router.get("/summary")
def feedback_summary():
    """
    Returns a summary of feedback statistics grouped by version (A/B).

    The summary includes:
    - Total number of feedback entries
    - Average score (ignoring neutral scores)
    - Count of thumbs up and thumbs down
    - A ratio string (e.g., "5:3")

    Returns:
        list[dict]: A list of summary entries per version.
    """
    data = db_session.query(
        Feedback.version,
        func.count(Feedback.id),
        func.avg(func.nullif(Feedback.rating, 0)),
        func.sum(case((Feedback.rating == 1, 1), else_=0)).label("thumbs_up"),
        func.sum(case((Feedback.rating == -1, 1), else_=0)).label("thumbs_down")
    ).group_by(Feedback.version).all()

    return [
        {
            "version": version,
            "total_feedback": total,
            "average_score": round(avg or 0, 2),
            "thumbs_up": up,
            "thumbs_down": down,
            "score_ratio": f"{up}:{down}" if down else f"{up}:0"
        }
        for version, total, avg, up, down in data
    ]


@router.get("/summary/export")
def export_feedback_summary_csv():
    """
    Exports feedback summary statistics as a downloadable CSV file.

    The CSV includes:
    - Version (A or B)
    - Total feedback count
    - Average score
    - Thumbs up count
    - Thumbs down count

    Returns:
        StreamingResponse: A CSV file stream with feedback summary data.
    """
    data = db_session.query(
        Feedback.version,
        func.count(Feedback.id),
        func.avg(func.nullif(Feedback.rating, 0)),
        func.sum(case((Feedback.rating == 1, 1), else_=0)).label("thumbs_up"),
        func.sum(case((Feedback.rating == -1, 1), else_=0)).label("thumbs_down")
    ).group_by(Feedback.version).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Version", "Total Feedback", "Average Score", "Thumbs Up", "Thumbs Down"])

    for row in data:
        version, total, avg, up, down = row
        writer.writerow([version, total, round(avg or 0, 2), up, down])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=feedback_summary.csv"})