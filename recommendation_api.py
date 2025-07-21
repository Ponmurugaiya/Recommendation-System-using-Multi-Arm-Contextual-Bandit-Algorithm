# recommendation_api.py

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from linucb import LinUCB
from context_vector import build_context_vector
from utils.firestore import get_all_candidate_lessons
import random

app = FastAPI()
model = LinUCB(alpha=0.4)

motivations = [
    "Every small step builds consistency!",
    "You're doing amazing. Keep going!",
    "Push your limits, not your patience.",
    "Today’s effort becomes tomorrow’s strength.",
    "Stay consistent, and mastery will follow!"
]

class RecommendRequest(BaseModel):
    user_id: str
    candidate_lessons: Optional[List[str]] = None

@app.post("/recommend")
def recommend_lesson(req: RecommendRequest):
    user_id = req.user_id

    # 1. Get candidate lessons
    candidate_lessons = req.candidate_lessons or get_all_candidate_lessons()


    # 2. Build context vectors
    context_dict = {}
    for lid in candidate_lessons:
        context = build_context_vector(user_id, lid)
        if context:
            context_dict[lid] = context

    if not context_dict:
        return {"error": "No valid lessons found."}

    # 3. Recommend lesson
    recommended = model.recommend(context_dict, list(context_dict.keys()))
    
    # 4. Explanation
    reason = generate_reason(context_dict[recommended])
    motivation = random.choice(motivations)

    return {
        "recommended_lesson": recommended,
        "reason": reason,
        "motivational_message": motivation
    }

def generate_reason(context):
    streak, xp, acc, time_spent, attempts, *_ = context
    if acc < 0.6:
        return "You’ve struggled with similar topics. Let’s strengthen that!"
    elif time_spent < 30:
        return "This topic usually takes less time. A quick win!"
    elif streak >= 3:
        return "Let’s maintain your streak with this lesson!"
    elif attempts > 2:
        return "You’re persistent! This lesson rewards that."
    else:
        return "This fits your current progress and skill focus!"
