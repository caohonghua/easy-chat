# chat-server

使用python3.10以上版本

# 设置

1. 开启虚拟环境

```shell
python3 -m venv .venv
```

2. 启用虚拟环境

```shell
source .venv/bin/activate
```

3. 安装依赖

```shell
pip install -r requirements.txt
```

4. 配置代理

```shell
export OPENAI_API_KEY=sk-******************

export OPENAI_PROXY=127.0.0.1:7890
```

5. 更新配置 config.py


6. 开启websocket服务(应用部署)

```shell
gunicorn -D -b 0.0.0.0:8000 -n chat-server --log-level info --log-file ./run.log -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker main:app
```
