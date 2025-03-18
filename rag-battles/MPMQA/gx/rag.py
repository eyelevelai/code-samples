import os, requests, time

from dotenv import load_dotenv
from groundx import Document, GroundX
from openai import OpenAI
import pandas as pd

from util import move_columns


gx = None
oai = None
system_prompt = "you are a helpful AI agent tasked with answering questions with the content provided to you"

load_dotenv(
    override=True,
)


def create_bucket(name):
    global gx

    init()

    res = gx.buckets.create(name=name)

    print(f"\n\tcreated bucket [{name}], bucket ID [{res.bucket.bucket_id}]\n")

def init():
    global gx, oai

    if gx is None:
        gx = GroundX(
            api_key=os.getenv("GROUNDX_API_KEY"),
        )

    if oai is None:
        oai = OpenAI()


def get_file(ur):
    response = requests.get(ur)
    return response.json()


def lookup_by_bucket(id):
    global gx

    init()

    res = gx.documents.lookup(
        id=id,
    )

    xu = []
    for u in res.documents:
        if u.xray_url is not None:
            xu.append(u.xray_url)

    print(xu)


def lookup_by_doc(id):
    global gx

    init()

    res = gx.documents.get(
        document_id=id,
    )

    if res.document.xray_url is not None:
        print(get_file(res.document.xray_url))
    else:
        print(f"no x-ray url for file [{id}]")


def rag(query, model_name, index):
    global gx, oai, system_prompt

    print(f"\n\n{query}\n")

    print(f"querying [{index}]")

    result = None
    retrievals = None
    source = None
    sourceCount = None

    tasktime = time.time()
    for _ in range(3):
        reqtime = time.time()
        try:
            retrievals = gx.search.content(id=index, query=query)
            break
        except Exception as e:
            print(f"gx error, trying again [{time.time() - reqtime:.4f}]")
            print(e)
            print(type(e))
            time.sleep(5)
    print(f"gx done [{time.time() - tasktime:.4f}]")

    if sourceCount == 0:
        # composing response fields
        d = {}
        d["approach"] = "RAG"
        d["response"] = ""
        d["source"] = source
        d["retrieval_count"] = sourceCount
        d["partition_name"] = f"bucket_{index}"
        d["partition_id"] = index

        return d

    source = str(retrievals.search.text)
    sourceCount = len(retrievals.search.results)

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": f"content:\n{source}\n\nanswer the following question using the content above: {query}",
        },
    ]

    tasktime = time.time()
    for _ in range(3):
        reqtime = time.time()
        try:
            result = (
                oai.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=1.0,
                    top_p=0.7,
                )
                .choices[0]
                .message.content
            )
            if result is not None:
                print(f"{str(result)}")
                break
            else:
                print(
                    f"openAI result is none, trying again [{time.time() - reqtime:.4f}]"
                )
                time.sleep(5)
        except Exception as e:
            print(f"error, trying again [{time.time() - reqtime:.4f}]")
            print(e)
            print(type(e))
            time.sleep(5)
    print(f"openAI done [{time.time() - tasktime:.4f}]")

    # composing response fields
    d = {}
    d["approach"] = "RAG"
    d["response"] = str(result)
    d["source"] = source
    d["retrieval_count"] = sourceCount
    d["partition_name"] = f"bucket_{index}"
    d["partition_id"] = index

    return d


def upload(bucket_id, files, batch_size, total):
    global gx

    init()

    total_files = len(files)
    if total > 0 and total < total_files:
        files = files[:total]
        total_files = total

    print(f"\nscheduling files for upload...")

    for i in range(0, total_files, batch_size):
        batch = files[i : i + batch_size]

        docs = []
        for file in batch:
            docs.append(
                Document(
                    bucket_id=bucket_id,
                    file_path=file,
                ),
            )

        ingest = None
        if len(docs) > 0:
            remain = total_files - (i + batch_size)
            if remain < 0:
                remain = 0
            print(f"\nuploading [{len(docs)}] files, [{remain}] remaining")
            try:
                ingest = gx.ingest(
                    documents=docs,
                )
            except Exception as e:
                print("ingest error")
                raise e
            print("\nsuccess, polling for status...")

        print("\nqueued", end="", flush=True)
        while (
            ingest is not None
            and ingest.ingest.status != "complete"
            and ingest.ingest.status != "error"
            and ingest.ingest.status != "cancelled"
        ):
            time.sleep(3)
            ingest = gx.documents.get_processing_status_by_id(
                process_id=ingest.ingest.process_id
            )
            print(f", {ingest.ingest.status}", end="", flush=True)
            if ingest.ingest.status_message:
                print()
                print(ingest.ingest.status_message)

        if ingest.ingest.status == "error" or ingest.ingest.status == "cancelled":
            print()
            print("stopping upload process")
            raise ingest.status.status

        print()


def run(model_name, index, questions):
    init()

    completed = []
    for i, row in questions.iterrows():
        row = dict(row)
        res = rag(row["query"], model_name, index)

        this_row = {**row, **res}
        completed.append(this_row)

    df_completed = pd.DataFrame(completed)

    return move_columns(df_completed)
