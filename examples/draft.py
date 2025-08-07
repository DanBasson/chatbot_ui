#
# import os
# import requests
#
GROQ_API_KEY = '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'
# import requests
#
# MODEL_NAME = "llama3-8b-8192"  # Use this working model
# url = "https://api.groq.com/openai/v1/chat/completions"
# headers = {
#     "Authorization": f"Bearer {GROQ_API_KEY}",
#     "Content-Type": "application/json"
# }
#
# payload = {
#     "model": MODEL_NAME,
#     "messages": [
#         {"role": "system", "content": "be concise"},
#         {"role": "user", "content": "hello"}
#     ],
#     "temperature": 0.7,
#     "stream": True
# }
#
# response = requests.post(url, headers=headers, json=payload)
#
# print("Status Code:", response.status_code)
# print("Response Text:", response.text)


# =============

import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Required for LangChain to work with Groq
os.environ["OPENAI_API_KEY"] = GROQ_API_KEY
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
llm = ChatOpenAI(
    model="llama3-8b-8192",
    temperature=0.7
)

response = llm.invoke([
    HumanMessage(content="hello")
])


print(response.content)
