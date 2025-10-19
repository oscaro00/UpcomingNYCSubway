FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set working directory
WORKDIR /app

# Copy uv files for dependency resolution
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy application code
COPY python-api/ ./python-api/
COPY htmx/ ./htmx/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "python-api.app:app", "--host", "0.0.0.0", "--port", "8000"]