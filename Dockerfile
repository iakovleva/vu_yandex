FROM python:3.8
ADD . /
WORKDIR /
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "vu_income/yandex.py"]
