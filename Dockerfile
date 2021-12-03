FROM python:3.9

RUN wget https://github.com/google/fonts/archive/main.tar.gz -O gf.tar.gz
RUN tar -xf gf.tar.gz
RUN mkdir -p /usr/share/fonts/truetype/google-fonts
RUN find $PWD/fonts-main/ -name "*.ttf" -exec install -m644 {} /usr/share/fonts/truetype/google-fonts/ \; || return 1
RUN rm -f gf.tar.gz
RUN fc-cache -f && rm -rf /var/cache/*

RUN python -m pip install --upgrade pip \
  && apt-get update \
  && apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /.
CMD ["python","index.py"]