FROM python:3.8
COPY . /
WORKDIR /
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["vu_income/income_hourly.py"]
