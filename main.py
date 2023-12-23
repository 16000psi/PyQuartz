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
            "action",
            choices=["start", "stop", "list", "session_list"],
            help="Start or end timer",
        )
        parser.add_argument("other", nargs="?")

        args = parser.parse_args()
        action = getattr(self, args.action)
        action()
        self.con.close()

    def start(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["start"])
        parser.add_argument("timer_title", nargs="?")

        args = parser.parse_args()
        timer_title = args.timer_title

        self.cur.execute(
            """
            INSERT INTO timers (title) VALUES (?);
            """,
            (timer_title,),
        )
        new_timer_id = self.cur.lastrowid

        self.cur.execute(
            """
            INSERT INTO SESSIONS (sessiontimer, starttime) VALUES (?, ?);
            """,
            (new_timer_id, datetime.now().strftime(self.format)),
        )

        self.con.commit()

    def stop(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["stop"])
        parser.add_argument("timer_title", nargs="?")

        args = parser.parse_args()
        timer_title = args.timer_title

        timer_id = self.cur.execute(
            """
            SELECT timer_id FROM timers WHERE title = ?;
            """,
            (timer_title,),
        ).fetchone()[0]

        self.cur.execute(
            """
            UPDATE sessions SET endtime = ?
            WHERE endtime IS NULL
            AND sessiontimer = ?;
            """,
            (datetime.now().strftime(self.format), timer_id),
        )
        self.con.commit()
        breakpoint()

    def list(self):
        session_tuples = self.cur.execute(
            """
            WITH sessions_length AS (
            SELECT
            t.title,
            s.sessiontimer,
            s.session_id,
            s.starttime,
            s.endtime,
            (
            SELECT CASE
                WHEN s.endtime IS NULL THEN
                    strftime('%s', datetime(strftime('%s', ?)
                    - strftime('%s', s.starttime), 'unixepoch'))
                ELSE
                    strftime('%s', datetime(strftime('%s', s.endtime)
                    - strftime('%s', s.starttime), 'unixepoch'))
                END
            ) AS length_seconds,
            (
            SELECT CASE
                WHEN s.endtime IS NULL THEN 0
                ELSE 1
                END
            ) AS completed
            FROM sessions s
            INNER JOIN timers t
            ON s.sessiontimer = t.timer_id
            )
            SELECT title, sum(length_seconds), MIN(completed)
            FROM sessions_length
            GROUP BY sessiontimer;
            """,
            (datetime.now().strftime(self.format),),
        ).fetchall()
        for session in session_tuples:
            time_delta = timedelta(seconds=session[1])
            hours, remainder = divmod(time_delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

            print(f"- {session[0]}: {time_string}. {session[2]}")

    def session_list(self):
        sessions_tuples = self.cur.execute(
            """
            SELECT timers.title,
            sessions.session_id,
            sessions.starttime,
            sessions.endtime
            FROM timers INNER JOIN sessions
            on timers.timer_id = sessions.sessiontimer;
            """
        ).fetchall()

        sessions = [
            {
                "title": session[0],
                "session_id": session[1],
                "starttime": session[2],
                "endtime": session[3],
            }
            for session in sessions_tuples
        ]

        for session in sessions:
            print(
                f" - {session['title']}: session {session['session_id']}, {session['starttime']} - {session['endtime']}"
            )

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
                sessiontimer INTEGER REFERENCES timers(timer_id),
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
