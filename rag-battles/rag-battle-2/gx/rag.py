import os, time

from groundx import Document, GroundX
from openai import OpenAI
import pandas as pd

from util import move_columns


gx = None
oai = None
system_prompt = "you are a helpful AI agent tasked with answering questions with the content provided to you"


from rag_battle_2 import rag_battle_2_files


def init():
    global gx, oai

    if gx is None:
        gx = GroundX(
            api_key=os.getenv("GROUNDX_API_KEY"),
        )

    if oai is None:
        oai = OpenAI()


def rag(query, model_name, indexes):
    global gx, oai, system_prompt

    res = []

    print(f"\n\n{query}\n")

    for i, pid in enumerate(indexes):
        print(f"querying partition {i}, {pid}")

        result = None
        retrievals = None
        source = None
        sourceCount = None

        tasktime = time.time()
        for _ in range(3):
            reqtime = time.time()
            try:
                retrievals = gx.search.content(id=pid, query=query)
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
            d["partition_name"] = f"partition_{i}"
            d["partition_id"] = pid
            res.append(d)
            continue

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
        d["partition_name"] = f"partition_{i}"
        d["partition_id"] = pid

        res.append(d)

    return res


def upload(files=rag_battle_2_files, batch_size=20):
    global gx

    init()

    gx = GroundX(
        api_key=os.getenv("GROUNDX_API_KEY"),
    )

    total_files = len(files)

    print("scheduling files for upload...")

    for i in range(0, total_files, batch_size):
        batch = files[i : i + batch_size]

        docs = []
        for file in batch:
            docs.append(
                Document(
                    bucket_id=os.getenv("GROUNDX_BUCKET_ID"),
                    file_path=file,
                ),
            )

        ingest = None
        if len(docs) > 0:
            print(f"uploading [{len(docs)}] files")
            try:
                ingest = gx.ingest(
                    documents=docs,
                )
            except Exception as e:
                print("ingest error")
                raise e

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
            print(ingest.ingest.status)


def run(model_name, indexes, questions):
    init()

    completed = []
    for i, row in questions.iterrows():
        row = dict(row)
        res = rag(row["query"], model_name, indexes)

        for res_inst in res:
            this_row = {**row, **res_inst}
            completed.append(this_row)

    df_completed = pd.DataFrame(completed)

    return move_columns(df_completed)
