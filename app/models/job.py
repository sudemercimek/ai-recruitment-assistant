from pydantic import BaseModel, Field


class JobDescription(BaseModel):
    title: str
    description: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    min_experience_years: float = 0.0

    