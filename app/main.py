
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

from app.document_services import extract_text_from_document
from app.learning_service import generate_application_insights
from app.ai_service import generate_ai_response

from fastapi.middleware.cors import CORSMiddleware

from app.learning_service import generate_interview_improvements
from app.database import engine, get_db
from app.models import (
    Base,
    User,
    CandidateProfile,
    CandidateSkill,
    Application,
    ApplicationStatusHistory,
    CandidateFact,
    ApplicationArtifact,
    Communication,
    ApplicationQuestionAnswer,
    Interview

)
from app.schemas import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse,
    CandidateProfileCreate,
    CandidateProfileResponse,
    CandidateSkillCreate,
    CandidateSkillResponse,
    CandidateFactCreate,
    CandidateFactResponse,
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
    ApplicationStatusHistoryResponse,
    ApplicationArtifactResponse,
    ApplicationArtifactCreate,
    InterviewCreate,
    InterviewResponse,
    ApplicationQuestionAnswerCreate,
    ApplicationQuestionAnswerResponse,
    CommunicationResponse,
    CommunicationCreate,
    JobMatchRequest,
    JobMatchResponse,
    ResumeGenerationRequest,
    ResumeGenerationResponse,
    CoverLetterResponse,
    CoverLetterRequest,
    AIAnswerRequest,
    AIAnswerResponse,
    JobAnalysisResponse,
    JobAnalysisRequest,
    JobDocumentAnalysisResponse,
    DocumentExtractResponse
)
from app.security import hash_password
from app.security import verify_password
from app.token import create_access_token
from app.auth import get_current_user

app = FastAPI(
    title="AI Job Application Agent",
    description="AI-powered job application platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",
        "http://127.0.0.1:63342"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "AI Job Application Agent is running"}


@app.get("/db-check")
def check_database():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        return {"database": "Connected successfully"}


@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login", response_model=TokenResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(existing_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user

@app.post("/profile", response_model=CandidateProfileResponse)
def create_profile(
    profile: CandidateProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_profile = db.query(CandidateProfile).filter(
        CandidateProfile.user_id == current_user.id
    ).first()

    if existing_profile:
        raise HTTPException(
            status_code=409,
            detail="Profile already exists"
        )

    new_profile = CandidateProfile(
        user_id=current_user.id,
        full_name=profile.full_name,
        phone=profile.phone,
        location=profile.location,
        education=profile.education,
        experience_summary=profile.experience_summary
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile

@app.get("/profile", response_model=CandidateProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(CandidateProfile).filter(
        CandidateProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile

@app.post("/skills", response_model=CandidateSkillResponse)
def add_skill(
    skill: CandidateSkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_skill = CandidateSkill(
        user_id=current_user.id,
        skill_name=skill.skill_name
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill

@app.get("/skills", response_model=list[CandidateSkillResponse])
def get_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skills = db.query(CandidateSkill).filter(
        CandidateSkill.user_id == current_user.id
    ).all()

    return skills

@app.post("/facts", response_model=CandidateFactResponse)
def add_fact(
    fact: CandidateFactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_fact = CandidateFact(
        user_id=current_user.id,
        category=fact.category,
        fact_text=fact.fact_text,
        source=fact.source
    )

    db.add(new_fact)
    db.commit()
    db.refresh(new_fact)

    return new_fact

@app.get("/facts", response_model=list[CandidateFactResponse])
def get_facts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    facts = db.query(CandidateFact).filter(
        CandidateFact.user_id == current_user.id
    ).all()

    return facts

# Create a job application
@app.post("/applications", response_model=ApplicationResponse)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_application = Application(
        user_id=current_user.id,
        company_name=application.company_name,
        job_title=application.job_title,
        job_url=application.job_url,
        job_description=application.job_description,
        location=application.location,
        status="applied"
    )

    db.add(new_application)
    db.flush()

    history = ApplicationStatusHistory(
        application_id=new_application.id,
        old_status=None,
        new_status="applied",
        notes="Application created"
    )

    db.add(history)
    db.commit()
    db.refresh(new_application)

    return new_application


# Get all applications of the logged-in user
@app.get("/applications", response_model=List[ApplicationResponse])
def get_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).all()

    return applications


# Update application status
@app.patch(
    "/applications/{application_id}/status",
    response_model=ApplicationResponse
)
def update_application_status(
    application_id: int,
    status_update: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    old_status = application.status

    application.status = status_update.status

    history = ApplicationStatusHistory(
        application_id=application.id,
        old_status=old_status,
        new_status=status_update.status,
        notes=status_update.notes
    )

    db.add(history)
    db.commit()
    db.refresh(application)

    return application


# Get application status history
@app.get(
    "/applications/{application_id}/history",
    response_model=List[ApplicationStatusHistoryResponse]
)
def get_application_history(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    history = db.query(ApplicationStatusHistory).filter(
        ApplicationStatusHistory.application_id == application_id
    ).order_by(
        ApplicationStatusHistory.changed_at.desc()
    ).all()

    return history

@app.post(
    "/applications/{application_id}/artifacts",
    response_model=ApplicationArtifactResponse
)
def create_application_artifact(
    application_id: int,
    artifact: ApplicationArtifactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    new_artifact = ApplicationArtifact(
        application_id=application_id,
        artifact_type=artifact.artifact_type,
        content_text=artifact.content_text,
        storage_key=artifact.storage_key,
        version_number=1
    )

    db.add(new_artifact)
    db.commit()
    db.refresh(new_artifact)

    return new_artifact

@app.get(
    "/applications/{application_id}/artifacts",
    response_model=List[ApplicationArtifactResponse]
)
def get_application_artifacts(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    artifacts = db.query(ApplicationArtifact).filter(
        ApplicationArtifact.application_id == application_id
    ).all()

    return artifacts

@app.post(
    "/applications/{application_id}/interviews",
    response_model=InterviewResponse
)
def create_interview(
    application_id: int,
    interview: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    new_interview = Interview(
        application_id=application_id,
        interview_round=interview.interview_round,
        interview_date=interview.interview_date,
        interview_type=interview.interview_type,
        interviewer_name=interview.interviewer_name,
        questions_asked=interview.questions_asked,
        candidate_responses=interview.candidate_responses,
        feedback=interview.feedback,
        result=interview.result
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return new_interview

@app.get(
    "/applications/{application_id}/interviews",
    response_model=List[InterviewResponse]
)
def get_application_interviews(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    interviews = db.query(Interview).filter(
        Interview.application_id == application_id
    ).all()

    return interviews

@app.post(
    "/applications/{application_id}/questions",
    response_model=ApplicationQuestionAnswerResponse
)
def create_application_question(
    application_id: int,
    question_data: ApplicationQuestionAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    new_question = ApplicationQuestionAnswer(
        application_id=application_id,
        question=question_data.question,
        answer=question_data.answer,
        answer_verified=question_data.answer_verified
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question

@app.get(
    "/applications/{application_id}/questions",
    response_model=List[ApplicationQuestionAnswerResponse]
)
def get_application_questions(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    questions = db.query(ApplicationQuestionAnswer).filter(
        ApplicationQuestionAnswer.application_id == application_id
    ).all()

    return questions

@app.post(
    "/applications/{application_id}/communications",
    response_model=CommunicationResponse
)
def create_communication(
    application_id: int,
    communication: CommunicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    new_communication = Communication(
        application_id=application_id,
        direction=communication.direction,
        channel=communication.channel,
        subject=communication.subject,
        message_content=communication.message_content,
        sent_at=communication.sent_at
    )

    db.add(new_communication)
    db.commit()
    db.refresh(new_communication)

    return new_communication

@app.get(
    "/applications/{application_id}/communications",
    response_model=List[CommunicationResponse]
)
def get_application_communications(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    communications = db.query(Communication).filter(
        Communication.application_id == application_id
    ).all()

    return communications

@app.post("/ai/analyze-job", response_model=JobAnalysisResponse)
def analyze_job(
    request: JobAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    prompt = f"""
    Analyze the following job description.

    Identify:
    1. Job title and role
    2. Required technical skills
    3. Required qualifications
    4. Required experience
    5. Key responsibilities
    6. Important keywords

    Job Description:
    {request.job_description}
    """

    analysis = generate_ai_response(prompt)

    return {"analysis": analysis}

@app.post("/ai/job-match", response_model=JobMatchResponse)
def match_candidate_to_job(
    request: JobMatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(CandidateProfile).filter(
        CandidateProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    skills = db.query(CandidateSkill).filter(
        CandidateSkill.user_id == current_user.id
    ).all()

    skill_names = [skill.skill_name for skill in skills]

    prompt = f"""
    Compare the candidate's profile with the job description.

    Candidate Profile:
    Name: {profile.full_name}
    Education: {profile.education}
    Experience: {profile.experience_summary}
    Skills: {", ".join(skill_names)}

    Job Description:
    {request.job_description}

    Provide:
    1. Matching skills
    2. Missing skills
    3. Relevant qualifications
    4. Areas for improvement
    5. Overall job match assessment

    Be honest. Do not invent candidate experience or qualifications.
    """

    match_analysis = generate_ai_response(prompt)

    return {"match_analysis": match_analysis}


@app.post(
    "/ai/generate-resume",
    response_model=ResumeGenerationResponse
)
def generate_resume(
    request: ResumeGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify that the application belongs to the logged-in user
    application = db.query(Application).filter(
        Application.id == request.application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    profile = db.query(CandidateProfile).filter(
        CandidateProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    skills = db.query(CandidateSkill).filter(
        CandidateSkill.user_id == current_user.id
    ).all()

    skill_names = [skill.skill_name for skill in skills]
    application_insights = generate_application_insights(
        db,
        current_user.id
    )
    prompt = f"""
    Create a professional, ATS-friendly resume tailored to this job.

    Candidate details:
    Name: {profile.full_name}
    Phone: {profile.phone}
    Location: {profile.location}
    Education: {profile.education}
    Experience: {profile.experience_summary}
    Skills: {", ".join(skill_names)}

    Job Description:
    {request.job_description}

    Instructions:
    1. Use only the candidate information provided.
    2. Highlight relevant skills.
    3. Use relevant keywords naturally.
    4. Organize the resume with clear sections.
    5. Do not invent experience or achievements.
    6. Do not make up missing information.
    
    Previous application insights:
    {application_insights}

    Use these insights to guide keyword selection and presentation.
    Treat them as recommendations, NOT candidate facts.
    Never add skills, experience or achievements that are not verified.
    """

    tailored_resume = generate_ai_response(prompt)

    # Save the generated resume as an application artifact
    resume_artifact = ApplicationArtifact(
        application_id=request.application_id,
        artifact_type="resume",
        content_text=tailored_resume
    )

    db.add(resume_artifact)
    db.commit()
    db.refresh(resume_artifact)

    return {"tailored_resume": tailored_resume}



@app.post(
    "/ai/generate-cover-letter",
    response_model=CoverLetterResponse
)
def generate_cover_letter(
    request: CoverLetterRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == request.application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    profile = db.query(CandidateProfile).filter(
        CandidateProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    skills = db.query(CandidateSkill).filter(
        CandidateSkill.user_id == current_user.id
    ).all()

    skill_names = [skill.skill_name for skill in skills]

    application_insights = generate_application_insights(
        db,
        current_user.id
    )
    prompt = f"""
    Write a professional and personalized cover letter
    for the following job.

    Candidate details:
    Name: {profile.full_name}
    Education: {profile.education}
    Experience: {profile.experience_summary}
    Skills: {", ".join(skill_names)}

    Job Description:
    {request.job_description}

    Instructions:
    1. Explain why the candidate is suitable for this role.
    2. Highlight relevant skills and education.
    3. Use a professional and natural tone.
    4. Do not invent experience or achievements.
    5. Keep the cover letter concise.
    
    Previous application insights:
    {application_insights}

    Use these insights to improve how relevant skills and experience
    are presented for this role.

    Do not invent candidate facts or achievements.
    """

    cover_letter = generate_ai_response(prompt)

    cover_letter_artifact = ApplicationArtifact(
        application_id=request.application_id,
        artifact_type="cover_letter",
        content_text=cover_letter
    )

    db.add(cover_letter_artifact)
    db.commit()
    db.refresh(cover_letter_artifact)

    return {"cover_letter": cover_letter}


@app.post(
    "/ai/generate-answer",
    response_model=AIAnswerResponse
)
def generate_application_answer(
    request: AIAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    facts = db.query(CandidateFact).filter(
        CandidateFact.user_id == current_user.id,
        CandidateFact.is_verified == True
    ).all()

    if not facts:
        raise HTTPException(
            status_code=404,
            detail="No verified candidate facts found"
        )

    candidate_facts = "\n".join(
        [fact.fact_text for fact in facts]
    )

    prompt = f"""
    Answer the following job application question
    using only the candidate's verified facts.

    Verified Candidate Facts:
    {candidate_facts}

    Question:
    {request.question}

    Instructions:
    1. Write a clear and professional answer.
    2. Use only the verified facts provided.
    3. Do not invent experience, skills or achievements.
    4. If the facts are insufficient, clearly say so.
    """

    answer = generate_ai_response(prompt)

    return {"answer": answer}

@app.post("/ai/analyze-job-document",
          response_model=JobDocumentAnalysisResponse
          )
async def analyze_job_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    try:
        job_description = extract_text_from_document(
            file.filename or "",
            file_content
        )

        prompt = f"""
        Analyze the following job description.

         1. Job title and role
        2. Required technical skills
        3. Required qualifications
        4. Required experience
        5. Key responsibilities
        6. Important keywords
        7. Preferred skills, if mentioned

        Do not invent information that is not present
        in the job description.

        Job Description:
        {job_description}
        """

        analysis = generate_ai_response(prompt)

        return {
            "filename": file.filename,
            "analysis": analysis
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@app.post("/documents/extract",
          response_model=DocumentExtractResponse
          )
async def extract_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    file_content = await file.read()

    try:
        extracted_text = extract_text_from_document(
            file.filename,
            file_content
        )

        return {
            "filename": file.filename,
            "extracted_text": extracted_text
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ai/application-insights")
def get_application_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    insights = generate_application_insights(
        db,
        current_user.id
    )

    return {"insights": insights}


@app.get("/ai/interview-improvements")
def get_interview_improvements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    improvements = generate_interview_improvements(
        db,
        current_user.id
    )

    return {"improvements": improvements}



@app.get("/applications/{application_id}/overview")
def get_application_overview(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    artifacts = db.query(ApplicationArtifact).filter(
        ApplicationArtifact.application_id == application_id
    ).all()

    communications = db.query(Communication).filter(
        Communication.application_id == application_id
    ).all()

    history = db.query(ApplicationStatusHistory).filter(
        ApplicationStatusHistory.application_id == application_id
    ).all()

    interviews = db.query(Interview).filter(
        Interview.application_id == application_id
    ).all()

    questions = db.query(ApplicationQuestionAnswer).filter(
        ApplicationQuestionAnswer.application_id == application_id
    ).all()

    return {
        "application": application,
        "artifacts": artifacts,
        "communications": communications,
        "status_history": history,
        "interviews": interviews,
        "questions_and_answers": questions
    }
