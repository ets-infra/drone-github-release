FROM python:3.9.6-buster

COPY release_version.py /plugin_script/release_version.py
COPY requirements.txt /plugin_script/requirements.txt
RUN python -m pip install -r /plugin_script/requirements.txt
CMD ["python", "/plugin_script/release_version.py"]
