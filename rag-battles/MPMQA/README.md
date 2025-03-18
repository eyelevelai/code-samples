# MPMQA

This is an accuracy test based on the [MPMQA dataset](https://arxiv.org/abs/2304.09660).

## Data Set

The data for this test includes:
- 10,000+ pages of product manuals

## Process

1. **Clone Repository:**  
   Clone the GitHub sample code from:
   [MPMQA Code Repository](https://github.com/eyelevelai/code-samples/tree/main/rag-battles/mpmqa)  

2. **Install Dependencies:**  
   Run the following command to install the necessary dependencies:
```bash
pip install -r requirements.txt
```  

3. **Create .env**  
   Copy `.env.sample` to `.env` and add your GroundX API Key to the file. You can also add your OpenAI API Key if you'd like to use `rag.py`.  

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