# pyserver
template server in python |python微服务小模板

开发日志: https://cgdeeplearn.github.io/2020/05/18/Mirco-service/


## 1. clone project

```
git clone https://github.com/cgDeepLearn/pyserver.git
```

## 2. install pipenv

```
pip install pipenv
```

## 3. install requirements

```shell
cd pyservr/src
pipenv install -r requirements.txt
```

## 4. start server

```shell
cd pyserver/script
./operate start
```

## 5.test request

```shell
curl http://127.0.0.1:10001/test -d '{"order_id":12345}'
```

## 6. and more

- config server_ip/port
- config mysql / redis
- develop api by need
- config gevent workers in gunicorn_config.py

