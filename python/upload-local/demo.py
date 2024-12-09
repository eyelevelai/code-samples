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

# set to a value to skip a bucket lookup
# otherwise this demo will use the first result from get all buckets
bucketId = 0

# enumerated file type (e.g. docx, pdf)
# must be set to upload local or hosted
fileType = ""

# must be set to upload local
fileName = ""

# set to local file path to upload local file
uploadLocal = ""

if uploadLocal == "":
    raise Exception("set the local file path")

if fileType == "":
    raise Exception("set the file type to a supported enumerated type (e.g. txt, pdf)")

if fileName == "":
    raise Exception("set a name for the file")


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
                    # optional metadata field
                    # content is added to document chunks
                    # fields are search during search requests
                    # and returned in search results
                    "metadata": {"key": "value"},
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
