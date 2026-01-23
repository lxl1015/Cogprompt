import json
import pandas as pd
from pathlib import Path
from .config import DATA_DIR, NUM_CONCEPTS

def load_student_proficiency(fp: Path = DATA_DIR / "student_proficiency.csv") -> pd.DataFrame:
    df = pd.read_csv(fp)
    rename_map = {f"k{i}": f"c{i}" for i in range(1, NUM_CONCEPTS + 1)}
    df.rename(columns=rename_map, inplace=True)
    return df 

def load_exercise_params(fp: Path = DATA_DIR / "exercise_params.csv") -> pd.DataFrame:
    df = pd.read_csv(fp)
    df["discrimination"] = df["discrimination"].astype(str).str.replace("[", "", regex=False)\
                                                     .str.replace("]", "", regex=False).astype(float)
    rename_map = {f"k{i}": f"c{i}" for i in range(1, NUM_CONCEPTS + 1)}
    df.rename(columns=rename_map, inplace=True)
    return df

def load_responses(fp: Path = DATA_DIR / "linux_user_problem.json"):
    records = []
    with open(fp, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)
                records.append(obj)
    return records

def load_questions(fp: Path = DATA_DIR / "questions.json"):
    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f)
