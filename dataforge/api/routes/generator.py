"""
DataForge Synthetic Persona Generation REST API Route.
"""
from __future__ import annotations

import time
from fastapi import APIRouter, HTTPException, status
from ..schemas import GenerateRequest, GenerateResponse
from ...ml.prompt_synthesizer import DynamicPromptEngine

router = APIRouter(prefix="/generate", tags=["Synthetic Generation"])


@router.post(
    "",
    response_model=GenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="Sentetik İnsan ve Dijital İkiz Üret",
    description="Doğal dil istemine göre (örn: 'Kadıköy esnafı') TCKN ve UAVT adresleriyle nedensel tutarlı sentetik nüfus üretir."
)
async def generate_synthetic_data(req: GenerateRequest):
    try:
        start_time = time.time()
        engine = DynamicPromptEngine()
        personas = engine.synthesize(req.prompt, count=req.count)
        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return GenerateResponse(
            count=len(personas),
            data=personas,
            execution_time_ms=elapsed_ms
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Synthetic generation failed: {str(e)}"
        )
