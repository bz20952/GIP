from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import filter as f

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

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

    if options['filter_type'] == 'bandpass':
        b, a = f.bandpass(options['lower_cutoff'], options['upper_cutoff'], options['sampling_freq'])
    elif options['filter_type'] == 'lowpass':
        b, a = f.lowpass(options['lower_cutoff'], options['sampling_freq'])
    elif options['filter_type'] == 'highpass':
        b, a = f.highpass(options['upper_cutoff'], options['sampling_freq'])

    return {"message": "This should return a filtered graph."}