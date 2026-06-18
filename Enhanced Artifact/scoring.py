def calculate_suitability_score(dog, preferred_breeds, min_age, max_age,
                                preferred_sex, breed_weight, age_weight, sex_weight):
    """Calculate a rescue suitability score for one dog."""
    score = 0

    breed = str(dog.get("breed", ""))
    age = dog.get("age_upon_outcome_in_weeks", 0)
    sex = str(dog.get("sex_upon_outcome", ""))

    if preferred_breeds and breed in preferred_breeds:
        score += breed_weight

    if min_age <= age <= max_age:
        score += age_weight

    if preferred_sex and sex == preferred_sex:
        score += sex_weight

    return score


def rank_dogs_by_suitability(records, preferred_breeds, min_age, max_age,
                             preferred_sex, breed_weight, age_weight, sex_weight):
    """Score and sort dogs from most suitable to least suitable."""
    ranked_records = []

    for dog in records:
        dog_copy = dog.copy()
        dog_copy["suitability_score"] = calculate_suitability_score(
            dog_copy,
            preferred_breeds,
            min_age,
            max_age,
            preferred_sex,
            breed_weight,
            age_weight,
            sex_weight
        )
        ranked_records.append(dog_copy)

    ranked_records.sort(
        key=lambda dog: dog["suitability_score"],
        reverse=True
    )

    return ranked_records