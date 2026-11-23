from app.services.candidate_loader import load_candidates

candidates = load_candidates("data/candidates.json")

for candidate in candidates:
    print(candidate.full_name)
    print(candidate.skills)
    print(candidate.experience_years)