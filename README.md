This repository creates a webpage to display nearby and upcoming NYC subway trains.

A small python API uses the `nyct_gtfs` package to parse NYC subway data. A simple HTMX frontend displays the data and refreshes every 60 seconds.

## Configuration

In `python-api/nearby_stops.py`, the only object is a dictionary with the following format that is specific to a NYC location:

```python
relevant_stops = {
    # line_id : ([stop_id1, stop_id2], walking_time, stop_name)
}
```

See `python-api/stops.csv` for the stop ids. Walking time is specific to a NYC location and is assumed to be in minutes.

## Local Testing

```bash
fastapi dev python-api/app.py
```

Then visit `http://127.0.0.1:8000/` to see the web page. `http://127.0.0.1:8000/docs` will show the FastAPI docs.

## Running with Docker (Recommended)

The easiest way to run this application is using Docker, especially for deployment on devices like Raspberry Pi.

### Prerequisites

- Docker and Docker Compose installed on your system

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/oscaro00/UpcomingNYCSubway.git
   cd UpcomingNYCSubway
   ```

2. Build and run the container:
   ```bash
   docker compose up -d
   ```

3. Access the application at `http://localhost:8000`

### Docker Commands

```bash
# Build and start the container in the background
docker compose up -d

# View application logs
docker compose logs -f subway-tracker

# Stop the container
docker compose stop

# Stop the container and remove it
docker compose down

# Update and restart (after code changes)
docker compose up -d --build

# Check container status
docker compose ps
```
