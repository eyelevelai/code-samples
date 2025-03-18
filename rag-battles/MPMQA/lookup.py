import argparse, os, sys

from dotenv import load_dotenv

load_dotenv(
    override=True,
)


if os.getenv("GROUNDX_API_KEY") is None:
    raise Exception(
        """


    You have not set GROUNDX_API_KEY
    Copy .env.sample and rename it to .env then fill in the missing values

"""
    )


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print("\n")
        self.print_help()
        print("\n")
        sys.exit(2)


def parse_args():
    parser = CustomArgumentParser(description="Process command-line arguments.")

    parser.add_argument(
        "-b",
        type=int,
        required=False,
        help="The destination bucket ID to look up.",
    )

    parser.add_argument(
        "-d",
        type=str,
        required=False,
        help="The destination document ID to look up.",
    )

    try:
        args = parser.parse_args()

        if args.d is None and args.b is None:
            print("\n\nYou must set either a bucket ID (-b) or document ID (-d).")
            parser.error("")

        return args
    except SystemExit as e:
        raise e


from gx.rag import lookup_by_bucket, lookup_by_doc


if __name__ == "__main__":
    args = parse_args()

    if args.d is not None:
        lookup_by_doc(args.d)
    elif args.b is not None:
        lookup_by_bucket(args.b)
