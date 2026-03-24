task_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        task TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        counter INTEGER DEFAULT 1
    )
"""

# CRUD - CREATE - READ - UPDATE - DELETE
# INSERT SELECT UPDATE DELETE

insert_task = "INSERT INTO tasks (task, completed, counter) VALUES (?, ?, ?)"

select_task = 'SELECT id, task, completed, counter FROM tasks'

select_task_completed = 'SELECT id, task, completed, counter FROM tasks WHERE completed = 1'

select_task_uncompleted = 'SELECT id, task, completed, counter FROM tasks WHERE completed = 0'

update_task_text = "UPDATE tasks SET task = ? WHERE id = ?"
update_task_completed = "UPDATE tasks SET completed = ? WHERE id = ?"
update_task_counter = "UPDATE tasks SET counter = ? WHERE id = ?"

delete_task = "DELETE FROM tasks WHERE id = ?"



