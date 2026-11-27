
from app.services.candidate_loader import load_candidates
from app.services.candidate_scoring import rank_candidates
from data.sample_job import junior_ai_engineer_job


def main():
    # Load candidates from JSON
    candidates = load_candidates("data/candidates.json")

    # Rank all candidates
    ranked_candidates = rank_candidates(
        candidates,
        junior_ai_engineer_job
    )

    # Display all candidates
    print("\n--- ALL CANDIDATES ---")

    for index, candidate in enumerate(ranked_candidates, start=1):
        print(
            f"{index}. {candidate['full_name']} "
            f"- Score: {candidate['total_score']}"
        )

    # Select top 5 candidates
    shortlist = ranked_candidates[:5]

    print("\n--- TOP 5 SHORTLIST ---")

    for index, candidate in enumerate(shortlist, start=1):
        print(f"\n{index}. {candidate['full_name']}")
        print(f"Total Score: {candidate['total_score']}")
        print(f"Score Breakdown: {candidate['score_breakdown']}")
        print(f"Evidence: {candidate['evidence']}")


if __name__ == "__main__":
    main()
