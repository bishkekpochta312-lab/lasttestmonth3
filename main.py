import flet as ft 
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDoList'
    page.theme_mode = ft.ThemeMode.DARK

    task_list = ft.Column()

    def delete_task(task_id, row):
            main_db.delete_task(task_id=task_id)  
            task_list.controls.remove(row)        
            page.update()

    def view_tasks(task_id, task_text,completed=None,date=None):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

        date_text = ft.Text(
            value=date if date else "",
            size=12,
            color="grey"
        )

        checkbox_task = ft.Checkbox(value=bool(completed),on_change=lambda e:toggle_task(task_id=task_id,is_completed=e.control.value))

        def enable_edit(_):
            if task_field.read_only:
                task_field.read_only = False
            else:
                task_field.read_only = True

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def on_text_change(e):
            if not task_field.read_only:
                task_field.color = "red"

        task_field.on_change = on_text_change

        def save_task(_):
            main_db.update_task(task_id=task_id,new_task=task_field.value)
            task_field.read_only = True
            task_field.color = None
        
        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        row = ft.Row([])

        delete_button = ft.IconButton(icon=ft.Icons.DELETE,icon_color="red",on_click=lambda e: delete_task(task_id, row))

        text_row = ft.Row([task_field,date_text],expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        row.controls = [checkbox_task, text_row, edit_button,save_button,delete_button]

        return row
    
    

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id=task_id,completed=int(is_completed))

    def add_task_db(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task=task)
            print(f'Задача {task} успешно в БД! Его ID - {task_id}')

            tasks = main_db.get_tasks()
            last_task = tasks[-1]
            _, _, _, date = last_task
            task_list.controls.append(view_tasks(task_id=task_id, task_text=task, date=date))
            task_input.value = None
            page.update()


    task_input = ft.TextField(label='Введите задачу', expand=True, on_submit=add_task_db)
    send_button = ft.ElevatedButton('SEND', on_click=add_task_db)

    tasks = main_db.get_tasks()
    for task_id, task_text, completed, date in tasks:
        task_list.controls.append(
            view_tasks(task_id=task_id, task_text=task_text, completed=completed, date=date)
        )
    main_objects = ft.Row([task_input, send_button])

    page.add(main_objects, task_list)


if __name__ == '__main__':
    main_db.init_db()
    ft.app(main)