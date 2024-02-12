FROM python:3.11-slim
LABEL authors="strixprogrammer"

ENV APP_HOME /app

WORKDIR $APP_HOME

# Copy the Python requirements and install them
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

RUN chmod +x ./start.sh

EXPOSE 8000

# Use the script as the entry point
ENTRYPOINT ["./start.sh"]
