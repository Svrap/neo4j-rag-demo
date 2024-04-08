from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

from llm import llm #call llm from llm.py
from langchain.tools import Tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from tools.vector import kg_qa

tools =[
    Tool.from_function(
        name = "General Chat",
        description="For general chat not covered by other tools",
        func=llm.invoke,
        return_direct=False
    ),
    Tool.from_function(
        name="Vector Search Index",
        description="Provides information about movie plots using vector search",
        func= kg_qa,
        return_direct=False
    )
]

#to keep the history of messages
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=2,
    return_messages=True,
)


#defining the scope of the AGENT
agent_prompt = PromptTemplate.from_template(
    """
You are a Digital Asset expert providing information about Content.
Be as helpful as possible and return as much information as possible.
Do not answer any questions that do not relate to content and its details.

Do not answer any questions using your pre-trained knowledge, only use the information provided in the context.

TOOLS:
------

You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
"""
)



# agent_prompt = hub.pull("hwchase17/react-chat") -> this is will allow the bot to behave like chatGPT
agent = create_react_agent(llm,tools,agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

def generate_response(prompt):
    response = agent_executor.invoke({"input" : prompt})
    print("Response:", response)
    return response
