from flask_socketio import emit
from flask import request
from langchain.schema import LLMResult
from .. import socketio
import log

logger = log.setup_logger(__name__)

chat_socket_cache = {}


@socketio.on('connect', namespace='/chat')
def connect():
    user_id = request.args.get('user_id')
    client_ip = request.remote_addr
    user_key = client_ip + '-' + user_id
    get_chat_chain(user_key)
    logger.debug(f'聊天websocket连接成功, 客户端：{user_key}')


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    user_id = request.args.get('user_id')
    client_ip = request.remote_addr
    user_key = client_ip + '-' + user_id
    del chat_socket_cache[user_key]
    logger.debug(f'聊天websocket连接断开, 客户端：{user_key}')


@socketio.on('message', namespace='/chat')
def message(data):
    user_id = request.args.get('user_id')
    client_ip = request.remote_addr
    user_key = client_ip + '-' + user_id
    logger.debug(f'接受到聊天消息：{data}, 客户端：{user_key}')
    chain = get_chat_chain(user_key)
    chain.predict(input=data, callbacks=[ChatCallbackHandler(user_key=user_key)])



from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationTokenBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from config import temperature, model_name


CHAT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.This AI can provide answers in the corresponding language based on the language used by the questioner.

Current conversation:
{chat_history}
Human: {input}
AI:"""

def get_chat_chain(user_key):
    """获取用户聊天chat"""

    # 判断是否存在缓存
    if user_key in chat_socket_cache:
        return chat_socket_cache[user_key]
    # 构建模板
    prompt = PromptTemplate(input_variables=['chat_history', 'input'], template=CHAT_TEMPLATE)
    # 构建chain
    llm = ChatOpenAI(temperature=temperature, streaming=True, model_name=model_name)
    memory = ConversationTokenBufferMemory(memory_key='chat_history', llm=llm, max_token_limit=2000)
    chain = ConversationChain(llm=llm, memory=memory,prompt=prompt, verbose=True)
    # 缓存chain
    chat_socket_cache[user_key] = chain
    return chain

from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
import tiktoken

encoding = tiktoken.get_encoding('cl100k_base')

class ChatCallbackHandler(BaseCallbackHandler):

    def __init__(self, user_key) -> None:
        self.user_key = user_key
        self.tokens = 0

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], *, run_id: UUID, parent_run_id: UUID | None = None, tags: List[str] | None = None, **kwargs: Any) -> Any:
        return super().on_llm_start(serialized, prompts, run_id=run_id, parent_run_id=parent_run_id, tags=tags, **kwargs)

    def on_llm_end(self, response: LLMResult, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
        emit('message', '$$over$$')

    def on_llm_new_token(self, token: str, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
        """发送websocket信息"""
        emit('message', token)

    def on_llm_error(self, error: Exception | KeyboardInterrupt, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
        return super().on_llm_error(error, run_id=run_id, parent_run_id=parent_run_id, **kwargs)
    
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], *, run_id: UUID, parent_run_id: UUID | None = None, tags: List[str] | None = None, **kwargs: Any) -> Any:
        logger.debug(f'input: {inputs}')
        input = inputs['input']
        self.tokens += len(encoding.encode(input))
        history = inputs['chat_history']
        self.tokens += len(encoding.encode(history))

    def on_chain_error(self, error: Exception | KeyboardInterrupt, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
        return super().on_chain_error(error, run_id=run_id, parent_run_id=parent_run_id, **kwargs)
    
    def on_chain_end(self, outputs: Dict[str, Any], *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
        res = outputs['response']
        self.tokens += len(encoding.encode(res))
        logger.debug(f'总消耗token: {self.tokens}')
