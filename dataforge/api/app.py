import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routes.focus_group import router as focus_group_router
from .routes.generator import router as generator_router
from .routes.radar import router as radar_router
from .routes.census import router as census_router
from .routes.counterfactual import router as counterfactual_router
from .routes.society import router as society_router
from .. import __version__

app = FastAPI(
    title="DataForge API",
    description=(
        "🔬 **DataForge Enterprise API**: Türkiye'nin Hesaplamalı Sosyal Bilimler, "
        "Bilişsel Dijital İkiz ve Sentetik Odak Grubu Simülasyon Motoru."
    ),
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for Next.js / React Frontend Dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static directory setup
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# API v1 Router Registration
app.include_router(focus_group_router, prefix="/api/v1")
app.include_router(census_router, prefix="/api/v1")
app.include_router(generator_router, prefix="/api/v1")
app.include_router(radar_router, prefix="/api/v1")
app.include_router(counterfactual_router, prefix="/api/v1")
app.include_router(society_router, prefix="/api/v1")


@app.get("/", tags=["Studio Web Interface"])
async def studio_ui():
    """Serves the bespoke handcrafted DataForge Studio interface."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "service": "DataForge Cognitive Engine",
        "version": __version__,
        "docs": "/docs"
    }


@app.get("/health", tags=["Health & Info"])
async def health():
    return {"status": "ok", "version": __version__}
