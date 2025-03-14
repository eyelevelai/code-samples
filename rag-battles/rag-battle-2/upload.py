import os

from dotenv import load_dotenv

load_dotenv()


if os.getenv("GROUNDX_API_KEY") is None:
    raise Exception(
        """


    You have not set GROUNDX_API_KEY
    Copy .env.sample and rename it to .env then fill in the missing values

"""
    )

if os.getenv("GROUNDX_BUCKET_ID") is None:
    raise Exception(
        """


    You have not set GROUNDX_BUCKET_ID
    Copy .env.sample and rename it to .env then fill in the missing values

"""
    )


from gx.rag import upload as gxupload


if __name__ == "__main__":
    gxupload()
