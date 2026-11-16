from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# User schemas

class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


# Candidate profile schemas

class CandidateProfileCreate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    education: Optional[str] = None
    experience_summary: Optional[str] = None


class CandidateProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    education: Optional[str] = None
    experience_summary: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: str
    password: str

class CandidateSkillCreate(BaseModel):
    skill_name: str


class CandidateSkillResponse(BaseModel):
    id: int
    user_id: int
    skill_name: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class CandidateFactCreate(BaseModel):
    category: str
    fact_text: str
    source: Optional[str] = None


class CandidateFactResponse(BaseModel):
    id: int
    user_id: int
    category: str
    fact_text: str
    is_verified: bool
    source: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ApplicationCreate(BaseModel):
    company_name: str
    job_title: str
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    location: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    job_title: str
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    location: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


class ApplicationStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None


class ApplicationStatusHistoryResponse(BaseModel):
    id: int
    application_id: int
    old_status: Optional[str] = None
    new_status: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class ApplicationArtifactCreate(BaseModel):
    artifact_type: str
    content_text: Optional[str] = None
    storage_key: Optional[str] = None


class ApplicationArtifactResponse(BaseModel):
    id: int
    application_id: int
    artifact_type: str
    content_text: Optional[str] = None
    storage_key: Optional[str] = None
    version_number: int

    class Config:
        from_attributes = True

class InterviewCreate(BaseModel):
    interview_round: Optional[str] = None
    interview_date: Optional[datetime] = None
    interview_type: Optional[str] = None
    interviewer_name: Optional[str] = None
    questions_asked: Optional[str] = None
    candidate_responses: Optional[str] = None
    feedback: Optional[str] = None
    result: Optional[str] = None


class InterviewResponse(BaseModel):
    id: int
    application_id: int
    interview_round: Optional[str] = None
    interview_date: Optional[datetime] = None
    interview_type: Optional[str] = None
    interviewer_name: Optional[str] = None
    questions_asked: Optional[str] = None
    candidate_responses: Optional[str] = None
    feedback: Optional[str] = None
    result: Optional[str] = None

    class Config:
        from_attributes = True

class ApplicationQuestionAnswerCreate(BaseModel):
    question: str
    answer: Optional[str] = None
    answer_verified: bool = False


class ApplicationQuestionAnswerResponse(BaseModel):
    id: int
    application_id: int
    question: str
    answer: Optional[str] = None
    answer_verified: bool

    class Config:
        from_attributes = True

class CommunicationCreate(BaseModel):
    direction: str
    channel: str
    subject: Optional[str] = None
    message_content: str
    sent_at: Optional[datetime] = None


class CommunicationResponse(BaseModel):
    id: int
    application_id: int
    direction: str
    channel: str
    subject: Optional[str] = None
    message_content: str
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class JobAnalysisRequest(BaseModel):
    job_description: str


class JobAnalysisResponse(BaseModel):
    analysis: str

class JobMatchRequest(BaseModel):
    job_description: str


class JobMatchResponse(BaseModel):
    match_analysis: str

class ResumeGenerationRequest(BaseModel):
    application_id: int
    job_description: str


class ResumeGenerationResponse(BaseModel):
    tailored_resume: str

class CoverLetterRequest(BaseModel):
    application_id: int
    job_description: str


class CoverLetterResponse(BaseModel):
    cover_letter: str

class AIAnswerRequest(BaseModel):
    question: str


class AIAnswerResponse(BaseModel):
    answer: str

class JobDocumentAnalysisResponse(BaseModel):
    filename: str
    analysis: str


class DocumentExtractResponse(BaseModel):
    filename: str
    extracted_text: str