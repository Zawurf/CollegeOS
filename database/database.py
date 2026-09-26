import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def connect():
    return psycopg2.connect(DATABASE_URL)


def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            min_attendance INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timetable(
            id SERIAL PRIMARY KEY,
            subject_id INTEGER NOT NULL,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            class_number INTEGER,
            FOREIGN KEY(subject_id) REFERENCES subjects(id),
            UNIQUE(subject_id, day, start_time, end_time)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS official_data(
            id SERIAL PRIMARY KEY,
            subject_id INTEGER NOT NULL,
            total_classes INTEGER NOT NULL,
            attended_classes INTEGER NOT NULL,
            last_updated TEXT NOT NULL,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_logs(
            id SERIAL PRIMARY KEY,
            subject_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notification_logs(
            id SERIAL PRIMARY KEY,
            subject_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            notified_at TEXT NOT NULL,
            FOREIGN KEY(subject_id) REFERENCES subjects(id),
            UNIQUE(subject_id, date)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def add_subject(name, min_attendance):
    conn = connect()

    try:
        conn.execute("""
            INSERT INTO subjects(name, min_attendance)
            VALUES(%s, %s)
        """, (name, min_attendance))

        conn.commit()

    except psycopg2.IntegrityError:
        conn.rollback()
        print("Subject already exists")

    finally:
        conn.close()


def add_timetable(subject_name, day, start, end):
    sub_id = get_subject_id(subject_name)

    if sub_id is None:
        print(f"Subject '{subject_name}' not found")
        return

    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO timetable(
                subject_id,
                day,
                start_time,
                end_time
            )
            VALUES (%s, %s, %s, %s)
        """, (sub_id, day, start, end))

        conn.commit()

    except psycopg2.IntegrityError:
        conn.rollback()
        print("Lecture already exists")

    finally:
        cursor.close()
        conn.close()

def add_official_data(sub_id, total_cls, atd_cls, last_upd):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO official_data(
            subject_id,
            total_classes,
            attended_classes,
            last_updated
        )
        VALUES (%s, %s, %s, %s)
    """, (sub_id, total_cls, atd_cls, last_upd))

    conn.commit()

    cursor.close()
    conn.close()

def add_daily_logs(sub_id, date, status):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO daily_logs(
            subject_id,
            date,
            status
        )
        VALUES (%s, %s, %s)
    """, (sub_id, date, status))

    conn.commit()

    cursor.close()
    conn.close()


def add_subject(name, min_attendance):
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO subjects(name, min_attendance)
            VALUES (%s, %s)
        """, (name, min_attendance))

        conn.commit()

    except psycopg2.IntegrityError:
        conn.rollback()
        print("Subject already exists")

    finally:
        cursor.close()
        conn.close()


def get_subject_id(subject_name):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM subjects
        WHERE name = %s
    """, (subject_name,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return row[0]

    return None


def get_official_data(sub_id):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            total_classes,
            attended_classes,
            last_updated
        FROM official_data
        WHERE subject_id = %s
    """, (sub_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row


def get_daily_logs(sub_id):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT status
        FROM daily_logs
        WHERE subject_id = %s
    """, (sub_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def get_min_attendance(sub_id):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT min_attendance
        FROM subjects
        WHERE id = %s
    """, (sub_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return row[0]

    return None


def get_today_timetable(day):
    day = day.capitalize()

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            subjects.name,
            timetable.start_time,
            timetable.end_time
        FROM timetable
        JOIN subjects
            ON timetable.subject_id = subjects.id
        WHERE timetable.day = %s
    """, (day,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def is_already_logged(sub_id, date):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM daily_logs
        WHERE subject_id = %s
        AND date = %s
    """, (sub_id, date))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row is not None


def was_notified(sub_id, date):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM notification_logs
        WHERE subject_id = %s
        AND date = %s
    """, (sub_id, date))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row is not None


def mark_notified(sub_id, date):
    conn = connect()
    cursor = conn.cursor()

    notified_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
            INSERT INTO notification_logs(
                subject_id,
                date,
                notified_at
            )
            VALUES (%s, %s, %s)
        """, (sub_id, date, notified_at))

        conn.commit()

    except psycopg2.IntegrityError:
        conn.rollback()

    finally:
        cursor.close()
        conn.close()