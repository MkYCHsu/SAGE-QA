#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from config import SAGEConfig
from app import SAGEQAApp


class QARequest(BaseModel):
    question: str


class QAResponse(BaseModel):
    answer: str


def build_fastapi(app_runtime: SAGEQAApp) -> FastAPI:
    api = FastAPI(title="SAGE-QA")

    @api.on_event("startup")
    def _startup():
        app_runtime.setup()

    @api.get("/health")
    def health():
        return {"status": "ok", "ready": app_runtime.ready}

    @api.post("/qa", response_model=QAResponse)
    def qa(req: QARequest):
        result = app_runtime.ask(req.question, output_name="api")
        return QAResponse(answer=str(result))

    return api


def parse_args():
    p = argparse.ArgumentParser(description="Serve SAGE-QA as a FastAPI server.")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--base-url", default=None)
    p.add_argument("--model", default=None)
    p.add_argument("--api-key", default=None)
    p.add_argument("--data-dir", default=None)
    p.add_argument("--data-dir-out", default=None)
    p.add_argument("--embedding-model-path", default=None)
    p.add_argument("--chroma-dir", default=None)
    p.add_argument("--rebuild-embeddings", action="store_true")
    p.add_argument("--rebuild-chroma", action="store_true")
    p.add_argument("--debug", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = SAGEConfig.from_env()
    if args.base_url is not None:
        cfg.base_url = args.base_url
    if args.model is not None:
        cfg.model = args.model
    if args.api_key is not None:
        cfg.api_key = args.api_key
    if args.data_dir is not None:
        cfg.data_dir = Path(args.data_dir)
    if args.data_dir_out is not None:
        cfg.data_dir_out = Path(args.data_dir_out)
    if args.embedding_model_path is not None:
        cfg.embedding_model_path = Path(args.embedding_model_path)
    if args.chroma_dir is not None:
        cfg.chroma_dir = Path(args.chroma_dir)
    if args.rebuild_embeddings:
        cfg.rebuild_embeddings = True
    if args.rebuild_chroma:
        cfg.rebuild_chroma = True
    if args.debug:
        cfg.debug = True

    runtime = SAGEQAApp(cfg)
    api = build_fastapi(runtime)
    uvicorn.run(api, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
