# def main():
#     print("Hello from ragudemy!")


# if __name__ == "__main__":
#     main()
# Write this code in main.py
from fastapi import FastAPI
from langserve import add_routes
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Simple Prompt
prompt = PromptTemplate(
    template="Answer the following question:\n\n{question}",
    input_variables = ["question"]
)

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Simple Chain
chain = prompt | llm

# FastAPI app
app = FastAPI()

# Add LangServe route
add_routes(app, 
           chain,
           path="/chat" # end point name used by application to access this route
          )

# Optional if we want do not wnat to use default port
if __name__ == "__main__":
    import uvicorn
    # Start the server on localhost at port 8000. if you deploy this app on private cloud add relevent port here. here we are puting localhost port.
    uvicorn.run(app, host="127.0.0.1", port=8000)
