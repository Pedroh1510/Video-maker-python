FROM python:3.9
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
  && apt-get update \
  && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
COPY . /.
CMD ["python","index.py"]