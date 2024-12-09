import io, json, requests

from request import ingestRequestForm

from db import completeRecords, getFiles, getRecord, initDB
from record import processRecord

from pydantic import BaseModel
from dataclasses import dataclass
from typing import List
from fastapi import FastAPI, HTTPException

app: FastAPI = FastAPI(debug=True)


@dataclass
class Document:
    contentURL: str
    customMeta: dict
    documentID: str
    fileName: str
    status: str


class Process(BaseModel):
    bucketId: int
    callbackUrl: str
    chunks: int
    chunkSize: int


@dataclass
class ProcessResponse:
    message: str
    processed: int


class Callback(BaseModel):
    callbackData: str
    documents: List[Document]
    processId: str
    status: str


@dataclass
class CallbackResponse:
    message: str


db = initDB()


@app.post("/callback")
async def ingest_callback(request: Callback) -> CallbackResponse:
    response: CallbackResponse = CallbackResponse(message="OK")

    dids = []
    rids = []
    for v in request.documents:
        if v.status == "complete":
            rids.append(v.customMeta["docM"]["record_id"])
            dids.append(v.documentID)

    if len(rids) > 0:
        completeRecords(db, rids, dids)
        cbdata = json.loads(request.callbackData)
        idx = 0
        prs = []
        r = getFiles(db, "queued", cbdata["chunkSize"])
        while idx < cbdata["chunkSize"]:
            record = getRecord(r)
            prs.append(processRecord(record))
            idx += 1

        chunks = cbdata["chunks"]
        if chunks > 0:
            try:
                res = ingestRequestForm(
                    db,
                    cbdata["bucketId"],
                    cbdata["callbackUrl"],
                    chunks - 1,
                    cbdata["chunkSize"],
                    prs,
                )
            except Exception as e:
                print(str(e))
            if res["request"].status_code == 200:
                print(
                    "submitted [%d] of [%d] files, [%d chunks left]"
                    % (res["files"], cbdata["chunkSize"], chunks - 1)
                )
            else:
                print(res.status_code, res.text)
        else:
            print("completed chunk processing")
    else:
        print(request)

    return response


@app.post("/start")
async def ingest_start(request: Process) -> ProcessResponse:
    r = getFiles(db, "queued", request.chunkSize)
    idx = 0
    try:
        prs = []
        while idx < request.chunkSize:
            record = getRecord(r)
            prs.append(processRecord(record))

            idx += 1
        res = ingestRequestForm(
            db,
            request.bucketId,
            request.callbackUrl,
            request.chunks - 1,
            request.chunkSize,
            prs,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if res["request"].status_code == 200:
        response: ProcessResponse = ProcessResponse(
            processed=idx,
            message="submitted [%d] of [%d] files, [%d chunks left]"
            % (res["files"], request.chunkSize, request.chunks - 1),
        )
    else:
        print(res.status_code, res.text)
        raise HTTPException(status_code=res.status_code, detail=str(res.text))

    return response
