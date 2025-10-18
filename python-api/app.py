from typing import Union, Dict, Tuple
from fastapi import FastAPI, HTTPException
from datetime import datetime

from subway import is_valid_line_id, get_subway_stop_info, get_upcoming_subway_trains
from nearby_stops import relevant_stops

app = FastAPI()


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
