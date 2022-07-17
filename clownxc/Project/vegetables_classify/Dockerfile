FROM python:3.7.12-slim-buster
ENV TZ Asia/Shanghai
EXPOSE 6000

COPY index.py requirements.txt vegetable_model_v1.h5 /app/
WORKDIR /app/
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

ENTRYPOINT python index.py