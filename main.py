import flet as ft 
from db import main_db

def main(page: ft.Page):
    page.title = 'Список Покупок'
    page.theme_mode = ft.ThemeMode.DARK

    task_list = ft.Column()

    filter_type = "all"

    def clear_completed(_):

        main_db.delete_completed_tasks()
        new_controls = []

        for row in task_list.controls:
            checkbox = row.controls[0] 
            if not checkbox.value:
                new_controls.append(row)

        task_list.controls = new_controls


    def load_task():
        task_list.controls.clear()
        for task_id, task, completed, counter in main_db.get_tasks(filter_type=filter_type):
            task_list.controls.append(view_tasks(task_id=task_id,task_text=task,completed=completed,counter=counter))

    def delete_task(task_id, row):
            main_db.delete_task(task_id=task_id)  
            task_list.controls.remove(row)        
            page.update()

    def view_tasks(task_id, task_text,completed=None,counter=None):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)


        counter_text = ft.Text(
            value=str(counter if counter is not None else 0),
            width=40
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

        text_row = ft.Row([task_field,counter_text],expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        row.controls = [checkbox_task, text_row, edit_button,save_button,delete_button]

        return row
    
    

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id=task_id,completed=int(is_completed))

    def add_task_db(_):
        if task_input.value:
            task = task_input.value
            counter = int(counter_input.value) if counter_input.value else 1

            task_id = main_db.add_task(task=task, counter=counter)

            task_list.controls.append(
                view_tasks(task_id=task_id, task_text=task, counter=counter)
            )

            task_input.value = None
            counter_input.value = None  
            page.update()

    task_input = ft.TextField(label='Введите название товара', expand=True, on_submit=add_task_db)
    counter_input = ft.TextField(label="Количество", width=100)
    send_button = ft.ElevatedButton('ADD', on_click=add_task_db)

    clear_button = ft.ElevatedButton("Очистить купленные",on_click=clear_completed)
    
    main_objects = ft.Row([task_input,counter_input, send_button, clear_button])

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value

        print(filter_type)
        load_task()

    

    filter_buttons = ft.Row([
        ft.ElevatedButton("Все", on_click=lambda e: set_filter("all")),
        ft.ElevatedButton("Некупленные",on_click=lambda e: set_filter("uncompleted")),
        ft.ElevatedButton("Купленные",on_click=lambda e: set_filter("completed"))
    ],alignment=ft.MainAxisAlignment.SPACE_EVENLY)


    page.add(main_objects,filter_buttons, task_list)
    load_task()

if __name__ == '__main__':
    main_db.init_db()
    ft.app(main)