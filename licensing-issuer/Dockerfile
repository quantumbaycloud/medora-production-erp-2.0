FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
RUN useradd --create-home --uid 10001 medorax && mkdir -p /data /run/secrets/medorax-license && chown -R medorax:medorax /app /data /run/secrets/medorax-license
USER medorax
EXPOSE 8100
CMD ["uvicorn", "app.main:APP", "--host", "0.0.0.0", "--port", "8100"]
