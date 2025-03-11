from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from dotenv import load_dotenv
import os
import json
import filter as f
import reader as r
import plotter as p
import animate as a
import utils as u


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
    p.plot_forcing(data, options)
    a.animate_beam(u.accel_to_disp(data, options), options)

    return {
        "details": "This endpoint generates all required plots based on user input during Test Setup.",
        "message": "Plots generated.",
        "success": True,
        "error": False,
        "code": 200,
    }


@app.post('/time-domain')
async def time_domain(request: Request):
    options = await request.json()
    file_ext = 'accel'

    if u.check_if_file_exists(options, file_ext) is False:
        data = r.read_csv(options)
        plot_path = await p.plot_acceleration(data, options)
    else:
        plot_path = f'./images/{u.format_accel_plot_name(options, file_ext)}' 

    return {
        "details": "This should return either a graph of acceleration data.",
        "message": os.path.join(root_url, plot_path),
        "success": True,
        "error": False,
        "code": 200
    }


@app.post('/forcing')
async def forcing(request: Request):
    options = await request.json()
    file_ext = 'force'

    if u.check_if_file_exists(options, file_ext) is False:
        data = r.read_csv(options)
        plot_path = await p.plot_forcing(data, options)
    else:
        plot_path = f'./images/{u.format_filename(options)}_{file_ext}.png'

    return {
        "details": "This gives the path to a forcing signal plot.",
        "message": os.path.join(root_url, plot_path),
        "success": True,
        "error": False,
        "code": 200
    }


@app.post('/animate')
async def animate(request: Request):
    options = await request.json()
    file_ext = 'anim'

    if u.check_if_file_exists(options, file_ext) is False:
        data = r.read_csv(options)
        plot_path = await a.animate_beam(data, options)
    else:
        plot_path = f'./images/{u.format_accel_plot_name(options, file_ext)}'

    return {
        "details": "This should the path to a forcing signal gif/plot.",
        "message": os.path.join(root_url, plot_path),
        "success": True,
        "error": False,
        "code": 200
    }


@app.post('/dft')
async def dft(request: Request):
    options = await request.json()
    file_ext = 'dft'

    if u.check_if_file_exists(options, file_ext) is False:
        data = r.read_csv(options)
        plot_path = await p.plot_dft(data, options)
    else:
        plot_path = f'./images/{u.format_accel_plot_name(options, file_ext)}' 

    return {
        "details": "This should return the path to the DFT plot.",
        "message": os.path.join(root_url, plot_path),
        "success": True,
        "error": False,
        "code": 200
    }


@app.post('/bode')
async def bode(request: Request):
    options = await request.json()
    file_ext = 'bode'

    if u.check_if_file_exists(options, file_ext) is False:
        data = r.read_csv(options)
        plot_path = await p.plot_bode(data, options)
    else:
        plot_path = f'./images/{u.format_accel_plot_name(options, file_ext)}' 

    return {
        "details": "This should return the path to the Bode plot.",
        "message": os.path.join(root_url, plot_path),
        "success": True,
        "error": False,
        "code": 200
    }


@app.post('/nyquist')
async def nyquist(request: Request):
    options = await request.json()
    file_ext = 'nyquist'

    if u.check_if_file_exists(options, file_ext) is False:
        data = r.read_csv(options)
        plot_path = await p.plot_nyquist(data, options)
    else:
        plot_path = f'./images/{u.format_accel_plot_name(options, file_ext)}' 

    return {
        "details": "This should return the path to the Nyquist plot.",
        "message": os.path.join(root_url, plot_path),
        "success": True,
        "error": False,
        "code": 200
    }


# @app.get('/raw-data')
# async def raw_data():
#     return {"message": "This should return raw data."}


@app.post('/filter')
async def filter(request: Request):
    options = await request.json()
    file_ext = 'filtered.png'

    if u.check_if_file_exists(options, file_ext) is False:
        data = r.read_csv(options)
        data_path = f.filter(data, options)
    else:
        data_path = f'./images/{u.format_filename(options)}_{file_ext}'

    return {
        "details": "This should return the path to a filtered data file.",
        "message": os.path.join(root_url, data_path),
        "success": True,
        "error": False,
        "code": 200
    }


@app.post('/start-tracking')
async def start_tracking(request: Request):
    options = await request.json()
    
    try:
        with open(f'./tracking/{options["serialNumber"]}.json', 'r') as f:
            tracking_data = json.load(f)
    except FileNotFoundError:
        with open(f'./templates/tracking.json', 'r') as f:
            tracking_data = json.load(f)
    
    tracking_data[str(options["subtaskId"])]["startTime"] = options["timestamp"]

    with open(f'./tracking/{options["serialNumber"]}.json', 'w') as f:
        json.dump(tracking_data, f)

    return {
        "detail": "Starts tracking of subtask.",
        "message": "Tracking of subtask {options['subtaskId']} started.",
        "success": True,
        "error": False,
        "code": 200
    }


@app.post('/stop-tracking')
async def start_tracking(request: Request):
    options = await request.json()
    
    try:
        with open(f'./tracking/{options["serialNumber"]}.json', 'r') as f:
            tracking_data = json.load(f)
    except FileNotFoundError:
        with open(f'./templates/tracking.json', 'r') as f:
            tracking_data = json.load(f)
    
    tracking_data[str(options["subtaskId"])]["endTime"] = options["timestamp"]  # Check if subtask is already being tracked

    with open(f'./tracking/{options["serialNumber"]}.json', 'w') as f:
        json.dump(tracking_data, f)

    return {
        "detail": "Stops tracking of subtask.",
        "message": f"Tracking of subtask {options['subtaskId']} stopped.",
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