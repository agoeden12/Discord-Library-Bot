FROM python
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /code/
CMD ["python3", "main.py"]