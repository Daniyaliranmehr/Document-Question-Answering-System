FROM python:3.12-slim

WORKDIR /app

ENV PIP_DEFAULT_TIMEOUT=500
ENV PIP_RETRIES=10
ENV PIP_NO_CACHE_DIR=1

RUN pip install --upgrade pip setuptools wheel

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]