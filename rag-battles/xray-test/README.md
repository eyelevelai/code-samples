# X-Ray Test

This is a random sample of 100 documents that have been anonymously uploaded to our [X-Ray demo](https://dashboard.eyelevel.ai/xray/).

These are files that were uploaded by people testing the EyeLevel.ai platform. They represent a mixture of “the hardest file I can think of” and “files representative of my use case”.


## Data Set
The data for this test includes 100 files from a random sample of 1,019 files uploaded by anonymous website visitors to our public X-Ray demo. These are real world files that were uploaded by people testing the EyeLevel platform. They represent a mix of “the hardest file I can think of” and “files representative of my use case”. The files can be found in question_files.py.
The data for this test includes:
  - 100 documents from a random sample of 1,019 files that have been anonymously uploaded to our [X-Ray demo](https://dashboard.eyelevel.ai/xray/)
  - 100 Q&A pairs that reference the content in tables (~33), figures (~33), and text (~33)

## Process

1. **Clone Repository:**  
   Clone the GitHub sample code from:
   [X-Ray Test](https://github.com/eyelevelai/code-samples/tree/main/rag-battles/xray-test)  

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
  - You can clone our [results spreadsheet here](https://docs.google.com/spreadsheets/d/1iRg7AU2uDPwKFKB0V1L6b72oQR-tBc3NlgvWw58TK0A/edit?usp=sharing).
  - Import `results/GroundX_test_{BUCKET_ID}.csv` to the Google sheet named `Import` and replace the `Import` sheet with your test results.
  - Copy the `columns A-H` and paste them into `GX-New-Run`.
  - Clear `column D` in `GX-New-Run` and enter your scores 0-5 in this column.
  - Manually review the answers and compare them to the expected answers in `column B`.
  - Score the answers 0-5, with 0 being completely wrong and 5 being completely right.
  - A final % accuracy will be display on the `Overview` tab.