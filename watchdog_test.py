import time
import json
import pyodbc
import os
import csv
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def on_created(event):
    print("Hey, {} has been created !".format(event.src_path))
    if event.src_path == r"C:\Users\Hussain Fiaz\Engineering47\week4\day5\food.json":
        print("File found")
        time.sleep(10)
        write_json_to_sql(event.src_path)
    os.remove(r"C:\Users\Hussain Fiaz\Engineering47\week4\day5\food.json")

def on_deleted(event):
    print("What the flip! Someone deleted {}!".format(event.src_path))


# def on_modified(event):
#     print("Hey buddy, {} has been modified".format(event.src_path))



def on_moved(event):
    print("Ok ok ok, someone has moved {} to {}".format(event.src_path, event.dest_path))


def write_json_to_sql(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            if key == "foodName":
                foodName = value
            elif key == "foodEmail":
                foodEmail = value
            elif key == "subjectValue":
                subject = value
            elif key == "messageValue":
                message = value
        print(foodName, foodEmail, subject, message)
        send_to_database(foodName, foodEmail, subject, message)

def send_to_database(foodName, foodEmail, subject, message):
    server = "localhost,1433"
    database_name = "NorthWind"
    user_name = "SA"
    password = "Passw0rd2018"

    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database_name + ';UID=' + user_name + ';PWD=' + password)
    my_northwind_cursor = connection.cursor()

    sql = "INSERT INTO food(foodName, foodEmail, subjectVal, messageVal) Values('{}','{}', '{}', '{}')".format(foodName, foodEmail, subject, message)
    insert_result_set = my_northwind_cursor.execute(sql)
    insert_result_set.commit()


if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = False
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    # my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = r"C:\Users\Hussain Fiaz\Engineering47\week4\day5"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
