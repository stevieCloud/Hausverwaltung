from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from ..services.claude_client import call_claude, build_parser_prompt

router = APIRouter(prefix="/admin/claude", tags=["claude"])

class TuneRequest(BaseModel):
    example_rows: str
    model: str | None = None
    max_tokens: int | None = 800

@router.post("/tune")
async def tune_parser(req: TuneRequest, background_tasks: BackgroundTasks):
    prompt = build_parser_prompt(req.example_rows)
    model = req.model or None
    try:
        # run in background to avoid blocking long calls
        result = await call_claude(prompt, model=model or None, max_tokens=req.max_tokens or 800)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # result contains raw Claude response; in next step we will parse and store rules
    return {"status": "ok", "raw": result}
