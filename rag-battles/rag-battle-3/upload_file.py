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
        required=True,
        help="The destination bucket ID where files will be uploaded.",
    )
    parser.add_argument(
        "-p",
        type=str,
        required=True,
        help="File path or URL",
    )

    try:
        args = parser.parse_args()

        return args
    except SystemExit as e:
        raise e


from gx.rag import upload


if __name__ == "__main__":
    args = parse_args()

    print(f"\nuploading [{args.p}] to bucket ID [{args.b}]")
    upload(args.b, [args.p], 1, 1)
