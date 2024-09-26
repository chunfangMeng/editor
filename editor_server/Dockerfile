FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=TRUE

ENV APP_HOME=/var/www/html/editor_server
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# 将当前目录加入到工作目录中（. 表示当前目录）
ADD . $APP_HOME

RUN /usr/local/bin/python -m pip install --upgrade pip >/dev/null 2>&1

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN sed -i 's/\r//' ./start.sh

RUN chmod +x ./start.sh

ENTRYPOINT /bin/bash ./start.sh