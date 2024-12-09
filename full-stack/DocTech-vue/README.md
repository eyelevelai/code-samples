# DocTech
This is a vue front end and flask backend demo of voice enabled RAG application.

To get this working on your own machine, you'll need to do the following:
1. set up a .env file in the backend folder such that the flask app can use your OpenAI and GroundX API Keys
```
GROUNDX_API_KEY = "xxx"
OPENAI_API_KEY = "xxx"
```
2. Create a bucket in GroundX and upload your documents
3. update [doctech.py](https://github.com/DanielWarfield1/DocTech_vue_2/blob/main/backend/docTech.py) to use the `bucket_id` you uploaded your documents to
4. Enable cross origin research sharing on your browser (on chrome you may need to download an extension).
5. `cd` to `backend` and run `pip3 -r requierments.txt`
6. run the flask app with `python3 app.py`
7. in another terminal `cd` to `frontend` and run `npm install`
8. run the frontend with `npm run build`

Further READMEs available in the frontend and backend folders
