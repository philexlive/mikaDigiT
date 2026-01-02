FROM python:3.13.5
WORKDIR /app

RUN useradd -m app

RUN mkdir -p /app/var && chown app:app /app/var

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy source code
COPY --chown=app:app . .

USER app

CMD ["fastapi", "run", "run.py"]