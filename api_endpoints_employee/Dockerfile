FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/tests

# Upgrade pip before installing test dependencies.
RUN python -m pip install --no-cache-dir --upgrade pip

COPY requirements.txt ./

# Install only the test-runner dependencies; the API is deployed separately.
RUN python -m pip install --no-cache-dir -r requirements.txt

# These API tests use Playwright's request client and do not need browser binaries.
COPY tests/*.py ./
COPY tests/pytest.ini ./

CMD ["pytest", "-n", "3", "-v"]

