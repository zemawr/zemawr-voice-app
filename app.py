import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from TTS.api import TTS

app = FastAPI(title="Zemawr Independent Voice Engine")

# Initialize and download the premium open-source voice model
print("Loading hyper-realistic voice weights onto your M1 Mac...")
# We use the XTTS v2 model because it natively supports ultra-realistic emotional pacing
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

class AdScriptRequest(BaseModel):
    text: str
    speaker: str = "Anais Takahara" # A high-quality built-in professional voice option

@app.post("/v1/generate-ad-speech")
async def generate_speech(request: AdScriptRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Script text cannot be blank.")
        
    output_filename = "free_local_ad.mp3"
    
    try:
        # Run the voice generation entirely inside your own ecosystem
        tts.tts_to_file(
            text=request.text,
            file_path=output_filename,
            speaker=request.speaker,
            language="en"
        )
        return FileResponse(output_filename, media_type="audio/mpeg")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
