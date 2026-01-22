FROM python:3.12-alpine

WORKDIR /app

# Устанавливаем только необходимые зависимости для psycopg2
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py migrate && python  .py runserver 0.0.0.0:8000"]