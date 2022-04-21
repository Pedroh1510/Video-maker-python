FROM python:3.9-slim
# FROM python:3.9

# RUN wget https://github.com/google/fonts/archive/main.tar.gz -O gf.tar.gz && \
#   tar -xf gf.tar.gz && \
#   mkdir -p /usr/share/fonts/truetype/google-fonts && \
#   find $PWD/fonts-main/ -name "*.ttf" -exec install -m644 {} /usr/share/fonts/truetype/google-fonts/ \; || return 1 && \
#   rm -f gf.tar.gz && fc-cache -f && rm -rf /var/cache/*
RUN apt update && apt install fonts-indic -y
RUN apt-get update \
  && apt-get install ffmpeg libsm6 libxext6  -y \
  && apt-get install ffmpeg libsm6 libxext6  -y && apt-get autoclean -y && apt-get clean -y && apt-get autoremove -y

# RUN python -m pip install --upgrade pip \
#   && apk add  --no-cache ffmpeg
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /.

ENV db=True
CMD ["python","index.py"]