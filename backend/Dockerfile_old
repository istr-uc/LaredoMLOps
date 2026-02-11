FROM python:3.11 as builder

SHELL ["/bin/bash", "-c"] 

# COPY requirements.txt /tmp/
#RUN mkdir project
WORKDIR /project
# Install Flask
COPY .python-version .
COPY pyproject.toml .
COPY uv.lock .
COPY src ./src
COPY test ./test

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

RUN uv sync


FROM python:3.11

EXPOSE 5050

COPY --from=builder /project /project

WORKDIR /project

ENTRYPOINT source /project/.venv/bin/activate && export PYTHONPATH=/project && /project/.venv/bin/gunicorn -w 4 src.wsgi:app -b 0.0.0.0:5050 -t 0
