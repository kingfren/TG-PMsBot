FROM python:3.11-slim
RUN apt update ; \
    apt install --no-install-recommends \
    git nano screen procps neofetch
WORKDIR /app
COPY . .
RUN python -m pip install --no-cache-dir -U pip setuptools
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "-m", "pmbot" ]
