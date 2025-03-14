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
        nargs="+",
        required=False,
        help="Optional integer list of bucket IDs to group together. If set, you must include at least 2 bucket IDs",
    )
    parser.add_argument(
        "-d",
        type=int,
        required=False,
        help="Optional group ID to delete. Setting this variable with delete the group with the given ID.",
    )
    parser.add_argument(
        "-n",
        type=str,
        required=False,
        default="",
        help="Optional name for the group. Defaults to a list of bucket IDs.",
    )

    try:
        args = parser.parse_args()

        if args.b is not None and len(args.b) == 1:
            print("\n\nYou must include at least 2 bucket IDs like this: -b 1 2.")
            parser.error("")

        return args
    except SystemExit as e:
        raise e


from gx.rag import create_group, delete_group, get_groups


if __name__ == "__main__":
    args = parse_args()

    if args.b is not None:
        name = f""
        for b in args.b:
            if name != "":
                name += ", "
            name += f"{b}"
        name = f"BucketIDs [{name}]"
        if args.n != "":
            name = args.n

        create_group(args.b, name)
    elif args.d is not None:
        delete_group(args.d)
    else:
        get_groups()
