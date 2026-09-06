ARG PYTHON_IMAGE=python:3.12.10-slim-bookworm@sha256:fd95fa221297a88e1cf49c55ec1828edd7c5a428187e67b5d1805692d11588db
FROM ${PYTHON_IMAGE}
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.lock
COPY . .
RUN python -m pip install --no-cache-dir --no-deps -e .
CMD ["python", "-m", "uvicorn", "astrobridge.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
