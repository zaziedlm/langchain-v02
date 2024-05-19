import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
# prepare llm
llm = ChatOpenAI(model="gpt-4o")

from langchain_core.messages import SystemMessage, HumanMessage
# prepare system message
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="次の文章を、日本語から英語に翻訳してください。こんにちは、ごきげんいかがですか"),
]

# 1)llm invoke result

result = llm.invoke(messages)
print('1)',result.content)
###############################################################################
from langchain_core.output_parsers import StrOutputParser

# 2)use output parser

result = llm.invoke(messages)
parser = StrOutputParser()
retstr = parser.invoke(result)
print('2)',retstr)
###############################################################################
# 3)chaining llm and parser

chain = llm | parser
retstr = chain.invoke(messages)
print('3)',retstr)
###############################################################################
# 4)prompt template chain

from langchain_core.prompts import ChatPromptTemplate

# prepare prompt template
prompt_template  =  ChatPromptTemplate.from_messages(
    [
        ("system", "日本語から{lang}に翻訳してください"), 
        ("user", "{text}")
    ]
)

chain = prompt_template | llm | parser
result = chain.invoke({
    "lang": "英語",
    "text": "こんにちは、ごきげんいかがですか"
})
print('4)',result)
