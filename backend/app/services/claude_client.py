import os
import httpx
from typing import Any, Dict

CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
# Adjust API URL/model to your Claude provider/version
CLAUDE_API_URL = os.environ.get("CLAUDE_API_URL", "https://api.anthropic.com/v1/complete")
DEFAULT_MODEL = os.environ.get("CLAUDE_MODEL", "claude-2.1")

async def call_claude(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 1000) -> Dict[str, Any]:
    if not CLAUDE_API_KEY:
        raise RuntimeError("CLAUDE_API_KEY not configured in environment")
    headers = {
        "Authorization": f"Bearer {CLAUDE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens,
    }
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(CLAUDE_API_URL, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()

# Example helper to build a parser prompt
def build_parser_prompt(example_rows: str) -> str:
    prompt = (
        "You are a helpful data extraction assistant. Extract structured fields from the following bank transactions:\n"
        "Provide output as JSON array of {date, amount, currency, description, suggested_project, suggested_category}.\n\n"
        f"Transactions:\n{example_rows}\n\nReturn only JSON."
    )
    return prompt
