import os, sys

from groundx import Groundx, ApiException
import openai

from dotenv import load_dotenv

load_dotenv()

if os.getenv("GROUNDX_API_KEY") is None or os.getenv("OPENAI_API_KEY") is None:
    raise Exception(
        """

    You have not set a required environment variable (GROUNDX_API_KEY or OPENAI_API_KEY)
    Copy .env.sample and rename it to .env then fill in the missing values
"""
    )

# GroundX Project ID or Bucket ID
# Found in your GroundX account
# OR by querying /project, /bucket
groundxId = 0

# Your question
query = "YOUR QUERY HERE"

# Instructions sent to ChatGPT for completions
# You may want to change this
instruction = "You are a helpful virtual assistant that answers questions using the content below. Your task is to create detailed answers to the questions by combining your understanding of the world with the content provided below. Do not share links."

# Initialize the GroundX and OpenAI clients
groundx = Groundx(
    api_key=os.getenv("GROUNDX_API_KEY"),
)

openai.api_key = os.getenv("OPENAI_API_KEY")


# Do a GroundX search
try:
    content_response = groundx.search.content(id=groundxId, query=query)
    results = content_response.body["search"]
except ApiException as e:
    print("Exception when calling SearchApi.content: %s\n" % e)

# Access our suggested retrieved context
llmText = results["text"]

if llmText == "":
    raise Exception("\n\n\tYour search returned an empty result\n")

# Do an OpenAI generation with the retrieved context
completion = openai.chat.completions.create(
    model=os.getenv("OPENAI_MODEL"),
    messages=[
        {
            "role": "system",
            "content": """%s
===
%s
===
"""
            % (instruction, llmText),
        },
        {"role": "user", "content": query},
    ],
)

if len(completion.choices) == 0:
    print("\n\n\tempty result from OpenAI for query [%s]\n\ntresult:\n\n\n" % query)
    print(completion)
    sys.exit()

print(
    "\n\nQUERY\n\n%s\n\n\nSCORE\n\n[%.2f]\n\n\nRESULT\n\n%s\n\n\n"
    % (query, results["score"], completion.choices[0].message.content)
)
