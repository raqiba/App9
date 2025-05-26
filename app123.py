import random
from typing import List, Dict

# Stub for Gemini or any LLM
class LLMClient:
    def __init__(self):
        pass

    def generate_questions(self, job_role: str, job_description: str, difficulty_level: str) -> List[str]:
        # Placeholder: Replace with actual Gemini API logic
        return [f"Mock question {i+1} for {job_role} ({difficulty_level})" for i in range(10)]

    def evaluate_answer(self, question: str, answer: str) -> Dict:
        # Placeholder evaluation logic (randomized)
        rating = random.randint(1, 5)
        feedback = "Good answer." if rating >= 3 else "Needs improvement."
        return {
            "rating": rating,
            "feedback": feedback
        }


class Question:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.user_answer = ""
        self.rating = 0
        self.feedback = ""

    def answer(self, answer_text: str):
        self.user_answer = answer_text

    def evaluate(self, evaluator: LLMClient):
        result = evaluator.evaluate_answer(self.prompt, self.user_answer)
        self.rating = result["rating"]
        self.feedback = result["feedback"]


class InterviewSession:
    def __init__(self, job_role: str, job_description: str, difficulty_level: str):
        self.job_role = job_role
        self.job_description = job_description
        self.difficulty_level = difficulty_level
        self.questions: List[Question] = []
        self.llm_client = LLMClient()

    def start_interview(self):
        question_prompts = self.llm_client.generate_questions(
            self.job_role, self.job_description, self.difficulty_level
        )
        self.questions = [Question(prompt) for prompt in question_prompts]

    def conduct_interview(self):
        for idx, question in enumerate(self.questions, 1):
            print(f"\nQ{idx}: {question.prompt}")
            # In real app, replace with frontend input or API call
            answer = input("Your Answer: ")
            question.answer(answer)
            question.evaluate(self.llm_client)
            print(f"Rating: {question.rating}/5")
            print(f"Feedback: {question.feedback}")

    def get_summary(self) -> Dict:
        total_score = sum(q.rating for q in self.questions)
        avg_score = total_score / len(self.questions)
        return {
            "average_score": avg_score,
            "total_score": total_score,
            "question_stats": [
                {
                    "question": q.prompt,
                    "rating": q.rating,
                    "feedback": q.feedback
                } for q in self.questions
            ]
        }

    def print_summary(self):
        summary = self.get_summary()
        print("\n=== Interview Summary ===")
        print(f"Total Score: {summary['total_score']}/50")
        print(f"Average Rating: {summary['average_score']:.2f}/5")
        for idx, q_stat in enumerate(summary["question_stats"], 1):
            print(f"\nQ{idx}: {q_stat['question']}")
            print(f" - Rating: {q_stat['rating']}")
            print(f" - Feedback: {q_stat['feedback']}")
