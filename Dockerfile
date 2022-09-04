FROM python:3.9.13-bullseye

ENV DIR_WORK=/workspace
RUN mkdir ${DIR_WORK} 
WORKDIR ${DIR_WORK}
COPY . .

# python
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install -r requirements.txt
