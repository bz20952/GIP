from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from dotenv import load_dotenv
import os
import filter as f
import reader as r
import plotter as p


# Define root URL
root_url = f"http://{os.environ.get('PUBLIC_HOSTNAME')}:{os.environ.get('PUBLIC_BACKEND_PORT')}"

# Initialise API
app = FastAPI()

# Allow cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", f"http://{os.environ.get('PUBLIC_HOSTNAME')}:{os.environ.get('FRONTEND_PORT')}"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Serve images from the images folder
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
async def root():
    return {
        "details": "This is the API root.",
        "message": "Hello world!",
        "success": True,
        "error": False,
        "code": 200,
    }


@app.post("/run-test")
async def run_test(request: Request):
    options = await request.json()
    data = r.read_csv(options)
    p.plot_acceleration(data, options)

    return {
        "details": "This endpoint generates all required plots based on user input during Test Setup.",
        "message": "Plots generated.",
        "success": True,
        "error": False,
        "code": 200,
    }


@app.get('/time-domain')
async def time_domain():
    return {
        "details": "This should return either a graph of acceleration data.",
        "message": f"{root_url}/images/random.gif",
        "success": True,
        "error": False,
        "code": 200
    }


@app.get('/forcing')
async def forcing():
    return {
        "details": "This should the path to a forcing signal gif/plot.",
        "message": f"{root_url}/images/random.gif",
        "success": True,
        "error": False,
        "code": 200
    }


@app.get('/animate')
async def animate():
    return {
        "details": "This should the path to a forcing signal gif/plot.",
        "message": f"{root_url}/images/random.gif",
        "success": True,
        "error": False,
        "code": 200
    }


@app.get('/dft')
async def dft():
    return {
        "details": "This should return the path to the DFT plot.",
        "message": "",
        "success": True,
        "error": False,
        "code": 200
    }


@app.get('/frf-gain')
async def frf_gain():
    return {
        "details": "This should return the path to the FRF gain plot.",
        "message": "",
        "success": True,
        "error": False,
        "code": 200
    }


@app.get('/frf-phase')
async def frf_phase():
    return {
        "details": "This should return the path to the FRF phase plot.",
        "message": "",
        "success": True,
        "error": False,
        "code": 200
    }


@app.get('/bode')
async def bode():
    return {
        "details": "This should return the path to the Bode plot.",
        "message": "",
        "success": True,
        "error": False,
        "code": 200
    }


@app.get('/nyquist')
async def nyquist():
    return {
        "details": "This should return the path to the Nyquist plot.",
        "message": "",
        "success": True,
        "error": False,
        "code": 200
    }


# @app.get('/raw-data')
# async def raw_data():
#     return {"message": "This should return raw data."}


@app.get('/filter')
async def filter(request: Request):
    options = await request.json()

    if options['filterType'] == 'bandpass':
        b, a = f.bandpass(options['lowerCutoff'], options['upperCutoff'], options['samplingFreq'])
    elif options['filterType'] == 'lowpass':
        b, a = f.lowpass(options['lowerCutoff'], options['samplingFreq'])
    elif options['filterType'] == 'highpass':
        b, a = f.highpass(options['upperCutoff'], options['samplingFreq'])

    return {
        "details": "This should return a filtered graph.",
        "message": "",
        "success": True,
        "error": False,
        "code": 200
    }


if __name__ == "__main__":
    if os.environ.get('ENV') == 'docker':
        uvicorn.run("api:app", host='0.0.0.0', port=int(os.environ.get('PUBLIC_BACKEND_PORT')), workers=4)
    else:
        load_dotenv('../.env')
        uvicorn.run("api:app", port=int(os.environ.get('PUBLIC_BACKEND_PORT')), reload=True)