
FROM python:3.12-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m playwright install --with-deps chromium

COPY . .

RUN mkdir -p reports/html allure-results test-results

CMD ["python", "-m", "pytest", "tests/", "-v", \
     "--browser=chromium", \
     "--html=reports/html/report.html", \
     "--self-contained-html", \
     "--alluredir=allure-results", \
     "--clean-alluredir", \
     "--tracing=retain-on-failure", \
     "--screenshot=only-on-failure", \
     "--video=retain-on-failure", \
     "--output=test-results"]
