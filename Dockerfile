FROM python:3-slim AS build-env
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt --target /app/dependencies
COPY main.py /app/

FROM gcr.io/distroless/python3
COPY --from=build-env /app /app
WORKDIR /app
ENV PYTHONPATH=/app/dependencies
ENTRYPOINT ["python", "main.py"]
