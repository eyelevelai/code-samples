from agents import Agent
from tools import GroundXTool

query = "What do you know?"

demo = Agent(
    tools=[
        GroundXTool(),
    ],
)

res = demo.process(
    """
    You are a demo Agent that demonstrates the ability to answer questions based on retrieved content from the GroundXTool.

    You create intelligent search queries and search for content, via the GroundXTool, based on the questions posed to you.

    If you fail to find relevant content, you modify your search queries and try again.

    Answer the following question using the content from the GroundXTool:
    {query}
    """.format(
        query=query,
    ),
)

print(f"\nAgent Response:\n{res}\n\n")
