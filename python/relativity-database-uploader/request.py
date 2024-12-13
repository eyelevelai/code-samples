import json, requests

from config import ingest
from db import updateRecordStatus

maxFile = 4500000
maxRequest = 4500000
minFile = 4


def ingestRequestForm(db, bid, cb, cks, sz, prs):
    headers = {
        "X-API-Key": ingest["apiKey"],
    }

    fileCnt = 0
    requestSize = 0
    files = {}
    for pr in prs:
        cbdata = dict(
            bucketId=bid,
            callbackUrl=cb,
            chunks=cks,
            chunkSize=sz,
        )

        meta = json.dumps(
            dict(
                bucketId=bid,
                callbackData=json.dumps(cbdata),
                callbackUrl=cb,
                fileName=pr["filename"],
                metadata=pr["meta"],
            )
        )

        if len(meta.encode("utf-8")) + requestSize > maxRequest:
            print(
                "[1] request size too large [%d], stopping at [%d] files"
                % (len(meta.encode("utf-8")) + requestSize, fileCnt)
            )
            break

        shouldAdd = True
        file = open(pr["text_link"], "rb").read()
        if len(file) > maxFile:
            print(
                "file too large [%d] [%d] [%s]"
                % (pr["record_id"], len(file), pr["filename"])
            )
            updateRecordStatus(db, pr["record_id"], "too-large")
            shouldAdd = False
        elif len(file) < minFile:
            print(
                "file too small [%d] [%d] [%s]"
                % (pr["record_id"], len(file), pr["filename"])
            )
            updateRecordStatus(db, pr["record_id"], "too-small")
            shouldAdd = False
        elif len(file) + len(meta.encode("utf-8")) + requestSize > maxRequest:
            print(
                "[2] request size too large [%d], stopping at [%d] files"
                % (len(file) + len(meta.encode("utf-8")) + requestSize, fileCnt)
            )
            break

        if shouldAdd == True:
            requestSize += len(file) + len(meta.encode("utf-8"))
            fileCnt += 1
            files["meta-%d" % pr["record_id"]] = (
                None,
                meta,
                "application/json; charset=UTF-8",
            )
            files["blob-%d" % pr["record_id"]] = (
                None,
                file.decode("utf-8"),
                "text/plain; charset=UTF-8",
            )

    return {
        "request": requests.post(ingest["url"], headers=headers, files=files),
        "files": fileCnt,
    }


def ingestRequestMixed(bid, cb, cks, sz, prs):
    bnd = ingest["mmBoundary"]
    headers = {
        "Content-Type": "multipart/mixed; boundary=%s" % bnd,
        "X-API-Key": ingest["apiKey"],
    }

    body = """
"""

    for pr in prs:
        cbdata = dict(
            bucketId=bid,
            callbackUrl=cb,
            chunks=cks,
            chunkSize=sz,
        )

        meta = json.dumps(
            dict(
                bucketId=bid,
                callbackData=json.dumps(cbdata),
                callbackUrl=cb,
                metadata=pr["meta"],
            )
        )

        file = open(pr["text_link"], "rb").read().decode("utf-8")

        body += """--%s
Content-Disposition: attachment; name="blob"; filename="%s"
Content-Type: text/plain; charset=utf-8

%s
--%s
Content-Disposition: attachment; name="metadata"
Content-Type: application/json

%s
""" % (
            bnd,
            pr["filename"],
            file,
            bnd,
            meta,
        )

    body += (
        """--%s--
"""
        % bnd
    )

    return requests.post(ingest["url"], headers=headers, data=body)
