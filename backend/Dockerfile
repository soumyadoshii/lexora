FROM python:3.12-slim
WORKDIR /srv
COPY backend/ ./backend/
COPY frontend/ ./frontend/
RUN pip install --no-cache-dir -r backend/requirements.txt
WORKDIR /srv/backend
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
