import os, time

from groundx import Groundx, ApiException

from dotenv import load_dotenv

load_dotenv()

if os.getenv("GROUNDX_API_KEY") is None:
    raise Exception(
        """

    You have not set a required environment variable (GROUNDX_API_KEY)
    Copy .env.sample and rename it to .env then fill in the missing values
"""
    )

query = "YOUR QUERY"

# set to a value to skip a bucket lookup
# otherwise this demo will use the first result from get all buckets
bucketId = 0

# enumerated file type (e.g. docx, pdf)
# must be set to upload local or hosted
# fileType = ""
fileType = ""

# must be set to upload local
fileName = ""

# set to local file path to upload local file
uploadLocal = ""

# set to hosted URL to upload hosted file
uploadHosted = ""


# initialize client
groundx = Groundx(
    api_key=os.getenv("GROUNDX_API_KEY"),
)


if bucketId == 0:
    # list buckets
    try:
        bucket_response = groundx.buckets.list()

        if len(bucket_response.body["buckets"]) < 1:
            print(bucket_response.body["buckets"])
            raise Exception("no results from buckets")

        bucketId = bucket_response.body["buckets"][0]["bucketId"]
    except ApiException as e:
        print("Exception when calling BucketApi.list: %s\n" % e)


if uploadLocal != "" and fileType != "" and fileName != "":
    # upload local documents to GroundX
    try:
        ingest = groundx.documents.upload_local(
            body=[
                {
                    "blob": open(uploadLocal, "rb"),
                    "metadata": {
                        "bucketId": bucketId,
                        "fileName": fileName,
                        "fileType": fileType,
                    },
                },
            ]
        )

        while (
            ingest.body["ingest"]["status"] != "complete"
            and ingest.body["ingest"]["status"] != "error"
            and ingest.body["ingest"]["status"] != "cancelled"
        ):
            time.sleep(3)
            ingest = groundx.documents.get_processing_status_by_id(
                process_id=ingest.body["ingest"]["processId"]
            )
    except ApiException as e:
        print("Exception when calling DocumentApi.upload_local: %s\n" % e)


if uploadHosted != "":
    # upload hosted documents to GroundX
    try:
        ingest = groundx.documents.upload_remote(
            documents=[{"bucketId": bucketId, "sourceUrl": uploadHosted}],
        )

        while (
            ingest.body["ingest"]["status"] != "complete"
            and ingest.body["ingest"]["status"] != "error"
            and ingest.body["ingest"]["status"] != "cancelled"
        ):
            time.sleep(3)
            ingest = groundx.documents.get_processing_status_by_id(
                process_id=ingest.body["ingest"]["processId"]
            )
    except ApiException as e:
        print("Exception when calling DocumentApi.upload_remote: %s\n" % e)

if query != "":
    # search
    try:
        content_response = groundx.search.content(id=bucketId, query=query)

        print(content_response.body["search"]["text"])
    except ApiException as e:
        print("Exception when calling SearchApi.content: %s\n" % e)
