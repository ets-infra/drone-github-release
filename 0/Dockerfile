FROM python:3.9.4-buster

COPY release_version.py release_version.py
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
CMD ["python", "release_version.py"]
