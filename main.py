import argparse
import random
import sqlite3
from datetime import datetime, timedelta


class Handler:
    def __init__(self):
        self.format = "%Y-%m-%d %H:%M:%S"
        self.con = sqlite3.connect("PyQuartz.db")
        self.cur = self.con.cursor()
        if not self.cur.execute("SELECT name FROM sqlite_master").fetchone():
            print("databases creating")
            self.create_tables()
            self.insert_test_data()

    def handle(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "action", choices=["start", "stop", "list"], help="Start or end timer"
        )

        args = parser.parse_args()
        action = getattr(self, args.action)
        action()

    def start(self):
        print("timer started")

    def stop(self):
        print("timer stopped")

    def list(self):
        timers = self.cur.execute("SELECT * FROM timers").fetchall()
        sessions_tuples = self.cur.execute("SELECT * FROM sessions").fetchall()
        sessions = []
        for session in sessions_tuples:
            session_dict = {}
            session_dict["timer_id"] = session[0]
            session_dict["started_at"] = datetime.strptime(session[2], self.format)
            if session[3]:
                session_dict["ended_at"] = datetime.strptime(session[3], self.format)
                session_dict["length"] = (
                    session_dict["ended_at"] - session_dict["started_at"]
                )
            else:
                session_dict["length"] = datetime.now() - session_dict["started_at"]
            sessions.append(session_dict)

        # for timer in timers:

        breakpoint()

    def create_tables(self):
        self.cur.execute(
            """
            CREATE TABLE timers (
            timer_id INTEGER PRIMARY KEY,
            title TEXT
            );
            """
        )
        self.cur.execute(
            """
            CREATE TABLE sessions (
                session_id INTEGER PRIMARY KEY,
                sessiontimer INTEGER REFERENCES timer(timer_id),
                starttime TEXT,
                endtime TEXT
                );
            """
        )

    def insert_test_data(self):
        self.cur.execute("INSERT INTO timers (title) VALUES ('Timer 1');")
        self.cur.execute("INSERT INTO timers (title) VALUES ('Timer 2');")

        start_datetime, end_datetime = self.generate_random_datetime_pair()
        start_datetime = start_datetime.strftime(self.format)
        end_datetime = end_datetime.strftime(self.format)
        self.cur.execute(
            "INSERT INTO sessions (sessiontimer, starttime, endtime) VALUES (1, ?, ?);",
            (start_datetime, end_datetime),
        )

        start_datetime, end_datetime = self.generate_random_datetime_pair()
        start_datetime = start_datetime.strftime(self.format)
        end_datetime = end_datetime.strftime(self.format)
        self.cur.execute(
            "INSERT INTO sessions (sessiontimer, starttime, endtime) VALUES (2, ?, ?);",
            (start_datetime, end_datetime),
        )

        self.cur.execute(
            "INSERT INTO sessions (sessiontimer, starttime, endtime) VALUES (2, ?, ?);",
            (datetime.now().strftime(self.format), None),
        )
        self.con.commit()

    def generate_random_datetime_pair(self):
        start_date = datetime.now() - timedelta(days=30)
        start_datetime = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        end_datetime = start_datetime + timedelta(hours=random.randint(1, 24))

        return start_datetime, end_datetime


if __name__ == "__main__":
    handler = Handler()
    handler.handle()
