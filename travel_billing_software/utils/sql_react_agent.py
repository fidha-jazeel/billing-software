# ai_features.py

import os
from pathlib import Path
from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import chat_agent_executor
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from langchain.agents import create_agent
from travel_billing_software.database.db_manager import get_db_path
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from travel_billing_software.utils.path_loader import resource_path

load_dotenv(resource_path("travel_billing_software/.env"))

AI_ENABLED = True


api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    AI_ENABLED = False
    print("GOOGLE_API_KEY not set. AI features disabled.")

def get_agent_report(user_question: str):
    return "AI features are disabled."
if AI_ENABLED:
    try:
        # -------------------------
        # 1. Configure your LLM
        # -------------------------
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            api_key=api_key,
            max_tokens=2000,
            timeout=15,
        )
        print("Using Gemini 2.5 Pro model for LLM.")
        
        # -------------------------
        # 2. Connect to your DB
        # -------------------------
        db_file = get_db_path() 
        db_uri = f"sqlite+pysqlite:///file:{Path(db_file).as_posix()}?mode=ro&cache=shared&uri=true"
        db = SQLDatabase.from_uri(
            db_uri,
            engine_args={
                "connect_args": {
                    "uri": True,
                    "timeout": 2,          # wait up to 2s if DB is busy
                    "check_same_thread": False,
                }
            },
        )

        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        tools = toolkit.get_tools()

        # -------------------------
        # 3. Build agent (THE RIGHT WAY)
        # -------------------------
        system_prompt = """
        You are a Senior Data Analyst at a travel billing company.

        Your job:
        1. Understand the user question.
        2. Decide whether SQL is needed.
        3. If needed, call SQL tools to get the required data.
        4. Analyze the returned dataset:
        - trends
        - anomalies
        - comparisons
        - summary statistics
        5. Provide a final readable business summary:
        - insights
        - explanations
        - recommendations
        - formatted tables/analysis

        Important SQL Rules:
        - NEVER run INSERT / UPDATE / DELETE.
        - ONLY run SELECT queries.
        - Limit results to 10 unless user requests more.
        - SQLite dialect.
        """
        # agent = chat_agent_executor.create(
        #     llm=llm,
        #     tools=tools,
        #     system_prompt=system_prompt,
        #     debug=True
        # )

        agent = create_agent(
            llm,
            tools,
            system_prompt=system_prompt,
        )

        # -------------------------
        # 4. Helper to run user question
        # -------------------------
        def extract_final_answer(full_trace):
            try:
                messages = full_trace['messages']

                # 2. The final message is the last one in the list
                final_ai_message = messages[-1]

                # 3. Access the 'content' key of the final message
                # Note: Since the content is a list of dicts, we need to drill down.
                # In a simpler run, this might be a direct string.
                if isinstance(final_ai_message.content, list):
                    final_answer = final_ai_message.content[0]['text']
                elif isinstance(final_ai_message.content, str):
                    final_answer = final_ai_message.content
                else:
                    final_answer = "Could not parse final answer."
                
                return final_answer
            except Exception as e:
                try:
                    return full_trace['messages'][-1].content
                except:
                    return str(full_trace)

        def get_agent_report(user_question: str):
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_question}]},
            )
            try:
                final_answer = extract_final_answer(result)
                return final_answer
            except Exception as e:
                return result
    except Exception as e:
        AI_ENABLED = False
        print("Error initializing AI features:", str(e))
        def get_agent_report(user_question: str):
            return "AI features are currently unavailable."

if __name__ == "__main__":
    # Example usage
    question = "List the top 5 customers by total billing amount."
    answer = get_agent_report(question)
    print("Agent Answer:", answer)