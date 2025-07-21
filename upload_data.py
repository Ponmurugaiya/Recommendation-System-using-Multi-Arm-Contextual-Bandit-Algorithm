from utils.firestore import db
from datetime import datetime
import random

#Sample Users
users = [
    {"user_id": "user_001", "gender": "male", "agegroup": "13-15", "averagetime": 80, "dayconsistent_score": 5},
    {"user_id": "user_002", "gender": "female", "agegroup": "10-12", "averagetime": 60, "dayconsistent_score": 7}
]

#Sample Lessons (Items)
items = [
    {"item_id": "listen_101", "type": "listening", "skill": "listen", "skill_weightage": 0.3, "class": "6"},
    {"item_id": "read_203", "type": "reading", "skill": "read", "skill_weightage": 0.25, "class": "6"},
    {"item_id": "write_305", "type": "writing", "skill": "write", "skill_weightage": 0.25, "class": "7"},
    {"item_id": "speak_404", "type": "speaking", "skill": "speak", "skill_weightage": 0.2, "class": "7"}
]

#Sample Interactions
interactions = [
    {
        "user_id": "user_001",
        "item_id": "listen_101",
        "event_type": "completed",
        "timestamp": datetime.now(),
        "session_id": "sess_001",
        "attempt_count": 1,
        "status": "completed",
        "no_of_ques": 5,
        "correct": 4,
        "wrong": 1,
        "skipped": 0,
        "hint_used": 1,
        "timespend": 85
    },
    {
        "user_id": "user_002",
        "item_id": "write_305",
        "event_type": "started",
        "timestamp": datetime.now(),
        "session_id": "sess_002",
        "attempt_count": 2,
        "status": "in_progress",
        "no_of_ques": 4,
        "correct": 2,
        "wrong": 1,
        "skipped": 1,
        "hint_used": 0,
        "timespend": 70
    }
]

def upload_data():
    # Upload Users
    for u in users:
        db.collection("users").document(u["user_id"]).set(u)
    print("✅ Users uploaded")

    # Upload Items (Lessons)
    for item in items:
        db.collection("items").document(item["item_id"]).set(item)
    print("✅ Items uploaded")

    # Upload Interactions
    for i in interactions:
        db.collection("interactions").add(i)
    print("✅ Interactions uploaded")

if __name__ == "__main__":
    upload_data()
