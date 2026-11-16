from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    func,
    Boolean
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    full_name = Column(String(150), nullable=False)
    phone = Column(String(20), nullable=True)
    location = Column(String(150), nullable=True)
    education = Column(Text, nullable=True)
    experience_summary = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    skill_name = Column(String(100), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class CandidateFact(Base):
    __tablename__ = "candidate_facts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    category = Column(String(100), nullable=False)
    fact_text = Column(Text, nullable=False)

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False
    )

    source = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    job_url = Column(String(500), nullable=True)
    job_description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)

    status = Column(
        String(50),
        default="applied",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )

    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)

    changed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class ApplicationArtifact(Base):
    __tablename__ = "application_artifacts"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )

    artifact_type = Column(String(50), nullable=False)
    content_text = Column(Text, nullable=True)
    storage_key = Column(String(500), nullable=True)

    version_number = Column(
        Integer,
        default=1,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class Communication(Base):
    __tablename__ = "communications"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )

    direction = Column(String(20), nullable=False)
    channel = Column(String(50), nullable=False)

    subject = Column(String(255), nullable=True)
    message_content = Column(Text, nullable=False)

    sent_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class ApplicationQuestionAnswer(Base):
    __tablename__ = "application_questions_answers"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)

    answer_verified = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )

    interview_round = Column(String(100), nullable=True)
    interview_date = Column(DateTime(timezone=True), nullable=True)
    interview_type = Column(String(50), nullable=True)
    interviewer_name = Column(String(150), nullable=True)

    questions_asked = Column(Text, nullable=True)
    candidate_responses = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    result = Column(String(50), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )