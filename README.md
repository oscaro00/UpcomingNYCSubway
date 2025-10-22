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

1. Clone the repository and configure:
   ```bash
   git clone https://github.com/oscaro00/UpcomingNYCSubway.git
   cd UpcomingNYCSubway

   # Create your nearby stops configuration file
   cd python-api
   touch nearby_stops.py
   # See the Configuration section above for the expected format
   cd ..
   ```

2. Build and run the container:
   ```bash
   docker compose up -d
   ```

3. Access the application at `http://localhost:8000`

### Auto-start on Raspberry Pi (Optional)

To automatically start the application on boot (e.g., on a Raspberry Pi):

1. **Update the service file paths:**

   Edit `subway-tracker-startup.service` and update line 11 to match your installation directory:
   ```bash
   # If you cloned to /home/pi/UpcomingNYCSubway, change line 11 to:
   ExecStart=/home/pi/UpcomingNYCSubway/startup-subway-tracker.sh
   ```

   Also ensure the `User` on line 8 matches your username (default is `subwaytracker`).

2. **Make the startup script executable:**
   ```bash
   sudo chmod +x startup-subway-tracker.sh
   ```

3. **Install the systemd service:**
   ```bash
   # Copy the service file to systemd directory
   sudo cp subway-tracker-startup.service /etc/systemd/system/

   # Reload systemd to recognize the new service
   sudo systemctl daemon-reload

   # Enable it to start on boot
   sudo systemctl enable subway-tracker-startup.service

   # Test it now (optional)
   sudo systemctl start subway-tracker-startup.service

   # Check status
   sudo systemctl status subway-tracker-startup.service
   ```

4. **For kiosk mode (auto-open browser):**

   The startup script will automatically open Chromium in kiosk mode. Ensure:
   - Chromium browser is installed: `sudo apt-get install chromium-browser`
   - You have a graphical environment running (desktop)
   - The `XAUTHORITY` path in the service file matches your user's home directory
   - Once in kiosk mode, `alt + space` allows mouse control

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
# styling changes my require the browser cache to be cleared before changes appear

# Check container status
docker compose ps
```
