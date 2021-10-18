FROM python:3.9
RUN python -m pip install --upgrade pip \
  && apt-get update \
  && apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /.
CMD ["python","index.py"]