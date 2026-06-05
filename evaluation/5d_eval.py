import json
import requests
import os

EVAL_PROMPT_TEMPLATE = """
You are an excellent expert in evaluating teaching quality. 
Please rate the "AI teacher's responses" on the following 5 dimensions from 1 to 5 (1 = very poor, 5 = excellent). 
Please provide the JSON output strictly following the rating criteria.

【5D Dimension Definition】

1. Accuracy
- Did the answer correctly address the student's question?
- Was it closely related to the question and did it not stray off-topic?
- Was the explanation clear and did the concepts used make sense?

2. Personalization
- Does the explanation cater to the student's existing knowledge, proficiency level, and background?
- Does it offer a more understandable approach "for this particular student"?
- *Note: You will see an eval_prompt which contains information about the student's proficiency and relevant details; please rate based on this information. *

3. Pedagogy
- Does it provide a structured explanation? (In steps, in layers, in a progressive manner)
- Does it reflect the logical structure of the subject matter?
- Does it employ teaching strategies such as analogies, examples, and comparisons to aid understanding?

4. Engagement
- Does the response encourage students to reflect on or review their understanding?
- Are there any actionable learning suggestions provided for the next step?
- Does it inspire students to have a greater motivation to continue learning?

5. Supportiveness
- Is the tone positive, encouraging and respectful?
- Does it reduce students' anxiety and boost their confidence in learning?

-----------------------------------------

【Student-related personalized information (for Personalization)】
{eval_prompt}

-----------------------------------------

【AI Teacher Response (Needs Evaluation)】
{answer}

-----------------------------------------

Please output JSON in the following format (must be strictly followed).：
{{
"Accuracy": Rating (1-5 numbers),
"Personalization": Rating (1-5 numbers),
"Pedagogy": Rating (1-5 numbers),
"Engagement": Rating (1-5 numbers),
"Supportiveness": Rating (1-5 numbers),
"Comments": "Your overall evaluation, including a brief reason" 
}}
"""



def call_ollama(prompt):
    """Invoke Ollama phi4:14b"""
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "phi4:14b",
        "prompt": prompt,
        "stream": False
    }

    resp = requests.post(url, json=payload)
    data = resp.json()
    return data.get("response", "")


def build_eval_prompt(eval_prompt, answer):
    return EVAL_PROMPT_TEMPLATE.format(
        eval_prompt=eval_prompt,
        answer=answer
    )


def process_evaluation(answer_file, prompt_file, output_path):
    with open(answer_file, "r", encoding="utf-8") as f:
        answers = json.load(f)

    with open(prompt_file, "r", encoding="utf-8") as f:
        all_prompts = json.load(f)

    eval_map = {
        entry["student_id"]: entry.get("eval_prompt", "")
        for entry in all_prompts
    }

    results = []

    for item in answers:
        sid = item["student_id"]
        answer = item["answer"]

        print(f"\nThe responses of student {sid} are currently being evaluated....")

        eval_prompt = eval_map.get(sid, "（No personalized information）")

        prompt = EVAL_PROMPT_TEMPLATE.format(
            eval_prompt=eval_prompt,
            answer=answer
        )

        score_str = call_ollama(prompt)

        results.append({
            "student_id": sid,
            "question": item["question"],
            "answer": answer,
            "eval_prompt": eval_prompt,
            "evaluation": score_str.strip()
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nThe assessment results have been saved to：{output_path}")



if __name__ == "__main__":
    process_evaluation(
        answer_file="output_llm.jsonl",
        prompt_file="all_prompts.json",
        output_path="5d_eval.json"
    )
