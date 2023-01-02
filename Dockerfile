# Using Python 3.11 Source
# Debian - 11
FROM python:3.11-slim-bullseye
RUN apt update && apt install --no-install-recommends -qy git nano screen
WORKDIR /app
COPY . .
RUN python -m pip install --no-cache-dir -U pip wheel setuptools
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "-m", "pmbot" ]
