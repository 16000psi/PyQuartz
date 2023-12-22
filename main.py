import argparse
from datetime import datetime


class Handler:
    def __init__(self):
        pass

    def handle(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "action",
            choices=["start", "end"],
            help="Start or end timer"
        )

        args = parser.parse_args()
        action = getattr, args.action

        breakpoint()


if __name__ == "__main__":
    handler = Handler()
    handler.handle()
