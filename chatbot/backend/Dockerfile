# 1. Fetch the uv binary from the official image (Faster/Cleaner than curling)
FROM ghcr.io/astral-sh/uv:0.9.16 AS uv

# 2. Builder Stage
FROM python:3.11.9-slim-bookworm AS builder

WORKDIR /project

# Copy uv binary from the special stage
COPY --from=uv /uv /uvx /bin/

# Set env vars to speed up build and ensure consistent behavior
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never 

# --- OPTIMIZATION: Dependency Caching ---
# Copy ONLY dependency files first. 
# This ensures 'uv sync' is cached unless dependencies actually change.
COPY pyproject.toml uv.lock ./

# Install dependencies (without dev dependencies like pytest)
# --no-install-project: Installs libraries but waits on your actual code
RUN uv sync --frozen --no-dev --no-install-project

# Now copy the source code (Changing code won't trigger a re-install of deps)
COPY src ./src
# Copy docs 
COPY docs ./docs
# Install the project itself (if your project is a package) or verify env
RUN uv sync --frozen --no-dev

# 3. Final Runtime Stage
FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install --no-install-recommends -y libomp-dev libgomp1

WORKDIR /project

# Security: Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy the environment application code and docs
COPY --from=builder /project/.venv /project/.venv
COPY --from=builder /project/src /project/src
COPY --from=builder /project/docs /project/docs

# Copy pre-initialized Chroma database (if available from build context)
# NOTE: The database/ directory should be copied from the host before building the image
# Run the init_chroma_db.py script on your local machine, then:
# COPY database/ /project/database/
# Comment out the RUN mkdir line below if you COPY a pre-initialized database
# COPY database/ /project/database/ 2>/dev/null || true
COPY database/ /project/database/ 
# RUN mkdir -p /project/database

# Set environment variables
# Adding .venv/bin to PATH removes the need to "source" the venv
ENV PATH="/project/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/project" \
    SKIP_DB_INIT=true

EXPOSE 20000

# Switch to the non-root user
# USER appuser

# CMD is preferred over ENTRYPOINT for arguments that might change
# Running binary directly allows signals (like SIGTERM) to pass correctly
# CMD ["gunicorn", "-w", "4", "src.wsgi:app", "-b", "0.0.0.0:5050", "-t", "0"]
ENTRYPOINT gunicorn -w 1 src.wsgi:app -b 0.0.0.0:20000 -t 0