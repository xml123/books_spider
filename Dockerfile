FROM python:mine
WORKDIR /root/
ADD . /root/
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple/
CMD ["python3","main.py"]

