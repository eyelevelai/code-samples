# RAG Battle 3

This is a scaling test we conducted and [published results for here](https://www.eyelevel.ai/post/do-vector-databases-lose-accuracy-at-scale).


## Data Set

The data for this test includes:
  - Partition0
    - 1,000+ pages of public facing PDFs from the tax consultant Deloitte, from RAG Battle 2
  - Partition1
    - 9,000 pages of documents related to corporate taxes
  - Partition2
    - 40,000 pages of documents related to corporate taxes
  - Partition3
    - 50,000 pages of documents related to corporate taxes
  - 100 Q&A pairs that reference the content in tables (~33), figures (~33), and text (~33), from RAG Battle 2

## Process

1. **Clone Repository:**  
   Clone the GitHub sample code from:
   [RAG Battle 3](https://github.com/eyelevelai/code-samples/tree/main/rag-battles/rag-battle-3)  

2. **Install Dependencies:**  
   Run the following command to install the necessary dependencies:
```bash
pip install -r requirements.txt
```  

3. **Create .env**  
   Copy `.env.sample` to `.env` and add your GroundX and OpenAI API keys to the file.  

4. **Create Buckets:**  
   Create new buckets for each partition in this test and make note of the bucket IDs.
```bash
python bucket.py -n NAME_FOR_PARTITION_0_BUCKET
python bucket.py -n NAME_FOR_PARTITION_1_BUCKET
python bucket.py -n NAME_FOR_PARTITION_2_BUCKET
python bucket.py -n NAME_FOR_PARTITION_3_BUCKET
```  

5. **Create Bucket Groups:**  
   Create new bucket groups for each of the partitions in the test. This will group together your buckets into a single searchable group. Make note of the group IDs.
```bash
python group.py -b BUCKET_ID_FOR_PARTITION_0 BUCKET_ID_FOR_PARTITION_1
python group.py -b BUCKET_ID_FOR_PARTITION_0 BUCKET_ID_FOR_PARTITION_1 BUCKET_ID_FOR_PARTITION_2
python group.py -b BUCKET_ID_FOR_PARTITION_0 BUCKET_ID_FOR_PARTITION_1 BUCKET_ID_FOR_PARTITION_2 BUCKET_ID_FOR_PARTITION_3
``` 

6. **Upload Test Files:**  
   Upload test files to your new buckets by running the following commands:
```bash
python upload.py -p 0 -b BUCKET_ID_FOR_PARTITION_0
python upload.py -p 1 -b BUCKET_ID_FOR_PARTITION_1
python upload.py -p 2 -b BUCKET_ID_FOR_PARTITION_2
python upload.py -p 3 -b BUCKET_ID_FOR_PARTITION_3
```

7. **Run Q&A Test:**  
   Start the RAG tests by running the following commands for each partition:
```bash
python rag.py -g BUCKET_ID_FOR_PARTITION_0
python rag.py -g GROUP_ID_PARTITION_0_PARTITION_1
python rag.py -g GROUP_ID_PARTITION_0_PARTITION_1_PARTITION_2
python rag.py -g GROUP_ID_PARTITION_0_PARTITION_1_PARTITION_2_PARTITION_3
```

8. **Review the Results:**  
  The generated answers will be saved to `results/GroundX_test_{BUCKET_OR_GROUP_ID}.csv`.

9. **Score the Results:**
  - You can clone our [results spreadsheet here](https://docs.google.com/spreadsheets/d/1CUR2f-UI7yebFHCz8wswPgPKHmaS_TLkE_2rdIcOO2g/edit?usp=sharing).
  - Import `results/GroundX_test_{BUCKET_ID_FOR_PARTITION_0}.csv` to the Google sheet named `Import` and replace the `Import` sheet with your test results.
  - Copy the `columns A-H` and paste them into `Partition0`.
  - Clear `column D` in `Partition0` and enter your scores 0-5 in this column.
  - Manually review the answers and compare them to the expected answers in `column B`.
  - Score the answers 0-5, with 0 being completely wrong and 5 being completely right.
  - A final % accuracy will be display on the `Overview` tab.
  - Repeat this process for `Partition1`, `Partition2`, and `Partition3`.