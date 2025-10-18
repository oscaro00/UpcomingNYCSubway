from typing import Union, Dict, Tuple
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime

from subway import is_valid_line_id, get_subway_stop_info, get_upcoming_subway_trains
from nearby_stops import relevant_stops

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/current_time')
def get_current_time() -> str:
    return f'Current time: {datetime.now()}'

@app.get('/stop_info/{line_id}')
def get_stop_info(line_id: str) -> Tuple:
    if not is_valid_line_id(line_id, relevant_stops):
        raise HTTPException(status_code=404, detail=f'line_id {line_id} not found')
    return get_subway_stop_info(line_id, relevant_stops)

@app.get('/upcoming_trains/{line_id}')
def get_upcoming_trains(line_id: str) -> Dict:
    if not is_valid_line_id(line_id, relevant_stops):
        raise HTTPException(status_code=404, detail=f'line_id {line_id} not found')
    return get_upcoming_subway_trains(line_id, relevant_stops)

@app.get("/subway_component/{line_id}", response_class=HTMLResponse)
async def subway_component(line_id: str):
    try:
        stop_info = get_stop_info(line_id)
        stop_ids, walk_time, stop_name = stop_info
        
        train_data = get_upcoming_trains(line_id)
        
        line_data = train_data.get(line_id, {})
        northbound = sorted(line_data.get("N", []))
        southbound = sorted(line_data.get("S", []))
        
        html = f'''
        <div class="stop-info">
            <div class="stop-name">
                <i class="fa-solid fa-location-pin"></i>
                {stop_name}
            </div>
            <div class="walk-time">
                <i class="fa-solid fa-person-walking"></i>
                {walk_time} min walk
            </div>
            <div class="last-updated">
                Updated: {datetime.now().strftime("%H:%M:%S")}
            </div>
        </div>

        <div class="arrivals">
            <div class="arrivals-title">Upcoming Trains</div>
            <div class="directions-container">
        '''

        # Northbound trains
        html += '<div class="direction-section">'
        html += '<div class="direction-label">Northbound</div>'
        if northbound:
            for time in northbound:
                html += f'<div class="arrival-time">{time} min</div>'
        else:
            html += '<div class="no-trains">No trains</div>'
        html += '</div>'

        # Southbound trains
        html += '<div class="direction-section">'
        html += '<div class="direction-label">Southbound</div>'
        if southbound:
            for time in southbound:
                html += f'<div class="arrival-time">{time} min</div>'
        else:
            html += '<div class="no-trains">No trains</div>'
        html += '</div>'

        html += '</div>'  # Close directions-container
        html += '</div>'  # Close arrivals
        
        return html
        
    except Exception as e:
        return f'<div class="error">Error loading data: {str(e)}</div>'


@app.get("/")
async def read_root():
    return FileResponse("htmx/index.html")
