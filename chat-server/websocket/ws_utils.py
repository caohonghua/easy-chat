from flask_socketio import  emit
from uuid import UUID

from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory, RedisChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType, load_tools
from config import redis_host, redis_port, redis_slot, redis_ttl, model_name, temperature

def get_chain(user_id,app):
    if user_id in app.socket_cache:
        return app.socket_cache[user_id]
    llm = ChatOpenAI(temperature=temperature, streaming=True, model_name=model_name)
    url = 'redis://' + redis_host + ':' + str(redis_port) + '/' + str(redis_slot)
    redis_history = RedisChatMessageHistory(session_id=user_id,url=url, ttl=redis_ttl)
    memory = ConversationSummaryBufferMemory(chat_memory=redis_history, llm=llm, max_token_limit=500)
    chain = ConversationChain(llm=llm, memory=memory, verbose=False)
    app.socket_cache[user_id] = chain
    return chain


def get_agent(app, tool):
    if tool in app.agent_cache:
        return app.agent_cache[tool]
    llm = OpenAI(temperature=0, streaming=True)
    tools = load_tools([tool], llm=llm)
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=False)
    app.agent_cache[tool] = agent
    return agent

class ChatCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: any) -> any:
        emit('message', token)

    def on_llm_end(self, response: LLMResult, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: any) -> any:
        emit('message', '$$over$$')
        
