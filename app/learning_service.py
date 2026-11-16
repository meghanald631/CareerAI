
from app.models import (
    Application,
    Communication,
    ApplicationStatusHistory,
    Interview,
    ApplicationQuestionAnswer,
    CandidateFact
)
from app.ai_service import generate_ai_response


def generate_application_insights(db, user_id: int):

    applications = db.query(Application).filter(
        Application.user_id == user_id
    ).order_by(
        Application.created_at.desc()
    ).limit(30).all()

    if not applications:
        return "No application history available for analysis."

    application_ids = [app.id for app in applications]

    communications = db.query(Communication).filter(
        Communication.application_id.in_(application_ids)
    ).order_by(
        Communication.created_at.desc()
    ).limit(50).all()

    status_history = db.query(ApplicationStatusHistory).filter(
        ApplicationStatusHistory.application_id.in_(application_ids)
    ).order_by(
        ApplicationStatusHistory.changed_at.desc()
    ).limit(50).all()

    application_data = []

    for app in applications:
        application_data.append({
            "company": app.company_name,
            "job_title": app.job_title,
            "status": app.status,
            "job_description": app.job_description
        })

    communication_data = []

    for communication in communications:
        communication_data.append({
            "application_id": communication.application_id,
            "direction": communication.direction,
            "channel": communication.channel,
            "subject": communication.subject,
            "message": communication.message_content[:3000]
        })

    history_data = []

    for record in status_history:
        history_data.append({
            "application_id": record.application_id,
            "old_status": record.old_status,
            "new_status": record.new_status,
            "notes": record.notes
        })

    prompt = f"""
    You are an application outcome analysis assistant.

    Analyse the candidate's historical job applications.

    APPLICATIONS:
    {application_data}

    COMMUNICATIONS:
    {communication_data}

    STATUS HISTORY:
    {history_data}

    Analyse the following:

    1. Application patterns and outcomes.
    2. Skills or job requirements associated with interview invitations.
    3. Common rejection reasons, if explicitly available.
    4. Recruiter feedback and recurring observations.
    5. Applications that received no recorded response.
    6. Improvements recommended for future applications.

    Important rules:
    - Do not invent rejection reasons.
    - Do not assume every incoming message is from a recruiter.
    - Distinguish incoming and outgoing communications.
    - Do not claim that a skill caused an interview or rejection.
    - Clearly mention when there is insufficient data.
    - Base every observation on the supplied records.

    Present the findings in clear sections.
    """

    insights = generate_ai_response(prompt)

    return insights


def generate_interview_improvements(db, user_id: int):

    applications = db.query(Application).filter(
        Application.user_id == user_id
    ).all()

    application_ids = [app.id for app in applications]

    if not application_ids:
        return "No interview history available."

    interviews = db.query(Interview).filter(
        Interview.application_id.in_(application_ids)
    ).all()

    questions = db.query(ApplicationQuestionAnswer).filter(
        ApplicationQuestionAnswer.application_id.in_(application_ids)
    ).all()

    facts = db.query(CandidateFact).filter(
        CandidateFact.user_id == user_id,
        CandidateFact.is_verified == True
    ).all()

    interview_data = [
        {
            "round": interview.interview_round,
            "questions": interview.questions_asked,
            "responses": interview.candidate_responses,
            "feedback": interview.feedback,
            "result": interview.result
        }
        for interview in interviews
    ]

    question_data = [
        {
            "question": item.question,
            "answer": item.answer,
            "verified": item.answer_verified
        }
        for item in questions
    ]

    verified_facts = [
        fact.fact_text for fact in facts
    ]

    prompt = f"""
    Analyse the candidate's previous interview performance.

    Previous interviews:
    {interview_data}

    Previous questions and answers:
    {question_data}

    Verified candidate facts:
    {verified_facts}

    Identify:
    1. Repeated interview questions.
    2. Weak or incomplete answers, where evidence supports this.
    3. Interviewer feedback patterns.
    4. Topics requiring more preparation.
    5. Suggested improved answers based only on verified facts.

    Never invent experience, projects, skills or achievements.
    Clearly identify when information is insufficient.
    """

    return generate_ai_response(prompt)
