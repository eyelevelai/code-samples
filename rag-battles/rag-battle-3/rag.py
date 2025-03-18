import argparse, multiprocessing, os, sys

from dotenv import load_dotenv
import pandas as pd


load_dotenv(
    override=True,
)

if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
    raise Exception(
        """


    You have not set OPENAI_KEY
    Copy .env.sample and rename it to .env then fill in the missing values

"""
    )

if os.getenv("GROUNDX_API_KEY") is None or os.getenv("GROUNDX_API_KEY") == "":
    raise Exception(
        """


    You have not set GROUNDX_API_KEY
    Copy .env.sample and rename it to .env then fill in the missing values

"""
    )


model_name = "gpt-4o"
results_path = "results"


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print("\n")
        self.print_help()
        print("\n")
        sys.exit(2)


def parse_args():
    parser = CustomArgumentParser(description="Process command-line arguments.")

    parser.add_argument(
        "-g",
        type=int,
        required=True,
        help="Bucket or Group ID to search.",
    )
    parser.add_argument(
        "-f",
        type=str,
        required=False,
        default="tests/tests-all.csv",
        help="Optional relative path to test file.",
    )

    try:
        args = parser.parse_args()

        return args
    except SystemExit as e:
        raise e


def doGroundX(id, questions):
    global model_name, results_path

    from gx.rag import run as gxrun

    gx_experiment = f"GroundX_test_{id}"

    results = gxrun(model_name, id, questions)
    results.to_csv(f"{results_path}/{gx_experiment}_{model_name}.csv", index=False)


if __name__ == "__main__":
    args = parse_args()

    questions = pd.read_csv(args.f)
    questions.head()

    doGroundX(args.g, questions)
