import multiprocessing, os

from dotenv import load_dotenv
import pandas as pd


load_dotenv()

if os.getenv("OPENAI_API_KEY") is None:
    raise Exception(
        """


    You have not set OPENAI_KEY
    Copy .env.sample and rename it to .env then fill in the missing values

"""
    )

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

model_name = "gpt-4o"
results_path = "results"

gxidx = [
    os.getenv("GROUNDX_BUCKET_ID"),
]

questions = pd.read_csv("tests/tests-all.csv")
questions.head()


def doGroundX():
    global model_name, questions, results_path

    from gx.rag import run as gxrun

    gx_experiment = "GroundX_DO_test"

    results = gxrun(model_name, gxidx, questions)
    results.to_csv(f"{results_path}/{gx_experiment}_{model_name}.csv", index=False)


if __name__ == "__main__":
    functions = [doGroundX]

    if len(functions) > 1:
        processes = []

        for fn in functions:
            p = multiprocessing.Process(target=fn)
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

    elif len(functions) == 1:
        functions[0]()
