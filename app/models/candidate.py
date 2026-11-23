from email.policy import default

from pydantic import BaseModel, Field

class CandidateProfile(BaseModel):
    full_name: str
    email: str | None = None
    skills: list[str] = Field(default_factory=list)
    experience_years: float = 0.0
    education: str | None = None
    projects: list[str] = Field(default_factory=list)
    summary: str = ""
