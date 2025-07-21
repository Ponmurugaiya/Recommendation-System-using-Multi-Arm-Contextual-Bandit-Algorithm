# firestore_utils.py
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("Yours_Firestore_Credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# --- User Data ---
def get_user_profile(user_id):
    doc = db.collection("users").document(user_id).get()
    if not doc.exists:
        return None
    user = doc.to_dict()
    return {
        "gender": 1 if user.get("GENDER", "M") == "M" else 0,
        "age_group": int(user.get("AGEGROUP", 15)),
        "average_time": float(user.get("AVERAGETIME", 60)),
        "day_consistent_score": float(user.get("DAYCONSISTENT_SCORE", 0))
    }

# --- Lesson/Item Data ---
def get_lesson_metadata(item_id):
    doc = db.collection("items").document(item_id).get()
    if not doc.exists:
        return None
    item = doc.to_dict()
    type_map = {"listen": 0, "speak": 1, "read": 2, "write": 3}
    one_hot_type = [0, 0, 0, 0]
    one_hot_type[type_map.get(item.get("TYPE", "listen"), 0)] = 1
    return {
        "skill_weightage": float(item.get("SKILL_WEIGHTAGE", 1.0)),
        "class": int(item.get("CLASS", 6)),
        "type_onehot": one_hot_type
    }

# --- User × Item Interaction Stats ---
def get_interaction_stats(user_id, item_id):
    docs = db.collection("interactions") \
        .where("USER_ID", "==", user_id) \
        .where("ITEM_ID", "==", item_id).stream()
    
    total_acc = 0
    total_time = 0
    total_attempts = 0
    total_hint = 0
    total_skip = 0
    total_questions = 0
    count = 0

    for doc in docs:
        d = doc.to_dict()
        count += 1
        total_questions += d.get("NO_OF_QUES", 0)
        total_acc += d.get("CORRECT", 0) / max(1, d.get("NO_OF_QUES", 1))
        total_time += d.get("TIMESPEND", 0)
        total_attempts += d.get("ATTEMPT_COUNT", 1)
        total_hint += d.get("HINT_USED", 0)
        total_skip += d.get("SKIPPED", 0)

    if count == 0:
        return {
            "accuracy": 0,
            "time_spent": 0,
            "attempts": 0,
            "hint_ratio": 0,
            "skip_ratio": 0
        }

    return {
        "accuracy": total_acc / count,
        "time_spent": total_time / count,
        "attempts": total_attempts / count,
        "hint_ratio": total_hint / max(1, total_questions),
        "skip_ratio": total_skip / max(1, total_questions)
    }
def get_all_candidate_lessons():
    lessons = db.collection("items").stream()
    candidate_ids = []
    for doc in lessons:
        candidate_ids.append(doc.id)
    return candidate_ids
