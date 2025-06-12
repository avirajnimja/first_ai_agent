from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.llms import Ollama
from tools import search_movies_by_genre, get_movie_details, analyze_movies

llm = Ollama(model="llama3.2")
tools = [search_movies_by_genre, get_movie_details, analyze_movies]

agent = create_tool_calling_agent(llm, tools, prompt=None)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Example Queries
queries = [
    "List sci-fi movies from highest to lowest rating",
    "What is the highest budget movie?",
    "Get details for Inception"
]
for query in queries:
    print(f"Query: {query}")
    print(agent_executor.invoke({"input": query})["output"])
    print("---")