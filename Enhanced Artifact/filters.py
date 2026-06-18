def get_rescue_query(filter_type):
    """Return MongoDB query based on selected rescue type."""

    if filter_type == "Water Rescue":
        return {
            "$and": [
                {"breed": {"$in": [
                    "Labrador Retriever Mix",
                    "Chesapeake Bay Retriever",
                    "Newfoundland"
                ]}},
                {"sex_upon_outcome": "Intact Female"},
                {"age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}}
            ]
        }

    if filter_type == "Mountain or Wilderness Rescue":
        return {
            "$and": [
                {"breed": {"$in": [
                    "German Shepherd",
                    "Alaskan Malamute",
                    "Old English Sheepdog",
                    "Siberian Husky",
                    "Rottweiler"
                ]}},
                {"sex_upon_outcome": "Intact Male"},
                {"age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}}
            ]
        }

    if filter_type == "Disaster or Individual Tracking":
        return {
            "$and": [
                {"breed": {"$in": [
                    "Doberman Pinscher",
                    "German Shepherd",
                    "Golden Retriever",
                    "Bloodhound",
                    "Rottweiler"
                ]}},
                {"sex_upon_outcome": "Intact Male"},
                {"age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}}
            ]
        }

    return {}