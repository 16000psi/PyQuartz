import argparse
from datetime import datetime


class Handler:
    def __init__(self):
        pass

    def handle(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "action",
            choices=["start", "stop"],
            help="Start or end timer"
        )

        args = parser.parse_args()
        action = getattr(self, args.action)
        action()

    def start(self):

        print("timer started")

    def stop(self):

        print("timer stopped")


if __name__ == "__main__":
    handler = Handler()
    handler.handle()
