FROM python:3.12-bookworm

WORKDIR /app

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m playwright install --with-deps chromium && \
    chmod -R 777 /ms-playwright

COPY . .

RUN mkdir -p reports/html allure-results test-results && \
    chmod -R 777 reports allure-results test-results

CMD ["python", "-m", "pytest"]