FROM python:3.11

SHELL ["/bin/bash", "-c"] 

COPY requirements.txt /tmp/
#RUN mkdir project
WORKDIR /project
# Install Flask
COPY project/ .



RUN python -m venv laredo_env && source laredo_env/bin/activate && pip install --upgrade pip && pip install -r /tmp/requirements.txt

#RUN chown -R root:www-data /project && chmod -R 775 /project

EXPOSE 5050

#CMD [ "/project/laredo_env/bin/gunicorn --bind 0.0.0.0:5050 laredo_api:app" ]
CMD ["/bin/bash"]

# ENTRYPOINT /project/laredo_env/bin/gunicorn -w 4 laredo_api:app -b 0.0.0.0:5050 -t 0
ENTRYPOINT source /project/laredo_env/bin/activate && export PYTHONPATH=/project && /project/laredo_env/bin/gunicorn -w 4 src.wsgi:app -t 0
