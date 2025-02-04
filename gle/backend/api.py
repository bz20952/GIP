from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

import filter as f

# Initialise API
app = FastAPI()

# Allow cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Serve images from the images folder
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/dft')
async def dft():
    return {"message": "This should return either a graph or frequency content raw data."}


@app.get('/time-domain')
async def time_domain():
    return {"message": "This should return either a graph of acceleration data."}


@app.get('/raw-data')
async def raw_data():
    return {"message": "This should return raw data."}


@app.get('/filter')
async def filter(request: Request):
    options = await request.json()

    if options['filterType'] == 'bandpass':
        b, a = f.bandpass(options['lowerCutoff'], options['upperCutoff'], options['samplingFreq'])
    elif options['filterType'] == 'lowpass':
        b, a = f.lowpass(options['lowerCutoff'], options['samplingFreq'])
    elif options['filterType'] == 'highpass':
        b, a = f.highpass(options['upperCutoff'], options['samplingFreq'])

    return {"message": "This should return a filtered graph."}


if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True)