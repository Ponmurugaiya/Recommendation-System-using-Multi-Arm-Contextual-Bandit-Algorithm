# context_vector.py

from utils.firestore import get_user_profile, get_lesson_metadata, get_interaction_stats

def build_context_vector(user_id, lesson_id):
    user = get_user_profile(user_id)
    item = get_lesson_metadata(lesson_id)
    interaction = get_interaction_stats(user_id, lesson_id)

    if user is None or item is None:
        raise ValueError("User or Item not found in database")

    context_vector = [
        # --- User ---
        user["gender"],
        user["age_group"],
        user["average_time"],
        user["day_consistent_score"],

        # --- Item ---
        *item["type_onehot"],  # 4 one-hot values
        item["skill_weightage"],
        item["class"],

        # --- Interaction ---
        interaction["accuracy"],
        interaction["time_spent"],
        interaction["attempts"],
        interaction["hint_ratio"],
        interaction["skip_ratio"]
    ]

    return context_vector
