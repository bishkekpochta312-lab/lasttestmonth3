import sqlite3
from db import queries
from config import path_db



def init_db():
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.task_table)
    print('БД подключена!')
  


def add_task(task,counter=1):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.insert_task,(task,0,counter))
        task_id = cursor.lastrowid 
    return task_id

def update_task(task_id, new_task=None, completed=None, counter=None):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()

        if new_task is not None:
            cursor.execute(queries.update_task_text, (new_task, task_id))

        elif completed is not None:
            cursor.execute(queries.update_task_completed, (completed, task_id))

        elif counter is not None:
            cursor.execute(queries.update_task_counter, (counter, task_id))

def delete_task(task_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.delete_task,(task_id,))
    conn.commit()
    conn.close()



def get_tasks(filter_type="all"):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if filter_type == "all":
        cursor.execute(queries.select_task)
    elif filter_type == "completed":
        cursor.execute(queries.select_task_completed)
    elif filter_type == "uncompleted":
        cursor.execute(queries.select_task_uncompleted)
    else:
        cursor.execute(queries.select_task) 

    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_completed_tasks():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE completed = 1")

    conn.commit()
    conn.close()
