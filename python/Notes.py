import sqlite3 as sql
from tkinter import *
from tkinter import messagebox

# Создание подключения к базе данных и подключение к таблице
try:
    con = sql.connect('Notes.json')
    cur = con.cursor()
    cur.execute('''CREATE TABLE notes_table
                        (date text, notes_title text, notes text)''')
except Exception:
    print("Connected to table of database")


# Вставить строку данных
def add_notes():
    # Получение входных значений
    today = date_entry.get()
    notes_title = notes_title_entry.get()
    notes = notes_entry.get("1.0", "end-1c")
    # Выдает запрос на поиск пропущенных значений
    if (len(today) <= 0) & (len(notes_title) <= 0) & (len(notes) <= 1):
        messagebox.showerror(message="ВВЕДИТЕ НЕОБХОДИМЫЕ ДАННЫЕ")
    else:
        # Вставить в таблицу
        cur.execute("INSERT INTO notes_table VALUES ('%s','%s','%s')" % (today, notes_title, notes))
        messagebox.showinfo(message="Заметка добавлена")
        # Фиксация изменения
        con.commit()


# Отображение заметки
def view_notes():
    # Получить все вводимые пользователем данные
    date = date_entry.get()
    notes_title = notes_title_entry.get()
    # Если входные данные не заданы, извлечь все заметки
    if (len(date) <= 0) & (len(notes_title) <= 0):
        sql_statement = "SELECT * FROM notes_table"

    # Извлечь заметки, соответствующие названию
    elif (len(date) <= 0) & (len(notes_title) > 0):
        sql_statement = "SELECT * FROM notes_table where notes_title ='%s'" % notes_title
    # Извлечь заметки, соответствующие дате
    elif (len(date) > 0) & (len(notes_title) <= 0):
        sql_statement = "SELECT * FROM notes_table where date ='%s'" % date
    # Извлечь заметки, соответствующие дате и названию
    else:
        sql_statement = "SELECT * FROM notes_table where date ='%s' and notes_title ='%s'" % (date, notes_title)

    # Выполните запрос
    cur.execute(sql_statement)
    # Получить все содержимое запроса
    row = cur.fetchall()
    # Проверка
    if len(row) <= 0:
        messagebox.showerror(message="Заметка не найдена")
    else:
        # Вывод заметки
        for i in row:
            messagebox.showinfo(message="Дата: " + i[0] + "\nНазвание: " + i[1] + "\nЗаметка: " + i[2])


# Удаление заметки
def delete_notes():
    # Получение входных значений
    date = date_entry.get()
    notes_title = notes_title_entry.get()
    # Запрос, хочет ли пользователь удалить все заметки
    choice = messagebox.askquestion(message="Вы хотите удалить все заметки?")
    # Если выбрано значение "да", удалите все
    if choice == 'да':
        sql_statement = "DELETE FROM notes_table"
    else:
        # Удалять заметки, соответствующие определенной дате и названию
        if (len(date) <= 0) & (len(notes_title) <= 0):
            # Ошибка при отсутствии входных данных
            messagebox.showerror(message="ВВЕДИТЕ НЕОБХОДИМЫЕ ДАННЫЕ")
            return
        else:
            sql_statement = "DELETE FROM notes_table where date ='%s' and notes_title ='%s'" % (date, notes_title)
    # Выполнение запроса
    cur.execute(sql_statement)
    messagebox.showinfo(message="Заметка удалена")
    con.commit()


# Обновление заметки
def update_notes():
    # Получение пользовательских данных
    today = date_entry.get()
    notes_title = notes_title_entry.get()
    notes = notes_entry.get("1.0", "end-1c")
    # Проверка ввода пользователем
    if (len(today) <= 0) & (len(notes_title) <= 0) & (len(notes) <= 1):
        messagebox.showerror(message="ВВЕДИТЕ НЕОБХОДИМЫЕ ДАННЫЕ")
    # Обновление заметки
    else:
        sql_statement = "UPDATE notes_table SET notes = '%s' where date ='%s' and notes_title ='%s'" % (
            notes, today, notes_title)

    cur.execute(sql_statement)
    messagebox.showinfo(message="Заметка обновлена")
    con.commit()


# Вызов класса для просмотра окна
window = Tk()
# Установка размеров окна и заголовка
window.geometry("500x280")
window.title("ЗАМЕТКИ")

title_label = Label(window, text="Запишите свою заметку").pack()
# Считывание входных данных
# Ввод даты
date_label = Label(window, text="Дата:").place(x=10, y=20)
date_entry = Entry(window, width=20)
date_entry.place(x=50, y=20)
# Ввод названия заметок
notes_title_label = Label(window, text="Название:").place(x=10, y=50)
notes_title_entry = Entry(window, width=30)
notes_title_entry.place(x=80, y=50)
# Ввод заметок
notes_label = Label(window, text="Записи:").place(x=10, y=90)
notes_entry = Text(window, width=50, height=6)
notes_entry.place(x=60, y=90)

# Выполнение функции заметок
button1 = Button(window, text='Добавить заметки', bg='Turquoise', fg='Red', command=add_notes).place(x=10, y=220)
button2 = Button(window, text='Просмотр заметок', bg='Turquoise', fg='Red', command=view_notes).place(x=130, y=220)
button3 = Button(window, text='Удалить заметки', bg='Turquoise', fg='Red', command=delete_notes).place(x=255, y=220)
button4 = Button(window, text='Обновить', bg='Turquoise', fg='Red', command=update_notes).place(x=365, y=220)

# закрываем приложение
window.mainloop()
con.close()
