import openai
import os
from typing import List, Dict, Optional
import numpy as np
from dotenv import load_dotenv
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

EMBEDDING_MODEL = "text-embedding-ada-002"
DEFAULT_LLM_MODEL = "gpt-3.5-turbo"

# You can set LLM_MODEL to "gpt-4o" or "gpt-4-turbo" for better quality/efficiency
LLM_MODEL = os.getenv("LLM_MODEL", DEFAULT_LLM_MODEL)

def get_embedding(text: str) -> List[float]:
    # New OpenAI API v1+ for embeddings
    response = openai.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def find_best_match(clause: str, partner_clauses: List[str], partner_embeddings: List[List[float]]) -> Optional[int]:
    clause_emb = get_embedding(clause)
    similarities = [cosine_similarity(clause_emb, emb) for emb in partner_embeddings]
    if similarities:
        return int(np.argmax(similarities))
    return None

def check_compliance(bank_clause: str, partner_clause: str, llm_model: str = LLM_MODEL) -> Dict:
    system_message = {
        "role": "system",
        "content": (
            "You are a legal compliance assistant. "
            "Given a clause from a bank's Terms of Service (TOS) and a clause from a partner's TOS, "
            "determine if the partner clause complies with the bank clause. "
            "Always respond in JSON format with two fields: 'compliance' (one of 'compliant', 'non-compliant', 'missing') "
            "and 'explanation' (a brief reason for your decision)."
        )
    }
    few_shot_examples = [
        {
            "role": "user",
            "content": (
                "Bank TOS Clause: The borrower must maintain a minimum DSCR of 1.5x.\n"
                "Partner TOS Clause: The borrower must maintain a minimum DSCR of 1.5x.\n"
                "Does the partner clause comply with the bank clause?"
            )
        },
        {
            "role": "assistant",
            "content": '{"compliance": "compliant", "explanation": "The partner clause matches the bank clause exactly."}'
        },
        {
            "role": "user",
            "content": (
                "Bank TOS Clause: The facility must be secured against the company's fixed assets.\n"
                "Partner TOS Clause: The facility is unsecured.\n"
                "Does the partner clause comply with the bank clause?"
            )
        },
        {
            "role": "assistant",
            "content": '{"compliance": "non-compliant", "explanation": "The partner clause does not require security against fixed assets."}'
        }
    ]
    prompt = (
        f"Bank TOS Clause: {bank_clause}\n"
        f"Partner TOS Clause: {partner_clause}\n"
        "Does the partner clause comply with the bank clause?"
    )
    response = openai.chat.completions.create(
        model=llm_model,
        messages=[system_message, *few_shot_examples, {"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0,
        response_format={"type": "json_object"}
    )
    content = response.choices[0].message.content.strip()
    try:
        result = json.loads(content)
    except Exception:
        result = {"compliance": "unknown", "explanation": content}
    return result

def explain_compliance_result(result_json: Dict, llm_model: str = LLM_MODEL) -> str:
    explanation_prompt = (
        f"Given this compliance result in JSON:\n{json.dumps(result_json, indent=2)}\n"
        "Explain the result in plain English for a non-technical user."
    )
    response = openai.chat.completions.create(
        model=llm_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant who explains legal compliance results in simple terms."},
            {"role": "user", "content": explanation_prompt}
        ],
        max_tokens=256,
        temperature=0
    )
    return response.choices[0].message.content.strip()

def compare_clauses_stream(bank_clauses: List[str], partner_clauses: List[str], llm_model: str = LLM_MODEL):
    """
    Generator version: yields each result as soon as it's ready for streaming.
    """
    partner_embeddings = [get_embedding(clause) for clause in partner_clauses]
    for bank_clause in bank_clauses:
        best_idx = find_best_match(bank_clause, partner_clauses, partner_embeddings)
        partner_clause = partner_clauses[best_idx] if best_idx is not None else None
        if partner_clause:
            compliance_result = check_compliance(bank_clause, partner_clause, llm_model=llm_model)
        else:
            compliance_result = {"compliance": "missing", "explanation": "No matching clause found."}
        yield {
            "bank_clause": bank_clause,
            "partner_clause": partner_clause,
            **compliance_result
        }

def compare_clauses(bank_clauses: List[str], partner_clauses: List[str], llm_model: str = LLM_MODEL) -> List[Dict]:
    """
    For each bank clause, find the most similar partner clause (using embeddings),
    then use the LLM to check compliance and explain.
    """
    partner_embeddings = [get_embedding(clause) for clause in partner_clauses]
    results = []
    for bank_clause in bank_clauses:
        best_idx = find_best_match(bank_clause, partner_clauses, partner_embeddings)
        partner_clause = partner_clauses[best_idx] if best_idx is not None else None
        if partner_clause:
            compliance_result = check_compliance(bank_clause, partner_clause, llm_model=llm_model)
        else:
            compliance_result = {"compliance": "missing", "explanation": "No matching clause found."}
        results.append({
            "bank_clause": bank_clause,
            "partner_clause": partner_clause,
            **compliance_result
        })
    return results 