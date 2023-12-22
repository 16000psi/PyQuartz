import argparse
import sqlite3
from datetime import datetime


class Handler:
    def __init__(self):
        con = sqlite3.connect("timers.db")
        self.cur = con.cursor()
        if not self.cur.execute("SELECT name FROM sqlite_master").fetchone():
            print("databases creating")
            self.create_timers_table()

    def handle(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "action", choices=["start", "stop"], help="Start or end timer"
        )

        args = parser.parse_args()
        action = getattr(self, args.action)
        action()

    def start(self):
        print("timer started")
        breakpoint()

    def stop(self):
        print("timer stopped")

    def create_timers_table(self):
        self.cur.execute(
            """
            CREATE TABLE timer (
            timer_id INTEGER PRIMARY KEY,
            title TEXT
            );
            """
        )
        self.cur.execute(
            """
            CREATE TABLE session (
                session_id INTEGER PRIMARY KEY,
                sessiontimer INTEGER REFERENCES timer(timer_id),
                starttime TEXT,
                endtime TEXT
                );
            """
        )


if __name__ == "__main__":
    handler = Handler()
    handler.handle()
