from langchain.agents import AgentType, initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage


class Agent:

    def __init__(self):

        self.systemMessage = ''
        self.tools = []

    def add_tool(self, tool: Tool):
        self.tools.append(tool)

    def setSystemMessage(self, systemMessage: str):
        self.systemMessage = SystemMessage(content=systemMessage)

    def setConversationBufferMemory(self,
                                    llm,
                                    memory_key="chat_history",
                                    return_messages=True,
                                    max_token_limit=350,
                                    chat_memory=None):

        self.memory = ConversationBufferMemory(
            memory_key=memory_key,
            return_messages=return_messages,
            llm=llm,
            max_token_limit=max_token_limit,
            chat_memory=chat_memory
        )

    def agent(self, llm):
        # LangChain agent kwargs
        agent_kwargs = {
            "extra_prompt_messages":
            [MessagesPlaceholder(variable_name="chat_history")],
            "system_message":
            self.systemMessage,
        }

        # Create LangChain agent
        agent = initialize_agent(
            self.tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            agent_kwargs=agent_kwargs,
            memory=self.memory,
        )

        return agent
