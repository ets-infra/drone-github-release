FROM python:3.9.4-buster

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
CMD ["python", "release_version.py"]
