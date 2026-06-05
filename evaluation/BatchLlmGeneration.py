import json
import requests
from pathlib import Path

# ----- Configuration -----
MODEL = "llama3.1:8b"  # Ollama model name
SYSTEM_ROLE = """
You are an excellent intelligent learning mentor. You can integrate the cognitive map with the students' current mastery level,
explain and reason about the students' questions, and provide structured learning feedback.
It is particularly important to pay attention to the students' mastery level information. Generally, a mastery level of 0.5 indicates an average level. You should teach according to the students' mastery level,
such as providing more basic content when the mastery level is low and advanced content when it is high.
"""

OUTPUT_FORMAT = """
Please answer the question based on the above information. Your answer should:
- Be a conclusion (concentrate on the student's question)
- Be tailored to the student's level (ensure the answer is understandable to the student)

"""

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def build_prompt(item):
    q = item["question"]
    p = item["cogprompt"]
    return f"""{SYSTEM_ROLE}

[Q]The question raised by the students is：
{q}

[P]This is the relevant information extracted from the students' cognitive maps.：
{p}

[Output Format]
{OUTPUT_FORMAT}"""


def run_ollama(prompt: str, max_tokens: int = 2048) -> str:
    """Call Ollama via HTTP API with controlled output length."""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "system": "",
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": 0.3,
        }
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Ollama API error: {response.text}")
    result = response.json()
    return result.get("response", "")


# ----- Batch Processing -----
INPUT_FILE = Path("all_prompts.json")
OUTPUT_FILE = Path("output_llm.json")


if __name__ == "__main__":
    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    total = len(data)

    # Check Ollama service
    try:
        requests.get("http://localhost:11434")
    except Exception:
        print("❌ Please start the Ollama service first: ollama serve")
        exit(1)

    results = []

    for idx, item in enumerate(data, 1):
        sid = item.get("student_id")
        q_text = item.get("question", "")
        print(f"[{idx}/{total}] Processing student {sid} ...")

        prompt = build_prompt(item)
        raw_output = run_ollama(prompt, max_tokens=4000)

        results.append({
            "student_id": sid,
            "question": q_text,
            "answer": raw_output.strip()
        })

    OUTPUT_FILE.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"✅ Done. JSON has been saved to {OUTPUT_FILE}")
