from nyct_gtfs import NYCTFeed
from datetime import datetime
from typing import Dict, List, Tuple


def get_nyc_subway_data(line_id: str, relevant_stops: Dict) -> Dict:
    stop_id = None
    for line_ids, stop_info in relevant_stops.items():
        if line_id in line_ids:
            stop_id = stop_info[0]
            break
    
    feed = NYCTFeed(line_id)
    trains = feed.filter_trips(line_id=line_id, headed_for_stop_id=stop_id, underway=True)

    upcoming_trains = {}
    north_trains = []
    south_trains = []

    for train in trains:
        for stop in train.stop_time_updates:
            if stop.stop_id in stop_id and train.direction == 'N':
                north_trains.append(stop.arrival)
            elif stop.stop_id in stop_id and train.direction == 'S':
                south_trains.append(stop.arrival)
    upcoming_trains.update({line_id : {'N' : north_trains, 'S' : south_trains}})

    return upcoming_trains


def calc_time_diff(upcoming_trains: Dict) -> Dict:
    current_time = datetime.now()

    time_diff_dict = {}

    for line, arrivals in upcoming_trains.items():
        time_diff_dict[line] = {}
        for direction, times in arrivals.items():
            time_diff_dict[line][direction] = [int((time - current_time).total_seconds() // 60) for time in times]
    
    return time_diff_dict


def filter_walkable_trains(train_times: Dict, relevant_stops: Dict) -> Dict:
    line_id = list(train_times.keys())[0]
    walking_time = None

    for lines, stop_info in relevant_stops.items():
        if line_id in lines:
            walking_time = stop_info[1]
    
    filtered_trains_dict = {}

    for line, arrivals in train_times.items():
        filtered_trains_dict[line] = {}
        for direction, times in arrivals.items():

            filtered_trains_dict[line][direction] = [time for time in times if time > walking_time][0:3]
    
    return filtered_trains_dict


def get_upcoming_subway_trains(line_id: str, relevant_stops: Dict) -> Dict:
    raw_train_data = get_nyc_subway_data(line_id, relevant_stops)
    train_time_difference = calc_time_diff(raw_train_data)
    filtered_trains = filter_walkable_trains(train_time_difference, relevant_stops)

    return filtered_trains


def is_valid_line_id(line_id: str, relevant_stops: Dict) -> bool:
    for line_ids in relevant_stops.keys():
        if line_id in line_ids:
            return True
    return False


def get_subway_stop_info(line_id: str, relevant_stops: Dict) -> Tuple:
    for line_ids, stop_info in relevant_stops.items():
        if line_id in line_ids:
            return stop_info
    return ()


if __name__ == '__main__':
    pass
