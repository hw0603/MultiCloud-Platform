FROM python:3.10

# TODO: 현재는 볼륨을 호스트에 마운트하여 사용하므로 주석처리했으나, 배포 시 볼륨을 사용하지 않고 이미지 내부에 파일을 복사하여 사용할 것
# COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload","--host", "0.0.0.0", "--port", "8000"]
