class RewardEngine:
    """
    Combines evaluator score and user feedback
    to produce final RL reward.
    """

    def compute_reward(self, evaluation_score, user_rating=None):

        feedback_score = 0

        if user_rating is not None:

            # rating is +1 or -1
            feedback_score = user_rating * 0.2

        reward = evaluation_score + feedback_score

        return reward