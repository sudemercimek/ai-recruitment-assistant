
from app.models.candidate import CandidateProfile
from app.models.job import JobDescription


# Scoring weights
REQUIRED_SKILLS_WEIGHT = 60
EXPERIENCE_WEIGHT = 25
PREFERRED_SKILLS_WEIGHT = 15

MAX_EXPERIENCE_YEARS = 2


def match_skills(
    required_skills: list[str],
    candidate_skills: list[str]
) -> list[str]:
    candidate_skills_set = {
        skill.strip().casefold()
        for skill in candidate_skills
    }

    matched_skills = [
        skill
        for skill in required_skills
        if skill.strip().casefold() in candidate_skills_set
    ]

    return matched_skills


def calculate_skill_score(
    matched_skills: list[str],
    total_skills: int,
    weight: int
) -> float:
    if total_skills == 0:
        return 0.0

    return (len(matched_skills) / total_skills) * weight


def calculate_experience_score(
    experience_years: float
) -> float:
    experience_years = max(experience_years, 0.0)

    if experience_years >= MAX_EXPERIENCE_YEARS:
        return float(EXPERIENCE_WEIGHT)

    return (
        experience_years / MAX_EXPERIENCE_YEARS
    ) * EXPERIENCE_WEIGHT


def score_candidate(
    candidate: CandidateProfile,
    job: JobDescription
) -> dict:

    # Required skills
    matched_required = match_skills(
        job.required_skills,
        candidate.skills
    )

    required_score = calculate_skill_score(
        matched_required,
        len(job.required_skills),
        REQUIRED_SKILLS_WEIGHT
    )

    # Preferred skills
    matched_preferred = match_skills(
        job.preferred_skills,
        candidate.skills
    )

    preferred_score = calculate_skill_score(
        matched_preferred,
        len(job.preferred_skills),
        PREFERRED_SKILLS_WEIGHT
    )

    # Experience
    experience_score = calculate_experience_score(
        candidate.experience_years
    )

    # Total score
    total_score = (
        required_score
        + experience_score
        + preferred_score
    )

    return {
        "full_name": candidate.full_name,
        "total_score": round(total_score, 2),

        "score_breakdown": {
            "required_skills": round(required_score, 2),
            "experience": round(experience_score, 2),
            "preferred_skills": round(preferred_score, 2)
        },

        "evidence": {
            "matched_required_skills": matched_required,
            "not_listed_required_skills": [
                skill for skill in job.required_skills
                if skill.strip().casefold()
                not in {
                    item.strip().casefold()
                    for item in matched_required
                }
            ],
            "matched_preferred_skills": matched_preferred,
            "not_listed_preferred_skills": [
                skill for skill in job.preferred_skills
                if skill.strip().casefold()
                not in {
                    item.strip().casefold()
                    for item in matched_preferred
                }
            ],
            "reported_experience_years": candidate.experience_years
        }
    }

def rank_candidates(
    candidates: list[CandidateProfile],
    job: JobDescription
) -> list[dict]:

    scored_candidates = [
        score_candidate(candidate, job)
        for candidate in candidates
    ]

    ranked_candidates = sorted(
        scored_candidates,
        key=lambda candidate: candidate["total_score"],
        reverse=True
    )

    return ranked_candidates