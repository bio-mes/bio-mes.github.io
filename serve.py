"""Standalone server for the BioMes project homepage.

Serves the static files in this directory (index.html, styles.css, script.js,
favicon.ico, assets/) on their own process/port, independent of the
agentFlow_web_online_biology chat application.

Run:
    python3 serve.py                  # http://0.0.0.0:10001
    python3 serve.py --port 8090
"""
import argparse
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="BioMes Homepage", docs_url=None, redoc_url=None)
app.add_middleware(GZipMiddleware, minimum_size=1024)

# StaticFiles sends ETag/Last-Modified automatically, so browsers revalidate
# images via cheap 304s without needing an explicit max-age policy here.
app.mount("/assets", StaticFiles(directory=BASE_DIR / "assets"), name="assets")


@app.get("/")
async def index():
    return FileResponse(BASE_DIR / "index.html", headers={"Cache-Control": "no-cache"})


@app.get("/styles.css")
async def styles():
    return FileResponse(BASE_DIR / "styles.css", media_type="text/css", headers={"Cache-Control": "no-cache"})


@app.get("/script.js")
async def script():
    return FileResponse(BASE_DIR / "script.js", media_type="application/javascript", headers={"Cache-Control": "no-cache"})


@app.get("/favicon.ico")
async def favicon():
    return FileResponse(BASE_DIR / "favicon.ico", media_type="image/x-icon", headers={"Cache-Control": "public, max-age=86400"})


def main():
    parser = argparse.ArgumentParser(description="Serve the BioMes project homepage.")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=10001)
    args = parser.parse_args()
    print(f"BioMes homepage: http://{args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
