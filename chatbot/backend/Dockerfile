FROM python:3.11.9 as builder

SHELL ["/bin/bash", "-c"] 

# COPY requirements.txt /tmp/
#RUN mkdir project
WORKDIR /project
# Install Flask
# COPY database ./database
RUN mkdir ./database
COPY docs ./docs
COPY src ./src
COPY tests ./tests
COPY pyproject.toml ./
COPY uv.lock ./
# RUN python -m venv .venv && source .venv/bin/activate  && pip install poetry && poetry install --no-root
#RUN poetry install --no-root

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

RUN uv sync

FROM python:3.11.9

WORKDIR /project

COPY --from=builder /project /project

RUN echo 'export PYTHONPATH=project' >> ~/.bashrc
RUN echo 'source .venv/bin/activate' >> ~/.bashrc


#RUN chown -R root:www-data /project && chmod -R 775 /project

EXPOSE 20000


ENTRYPOINT source .venv/bin/activate && export PYTHONPATH=/project && /project/.venv/bin/gunicorn -w 1 src.wsgi:app -b 0.0.0.0:20000