import flet as ft 
from db import main_db


def main(page: ft.Page):
    page.title = 'ToDoList'
    page.theme_mode = ft.ThemeMode.LIGHT

    def add_task_db(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task=task)
            print(f'Задача {task} успешно в БД! Его ID - {task_id}')
            task_input.value = None
            page.update()


    task_input = ft.TextField(label='Введите задачу', expand=True, on_submit=add_task_db)
    send_button = ft.ElevatedButton('SEND', on_click=add_task_db)

    main_objects = ft.Row([task_input, send_button])

    page.add(main_objects)


if __name__ == '__main__':
    main_db.init_db()
    ft.app(main)