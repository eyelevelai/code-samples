# RAG Battle 2

This is an accuracy test we conducted and [published results for here](https://www.eyelevel.ai/post/most-accurate-rag).


## Data Set

The data for this test includes:
  - 1,000+ pages of public facing PDFs from the tax consultant Deloitte
  - 100 Q&A pairs that reference the content in tables (~33), figures (~33), and text (~33)

## Process

1. **Clone Repository:**  
   Clone the GitHub sample code from:
   [RAG Battle 2](https://github.com/eyelevelai/code-samples/tree/main/rag-battles/rag-battle-2)  

2. **Install Dependencies:**  
   Run the following command to install the necessary dependencies:
```bash
pip install -r requirements.txt
```  

3. **Create .env**  
   Copy `.env.sample` to `.env` and add your GroundX and OpenAI API keys to the file.  

4. **Create Bucket:**  
   Create a new bucket for this test and make note of the bucket ID.
```bash
python bucket.py -n NAME_FOR_BUCKET
```  

5. **Upload Test Files:**  
   Upload test files to your new bucket by running the following command:
```bash
python upload.py -b BUCKET_ID
```

6. **Run Q&A Test:**  
   Start the RAG test by running the following command:
```bash
python rag.py -g BUCKET_ID
```

7. **Review the Results:**  
  The generated answers will be saved to `results/GroundX_test_{BUCKET_ID}.csv`.

8. **Score the Results:**
  - You can clone our [results spreadsheet here](https://docs.google.com/spreadsheets/d/1lxlIVBgg2psXQ929AJgcnbknwIcknVCm5pNLz_CyxBs/edit?usp=sharing).
  - Import `results/GroundX_test_{BUCKET_ID}.csv` to the Google sheet named `Import` and replace the `Import` sheet with your test results.
  - Copy the `columns A-H` and paste them into `GX-New-Run`.
  - Clear `column D` in `GX-New-Run` and enter your scores 0-5 in this column.
  - Manually review the answers and compare them to the expected answers in `column B`.
  - Score the answers 0-5, with 0 being completely wrong and 5 being completely right.
  - A final % accuracy will be display on the `Overview` tab.