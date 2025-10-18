This repository creates a webpage to display nearby and upcoming NYC subway trains.

A small python API uses the `nyct_gtfs` package to parse NYC subway data. A simple HTMX frontend displays the data and refreshes every 60 seconds.

In `python-api/nearby_stops.py`, the only object is a dictionary with the following format that is specific to a NYC location:

```python
relevant_stops = {
    # line_id : ([stop_id1, stop_id2], walking_time, stop_name)
}
```

See `python-api/stops.csv` for the stop ids. Walking time is specific to a NYC location and is assumed to be in minutes.
