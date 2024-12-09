from groundx import Groundx
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# Setting up API keys
groundx = Groundx(
    api_key=os.environ['GROUNDX_API_KEY']
)

#===============================================================================
# Action Parsing
#===============================================================================

#action determiner
class Action(TypedDict):
    scroll_up: bool
    scroll_down: bool
    next_page: bool
    previous_page: bool
    snap_page: bool
    find_fig: bool
    find_pdf: bool
    non_determ: bool

action_parse_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Decide if the user wants one of the following actions performed:
            - `scroll_up`: scroll up a small amount within one page of the pdf
            - `scroll_down`: scroll down a small amount within one page of the pdf
            - `snap_page`: snap to a specific page of a pdf
            - `find_fig`: find a specific figure, table, image, or specific item.
            - `find_doc`: find a specific doc
            - `non_determ`: no valid action is discernable
            The values above are mutually exclusive. One should be true, the rest should be false.
            note: you can use snap_page to go to a page relative to the current page.
            note: blanket questions should default to find figure, unless they're obviously about a document.
            note: if a user asks a general question, assume it's from a figure and try to find a relevent figure.
            """,
        ),
        ("placeholder", "{messages}"),
    ]
)

action_parser = action_parse_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(Action)

#===============================================================================
# Snap Page Parsing
#===============================================================================

class SnapPage(TypedDict):
    snap_page: int

snap_page_parse_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Parse out the specific page of the pdf the user wants to snap to.
            """,
        ),
        ("placeholder", "{messages}"),
    ]
)

snap_page_parser = snap_page_parse_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(SnapPage)

#===============================================================================
# Figure Description Parsing
#===============================================================================

class FigDesc(TypedDict):
    figure_description: str

fig_desc_parse_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """The user wants to find a figure. Extract a description of the figure the user needs. Include all
            relevent information which might be used to identify the figure. Your response should be thorough, and fairly
            long, but not contain fluff. "I need a figure of ..."
            """,
        ),
        ("placeholder", "{messages}"),
    ]
)

fig_desc_parser = fig_desc_parse_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(FigDesc)

#===============================================================================
# Document Description Parsing
#===============================================================================

class DocDesc(TypedDict):
    doc_description: str

doc_desc_parse_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """The user wants to find a document. Extract a description of the document the user needs. Include all
            relevent information which might be used to identify the figure. Your response should be thorough, and fairly
            long, but not contain fluff. "I need a document of ..."
            """,
        ),
        ("placeholder", "{messages}"),
    ]
)

doc_desc_parser = doc_desc_parse_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(DocDesc)

#===============================================================================
# Search for Figure
#===============================================================================

bucket_id = 11795

def gx_search_figure(query):

    response = groundx.search.content(
        id=bucket_id,
        query=query
    )

    semantic_object = response.body['search']['results'][0]
    rag_context = response.body['search']['text']

    return semantic_object['sourceUrl'], semantic_object['boundingBoxes'][0]['pageNumber'], rag_context

#===============================================================================
# Search for Documents
#===============================================================================

def gx_search_document(query):

    response = groundx.search.content(
        id=bucket_id,
        query=query
    )

    semantic_object = response.body['search']['results'][0]
    rag_context = response.body['search']['text']

    return semantic_object['sourceUrl'], rag_context

#===============================================================================
# Old Endpoint
#===============================================================================

def handle_query(query, context):
    #getting action that should be performed
    response = action_parser.invoke({"messages": [("ai", "my name is doc tech, what action would you like me to perform?"),("user", query)]})
    response['pdf']= None
    response['page']=None

    #doing follow up as necessary
    if response['snap_page']:
        response['page']=snap_page_parser.invoke({"messages": [("ai", f"my name is doc tech, what page would you like to snap to. Current state: {context}"),("user", query)]})
    elif response['find_fig']:
        response['pdf'], response['page'], _ = gx_search_figure(query)
    elif response['find_pdf']:
        response['pdf'], _ = gx_search_document(query)

    return response

#===============================================================================
# New Endpoints With Voice
#===============================================================================

def decide_and_respond(query, context):
    #getting action that should be performed
    response = action_parser.invoke({"messages": [("ai", "my name is doc tech, what action would you like me to perform?"),("user", query)]})
    response['query']= query
    response['context']=context
    response['page']=None
    response['does_follow_up']=False

    #doing follow up as necessary
    if response['snap_page']:
        response['page']=snap_page_parser.invoke({"messages": [("ai", f"my name is doc tech, what page would you like to snap to. Current state: {context}"),("user", query)]})

    #Prompting the language model to come up with a response.
    class VerbalResponse(TypedDict):
        immediate_response: str
        followup_response: bool

    verb_resp_parse_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""You will be given a users query, and the actions a system decided to take based on that query.
                respond to the user verbally with an "immediate_response", informing them what action will be taken. Be breif and conversational.
                This is powered by GroundX, which is a retreival engine designed to work with complex real world documents.
                If the user asks about GroundX, tell them they use a computer vision based parsing system, trained on a large amount of corperate documents to understand documents. GroundX can run in the cloud, on prem, whatever.

                After the "immediate_response" has been given, and an action has been performed, you will have access to additional information if the action includes finding a pdf or figure.
                use "followup_response" to decide if you think it will be helpful to use that information to provide further verbal response.
                For instance, if a user asks you to pull up a figure or PDF without a question, no further verbal response is necessary. If the user asks you
                to answer a question, or needs help with something, you can answer that question with a verbal response after the information is retreived.
                If you already know the answer, you can provide that in the "immediate_response", and no "followup_response" is necessary.
                """,
            ),
            ("placeholder", "{messages}"),
        ]
    )

    verb_resp_parser = verb_resp_parse_prompt | ChatOpenAI(
        model="gpt-4o", temperature=0
    ).with_structured_output(VerbalResponse)

    response_info = verb_resp_parser.invoke({"messages": [("user", query),("ai", str(response))]})
    verbal_response = response_info['immediate_response']
    response['does_follow_up'] = response_info['followup_response']

    print('verbal response:')
    print(verbal_response)

    print('Will Follow Up:')
    print(response['does_follow_up'])

    #constructing audio
    from openai import OpenAI
    client = OpenAI()

    speech_file_path = "speech.mp3"
    r = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=verbal_response
    )
    r.stream_to_file(speech_file_path)

    #returning json object
    return response

def handle_action(response): 
    query = response['query']
    response['pdf']= None
    response['page']=None

    #Finding figure or pdf if necessary
    if response['find_fig']:
        response['pdf'], response['page'], rag_context = gx_search_figure(query)
    elif response['find_pdf']:
        response['pdf'], rag_context = gx_search_document(query)

    if response['does_follow_up']:
        #Constructing a verbal response post RAG.
        class VerbalResponse(TypedDict):
            response: str

        verb_resp_parse_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""A user has a query which has triggered a process to look up data which should be relevent to that query.
                    The relevent data is included below. Use this data to answer the users question. Say things like "from this document"
                    and "on page __".

                    If the data does not answer the question, tell the user you're not sure but they might find their answer in the document below.

                    you don't have to clarify that you can't see or can't show the document. The information below contains the information you need,
                    and the user is currently looking at the document.

                    Try not to repeat the full document name, as that can be rather long.

                    Try to keep your responses breif, quick, and direct unless prompted otherwise.

                    === lookup data relevent to query ===
                    {str(rag_context).replace('}', '}}').replace('{', '{{')}
                    """,
                ),
                ("placeholder", "{messages}"),
            ]
        )

        verb_resp_parser = verb_resp_parse_prompt | ChatOpenAI(
            model="gpt-4o", temperature=0
        ).with_structured_output(VerbalResponse)
        verbal_response = verb_resp_parser.invoke({"messages": [("user", query)]})['response']

        print('followup verbal response:')
        print(verbal_response)

        #constructing audio
        from openai import OpenAI
        client = OpenAI()

        speech_file_path = "speech2.mp3"
        r = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=verbal_response
        )
        r.stream_to_file(speech_file_path)

    return response