FROM python:3.11.9

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
RUN python -m venv .venv && source .venv/bin/activate  && pip install poetry && poetry install --no-root
#RUN poetry install --no-root
RUN echo 'export PYTHONPATH=project' >> ~/.bashrc
RUN echo 'source .venv/bin/activate' >> ~/.bashrc

#RUN chown -R root:www-data /project && chmod -R 775 /project

EXPOSE 20000

# CMD ["/bin/bash", "-ec", "while :; do echo '.'; sleep 5 ; done" ]
# COPY .env ./
ENTRYPOINT cp /project/environment/.env /project && source .venv/bin/activate && export PYTHONPATH=/project && /project/.venv/bin/gunicorn -w 1 src.wsgi:app -b 0.0.0.0:20000
# ENTRYPOINT source .venv/bin/activate && export PYTHONPATH=/project && echo $PYTHONPATH && python src/wsgi.py
# ENTRYPOINT ls /project/environment
