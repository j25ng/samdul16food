FROM python:3.11

WORKDIR /code

COPY src/samdul16food/main.py /code/

RUN pip install --no-cache-dir --upgrade git+https://github.com/j25ng/samdul16food.git@0.3.0

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
