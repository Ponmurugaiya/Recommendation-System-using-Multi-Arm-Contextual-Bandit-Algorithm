# linucb.py

import numpy as np
from collections import defaultdict

class LinUCB:
    def __init__(self, alpha=0.3, context_dim=15):
        self.alpha = alpha
        self.d = context_dim
        self.A = defaultdict(lambda: np.identity(self.d))
        self.b = defaultdict(lambda: np.zeros((self.d, 1)))

    def recommend(self, user_context, candidate_items):
        """
        Args:
            user_context: dict of {lesson_id: context_vector}
            candidate_items: list of lesson_ids

        Returns:
            lesson_id with highest Upper Confidence Bound(UCB) score
        """
        best_score = -float('inf')
        best_lesson = None

        for lesson_id in candidate_items:
            x = np.array(user_context[lesson_id]).reshape(-1, 1)
            A_inv = np.linalg.inv(self.A[lesson_id])
            theta = A_inv @ self.b[lesson_id]
            p = float((theta.T @ x) + self.alpha * np.sqrt((x.T @ A_inv @ x)))
            
            if p > best_score:
                best_score = p
                best_lesson = lesson_id

        return best_lesson

    def update(self, lesson_id, context_vector, reward):
        x = np.array(context_vector).reshape(-1, 1)
        self.A[lesson_id] += x @ x.T
        self.b[lesson_id] += reward * x
