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
        "-p",
        type=int,
        required=True,
        help="The partition ID files to upload. Must be one of: [1, 2, or 3],",
    )
    parser.add_argument(
        "-b",
        type=int,
        required=True,
        help="The destination bucket ID where files will be uploaded.",
    )
    parser.add_argument(
        "-n",
        type=int,
        required=False,
        default=10,
        help="Optional batch size for each ingest request. Defaults to 10 if not provided.",
    )
    parser.add_argument(
        "-t",
        type=int,
        required=False,
        default=0,
        help="Optional total number of files to process. Defaults to 0, or all, if not provided.",
    )

    try:
        args = parser.parse_args()
        if args.p != 1 and args.p != 2 and args.p != 3:
            print("\n\nYou used an invalid partition ID.")
            parser.error("")
        return args
    except SystemExit as e:
        raise e


from gx.rag import upload


if __name__ == "__main__":
    args = parse_args()

    files = []
    n = 10
    t = 0
    if args.n > 0:
        n = args.n
    if args.t > 0:
        t = args.t

    if args.p == 1:
        from partition_1 import rag_battle_3_p1_files

        files = rag_battle_3_p1_files
    elif args.p == 2:
        from partition_2 import rag_battle_3_p2_files

        files = rag_battle_3_p2_files
    elif args.p == 3:
        from partition_3 import rag_battle_3_p3_files

        files = rag_battle_3_p3_files

    print(
        f"\nuploading [{len(files)}] files for partition [{args.p}] to bucket ID [{args.b}]"
    )

    upload(args.b, files, n, t)
