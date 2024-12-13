import os, time

from groundx import GroundX, Document
from groundx.exceptions_base import OpenApiException

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
bucket_id = 0

# set to local file path to upload local file or hosted url
upload_path = ""

# initialize client
client = GroundX(
    api_key=os.getenv("GROUNDX_API_KEY"),
)

if bucket_id == 0:
    # list buckets
    try:
        bucket_response = client.buckets.list()

        if len(bucket_response.buckets) < 1:
            print(bucket_response.buckets)
            raise Exception("no results from buckets")

        bucket_id = bucket_response.buckets[0].bucket_id
    except OpenApiException as e:
        print("Exception when calling BucketApi.list: %s\n" % e)


if upload_path != "":
    # upload local documents to GroundX
    try:
        ingest = client.ingest(
            documents=[
                Document(
                    bucket_id=bucket_id,
                    file_path=upload_path,
                )
            ]
        )

        while (
            ingest.ingest.status != "complete"
            and ingest.ingest.status != "error"
            and ingest.ingest.status != "cancelled"
        ):
            time.sleep(3)
            ingest = client.documents.get_processing_status_by_id(
                process_id=ingest.ingest.process_id
            )
    except OpenApiException as e:
        print("Exception when calling DocumentApi.upload_local: %s\n" % e)

if query != "":
    # search
    try:
        content_response = client.search.content(id=bucket_id, query=query)

        print(content_response.search.text)
    except OpenApiException as e:
        print("Exception when calling SearchApi.content: %s\n" % e)
