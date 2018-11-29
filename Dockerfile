FROM python:3.6-slim
RUN apt-get update && apt-get install -y \
 git \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /Compilers323Docker
RUN git clone -b master --single-branch https://github.com/Nathan-LS/Compilers323.git
WORKDIR /Compilers323Docker/Compilers323
RUN pip3 install --upgrade -r requirements.txt
WORKDIR /app
ENTRYPOINT ["python3", "/Compilers323Docker/Compilers323/src"]