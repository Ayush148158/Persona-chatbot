import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# Force load the .env file
load_dotenv() 

api_key = os.getenv("MISTRAL_API_KEY")

model = ChatMistralAI(
    model="mistral-large-latest",
    api_key=api_key
)

print("press 1 for the Angry mode")
print("press 2 for the sad mode")
print("press 3 for the funny mode")
print("press 4 for the sarcastic mode")

choices = int(input("Enter your choice:- "))
if choices == 1:
    mode = "You are an angry person. You always respond in an angry tone."
elif choices == 2:
    mode = "You are a sad person. You always respond in a sad tone."
elif choices == 3:
    mode = "You are a funny person. You always respond in a funny tone."
elif choices == 4:
    mode = "You are a sarcastic person. You always respond in a sarcastic tone."

messages = [
    SystemMessage(content=mode)
]    

while True:
    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt)) 
    response = model.invoke(messages)
    print(f"AI: {response.content}")