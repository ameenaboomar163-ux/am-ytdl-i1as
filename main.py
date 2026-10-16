from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import yt_dlp
import uvicorn
import os

app = FastAPI(title="Am-YT-Downloader", version="1.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def home():
    return {"status": "online", "message": "API is ready!"}

@app.get("/api/v1/download/ytdl")
def download_youtube(url: str = Query(...), type: str = Query("video")):
    if not url.startswith("http"):
        return JSONResponse(status_code=400, content={"success": False, "error": "Invalid URL"})

    try:
        ydl_opts = {
            'quiet': True, 'no_warnings': True, 'skip_download': True,
            'format': 'best[ext=mp4]' if type == 'video' else 'bestaudio[ext=m4a]'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            direct_url = info.get('url')
            
            if not direct_url: raise ValueError("Direct URL not found")

            return JSONResponse(content={
                "success": True,
                "response": {
                    "title": info.get('title'),
                    "download_url": direct_url,
                    "type": type,
                    "source": "am-ytdl"
                }
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
