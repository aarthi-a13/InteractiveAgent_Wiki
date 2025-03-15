from phi.agent import Agent
import phi.api
from phi.model.openai.like import OpenAILike
from phi.tools.wikipedia import WikipediaTools
from phi.knowledge.wikipedia import WikipediaKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
from os import getenv
from dotenv import load_dotenv
import phi
from phi.playground import Playground, serve_playground_app
from phi.embedder.openai import OpenAIEmbedder

load_dotenv()
phi.api=getenv("PHI_API_KEY")
db_url = "postgresql+psycopg://tsdbadmin:e1a3iwvve9ohkjj4@grjyojkuhl.w51sclyrkc.tsdb.cloud.timescale.com:38160/tsdb"

openai_embedder = OpenAIEmbedder(
    api_key=getenv("AKASH_API_KEY"),
    base_url="https://chatapi.akash.network/api/v1",
    dimensions=1024,
    model="BAAI-bge-large-en-v1-5"
)

model_config = OpenAILike(
    id="Meta-Llama-3-3-70B-Instruct",
    api_key=getenv("AKASH_API_KEY"),
    base_url="https://chatapi.akash.network/api/v1",
    system_prompt="You are a funny and friendly assistant named 'Agent Ninja🥷 who helps users to answer their complex questions using factula data. Introduce yourself only when asked."
)

wiki_knowledge_base = WikipediaKnowledgeBase(
    vector_db=PgVector(
        table_name="wikipedia_documents",
        schema="ai",
        db_url=db_url,
        embedder=openai_embedder
    )
)

wiki_agent= Agent( 
    name="Ninja-Wiki", 
    role="Search Wikipedia for information on a given topic and asnwer user questions with factual information",
    model = model_config, 
    tools=[WikipediaTools(knowledge_base=wiki_knowledge_base)],
    
    instructions=[
        "Always search your knowledge base first and use it if available.",
        "Use the Wikipedia to search and load the information on a topic if it is not in your knowledge base.",
        "Share the source URL of the information you used in your response.",
        "Summarize the response in sections and provide appropriate citations"
        "Important: Use tables where possible.",
    ],
    read_chat_history=True,
    # stream=True,
    show_tool_calls=True,
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
    storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db"),
  )


web_search_agent = Agent(
    name="Ninja-Duck",
    role="Perform comprehensive web searches with parameter validation",
    model=model_config,
    tools=[DuckDuckGo(fixed_max_results=10)],
    instructions = [
    "Validate search parameters before execution.",
    "Include publication dates and source credibility.",
    "Structure responses with key findings, source evaluation, and timeline (if relevant).",
    "Add 'Last updated' timestamp for each fact.",
    "Limit responses to 10 bullet points and 500 words max.",
    "Important: Use tables where possible."
    ],
    read_chat_history=True,
    show_tool_calls=True,
    # stream=True,
    add_datetime_to_instructions=True,
    storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db"),
    markdown=True
)

# When Wiki fails to respond to the user query due to ambiguity in the search string, 
# -the default web search by DuckDuckGo will be used as per the instructions.
master = Agent(
    name="The Great Ninja",
    system_prompt="You are a friendly assistant named 'Agent Ninja🥷' who helps users on their queries. Strictly introduce only when asked",
    role="Collaborate with other agents to provide comprehensive answers",
    model=model_config,
    team=[wiki_agent, web_search_agent],
    instructions=[
        "1. Use the Knowledge Base from Wikipedia agent always.",
        "2. If no result found from the knowledge base, use the Wikipedia search from Wikipedia agent.",
        "3. If still not found, use the Web Search agent.",
        "4. Inform the user when using DuckDuckGo for web searches.",
        "5. Important: Use tables where possible."
    ],
    read_chat_history=True,
    show_tool_calls=True,
    # stream=True,
    add_datetime_to_instructions=True,
    storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db"),
    markdown=True
)

app=Playground(agents=[master,wiki_agent,web_search_agent]).get_app()

if __name__=="__main__":
    serve_playground_app("playground:app", reload=True)