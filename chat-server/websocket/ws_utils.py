from flask_socketio import  emit
from uuid import UUID

from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory, RedisChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from langchain.chat_models import ChatOpenAI
from config import redis_host, redis_port, redis_slot, redis_ttl

def get_chain(user_id,app):
    if user_id in app.socket_cache:
        return app.socket_cache[user_id]
    llm = ChatOpenAI(temperature=0, streaming=True)
    url = 'redis://' + redis_host + ':' + str(redis_port) + '/' + str(redis_slot)
    redis_history = RedisChatMessageHistory(session_id=user_id,url=url, ttl=redis_ttl)
    memory = ConversationSummaryBufferMemory(chat_memory=redis_history, llm=llm, max_token_limit=500)
    chain = ConversationChain(llm=llm, memory=memory, verbose=False)
    app.socket_cache[user_id] = chain
    return chain

class ChatCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: any) -> any:
        emit('message', token)

    def on_llm_end(self, response: LLMResult, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: any) -> any:
        emit('message', '$$over$$')
        
