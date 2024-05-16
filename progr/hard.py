import argparse
import psycopg2
import typing as t
import os

def display_trains(trains: t.List[t.Dict[str, t.Any]]) -> None:
    """
    Отобразить список поездов.
    """
    if trains:
        line = '+-{}-+-{}-+-{}-+-{}-+--{}--+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 13,
            '-' * 18,
            '-' * 14
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^13} | {:^18} | {:^14} |'.format(
                "№",
                "Пункт отправления",
                "Номер поезда",
                "Время отправления",
                "Пункт назначения"
            )
        )
        print(line)

        for idx, train in enumerate(trains, 1):
            print(
                '| {:>4} | {:<30} | {:<13} | {:>18} | {:^16} |'.format(
                    idx, train[1], train[2], train[3], train[4]
                )
            )
            print(line)
    else:
        print("Список поездов пуст.")

def create_db() -> None:
    """
    Создать базу данных PostgreSQL.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trains (
            train_id SERIAL PRIMARY KEY,
            departure_point TEXT NOT NULL,
            number_train TEXT NOT NULL,
            time_departure TEXT NOT NULL,
            destination TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stations (
            station_id SERIAL PRIMARY KEY,
            station_name TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_train(departure_point: str, number_train: str, 
              time_departure: str, destination: str) -> None:
    """
    Добавить данные о поезде в базу данных PostgreSQL.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO trains (departure_point, number_train, 
                            time_departure, destination)
        VALUES (%s, %s, %s, %s)
    ''', (departure_point, number_train, time_departure, destination))
    conn.commit()
    conn.close()

def select_all() -> list:
    """
    Выбрать все поезда из базы данных PostgreSQL.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM trains
    ''')
    trains = cursor.fetchall()
    conn.close()
    return trains

def select_trains(destination: str) -> list:
    """
    Выбрать поезда по пункту назначения из базы данных PostgreSQL.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM trains WHERE destination = %s
    ''', (destination,))
    trains = cursor.fetchall()
    conn.close()
    return trains

def main(command_line=None):
    parser = argparse.ArgumentParser("trains")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add", help="Add a new train")
    add.add_argument(
        "-dep",
        "--departure",
        action="store",
        required=True,
        help="The train's departure point"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        required=True,
        help="The train's number"
    )
    add.add_argument(
        "-t",
        "--time",
        action="store",
        required=True,
        help="The time departure of train"
    )
    add.add_argument(
        "-des",
        "--destination",
        action="store",
        required=True,
        help="The train's destination point"
    )

    _ = subparsers.add_parser("display", help="Display all trains")

    select = subparsers.add_parser("select", help="Select the trains")
    select.add_argument(
        "-P",
        "--point",
        action="store",
        required=True,
        help="The required point"
    )

    args = parser.parse_args(command_line)

    create_db()

    if args.command == "add":
        add_train(args.departure, args.number, args.time, args.destination)

    elif args.command == "display":
        display_trains(select_all())

    elif args.command == "select":
        selected = select_trains(args.point)
        display_trains(selected)

if __name__ == "__main__":
    main()