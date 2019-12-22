import hashlib
import sys
import time
import tkinter as tk  # импорт библиотеки tkinter
from tkinter import ttk, messagebox  # импорт модуля TTk

import psycopg2  # импорт модуля бд


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.currentTable = None
        self.db = db
        self.initUI()

        # self.view_records()

    def Pass(self):
        pass

    def initUI(self):  # главное окно
        self.toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # self.add_img = tk.PhotoImage(file='add.gif')
        # btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.pas, bg='#d7d8e0', bd=0,
        #                             compound=tk.TOP, image=self.add_img)
        # btn_open_dialog.pack(side=tk.LEFT)
        #
        self.availableTables = db.getAvailableTables()
        self.currentUserImg = tk.PhotoImage(file='user.gif')
        self.buttonCurrentUser = tk.Button(self.toolbar, text="Текущий пользователь: " + currentUser, bg='#d7d8e0',
                                           bd=0, image=self.currentUserImg, compound=tk.TOP, command=self.Pass)

        self.buttonCurrentUser.pack(side=tk.LEFT)
        self.changeUserImg = tk.PhotoImage(file='update.gif')
        self.buttonChangeUser = tk.Button(self.toolbar, text="Сменить пользователя", bg='#d7d8e0', bd=0,
                                          image=self.changeUserImg, compound=tk.TOP, command=self.changeUser)

        self.buttonChangeUser.pack(side=tk.LEFT)
        self.refreshImg = tk.PhotoImage(file='refresh.png')
        self.buttonRefresh = tk.Button(self.toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refreshImg,
                                       compound=tk.TOP, command=self.refresh)
        self.buttonRefresh.pack(side=tk.LEFT)

        self.listBox = tk.Listbox(self.toolbar, height=5, width=16)
        for i in self.availableTables:
            self.listBox.insert(tk.END, i)
        self.listBox.pack(side=tk.RIGHT)

        self.searchImg = tk.PhotoImage(file='search.gif')
        self.buttonSerch = tk.Button(self.toolbar, text='Посмотреть', bg='#d7d8e0', bd=0, image=self.searchImg,
                                     compound=tk.TOP, command=self.showDb)
        self.buttonSerch.pack(side=tk.RIGHT)

        self.deleteImg = tk.PhotoImage(file='delete.png')
        self.buttonDelete = tk.Button(self.toolbar, text='Удалить', bg='#d7d8e0', bd=0, image=self.deleteImg,
                                      compound=tk.TOP, command=self.deleteRecord)
        self.buttonDelete.pack(side=tk.RIGHT)

    def deleteRecord(self):
        messagebox.showwarning("Удалять записи может только админ",
                               "Delete давать пользователям не безопасно\n Придётся делать защиту от дурачков")
        try:
            recordIdToDelete = self.tree.selection()[0]
        except:
            return
        recordToDelete = self.tree.item(recordIdToDelete, "values")
        with db.conn:
            cur = db.conn.cursor()
            cur.execute("DELETE from \"{}\" where private_number={}".format(self.currentTable, recordToDelete[0]))
            db.conn.commit()

    def changeUser(self):
        EmployeeAuthRefresh()

    def refresh(self):
        self.buttonCurrentUser.configure(text="Текущий пользователь: " + currentUser)
        for i in range(self.availableTables.__len__()):
            self.listBox.delete(i, tk.END)
        self.availableTables = db.getAvailableTables()
        for i in self.availableTables:
            self.listBox.insert(tk.END, i)
        try:
            currentTable = self.availableTables[self.listBox.curselection()[0]]
        except:
            return
        self.showDb()

    def showDb(self):
        try:
            self.currentTable = self.availableTables[self.listBox.curselection()[0]]
        except:
            return
        with db.conn:
            cur = db.conn.cursor()
            cur.execute("SELECT * from \"{}\"".format(self.currentTable))
            records = cur.fetchall()
            db.conn.commit()
        try:
            self.tree.delete(*self.tree.get_children())
            self.tree.destroy()
        except:
            pass
        if self.currentTable == "employees":
            tables = [" ID ", "ID пиццерии", "Фамилия", "  Имя  ", "Отчество",
                      "Дата рождения", "Должность", "Адрес", "Позиция"]
            self.tree = ttk.Treeview(self, height=25, show='headings', columns=tables)
            [self.tree.column(table, width=table.__len__() * 10, anchor=tk.CENTER) for table in tables]
            [self.tree.heading(table, text=table) for table in tables]
            self.tree.pack()
        [self.tree.insert('', 'end', values=row) for row in records]

    # def records(self, description, costs, total):
    #     self.db.insert_data(description, costs, total)
    #     self.view_records()
    #
    # def update_record(self, description, costs, total):
    #     self.db.c.execute('''UPDATE finance SET description=?, costs=?, total=? WHERE ID=?''',
    #                       (description, costs, total, self.tree.set(self.tree.selection()[0], '#1')))
    #     self.db.conn.commit()
    #     self.view_records()
    #
    # def view_records(self):
    #     self.db.c.execute('''SELECT * FROM finance''')
    #     [self.tree.delete(i) for i in self.tree.get_children()]
    #     [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]
    #
    # def search(self):
    #     self.db.c.execute('''''')
    #
    # def delete_all_records(self):
    #     self.db.c.execute('''DELETE FROM finance''')
    #     self.db.conn.commit()
    #     self.view_records()


#
# class Child(tk.Toplevel):
#     def __init__(self):
#         super().__init__(root)
#         self.init_child()
#         self.view = app
#
#     def init_child(self):
#         self.title('Добавить доходы/расходы')
#         self.geometry('400x220+400+300')
#         self.resizable(False, False)
#
#         label_description = tk.Label(self, text='Наименование:')
#         label_description.place(x=50, y=50)
#         label_select = tk.Label(self, text='Статья дохода/расхода:')
#         label_select.place(x=50, y=80)
#         label_sum = tk.Label(self, text='Сумма:')
#         label_sum.place(x=50, y=110)
#
#         self.entry_description = ttk.Entry(self)
#         self.entry_description.place(x=200, y=50)
#
#         self.entry_money = ttk.Entry(self)
#         self.entry_money.place(x=200, y=110)
#
#         self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])
#         self.combobox.current(0)
#         self.combobox.place(x=200, y=80)
#
#         btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
#         btn_cancel.place(x=300, y=170)
#
#         self.btn_ok = ttk.Button(self, text='Добавить')
#         self.btn_ok.place(x=220, y=170)
#         self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
#                                                                        self.combobox.get(),
#                                                                        self.entry_money.get()))
#
#         self.grab_set()  # перехват всех событий, происходящих в приложении
#         self.focus_set()  # захват и удержание фокуса
#
#
# class Update(Child):
#     def __init__(self):
#         super().__init__()
#         self.init_edit()
#         self.view = app
#
#     def init_edit(self):
#         self.title('Редактировать позицию')
#         btn_edit = ttk.Button(self, text='Редактировать')
#         btn_edit.place(x=205, y=170)
#         btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
#                                                                           self.combobox.get(),
#                                                                           self.entry_money.get()))
#
#         self.btn_ok.destroy()


def hashFunc(s):
    return hashlib.sha3_256(s.encode()).hexdigest()


def sqlFilter(s):
    bads = ["/", "\\", "|", "=", ">", "<", "CREATE", "SELECT", "FROM", "ALL", "*", "!",
            "ALL", "ANY", "BETWEEN", "IN", "LIKE", "OR", "SOME", "(", ")", "&", "^", "%",
            "+", "~", "DROP", "DATEBASE", "KEY", "PRIMARY", "FOREIGN", "null", "DELETE",
            "SET", "DISTINCT", "GROUP BY", ";"]
    for i in bads:
        s = s.replace(i, "").replace(i.lower(), "")
    return s.strip()


hostnameIP = '157.230.19.140'
dbName = "cousedb"
port = "5432"


class EmployeeAuth(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.initUI()

    def initUI(self):
        self.parent.title("Авторизация")
        self.parent.geometry("240x120")

        tk.Label(text="Введите логин:").grid(row=0, column=0, sticky="w")
        tk.Label(text="Введите пароль:").grid(row=1, column=0, sticky="w")

        nameField = tk.Entry(textvariable=self.username)
        passwordField = tk.Entry(textvariable=self.password, show="*")

        nameField.insert(0, "pavel2")
        nameField.grid(row=0, column=1, padx=5, pady=5)
        passwordField.insert(0, "Pavel2108")
        passwordField.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(text="Подключиться",
                  background="#555",
                  foreground="#ccc",
                  padx="10",
                  pady="6",
                  command=self.click
                  ).grid(row=3, column=1, padx=0, pady=20)

    def click(self):
        global conn, connectionFlag, currentUser
        try:
            conn.close()
        except:
            pass
        try:
            conn = psycopg2.connect(
                database=dbName,
                user=self.username.get(),
                password=hashFunc(self.password.get()),
                host=hostnameIP,
                port=port
            )
        except:
            messagebox.showwarning("Неуспешное подключение", "{}:{}".format(hostnameIP, port))
            connectionFlag = False
        else:
            messagebox.showinfo("Успешное подключение", "{}:{}".format(hostnameIP, port))
            connectionFlag = True
            currentUser = self.username.get()


class EmployeeAuthRefresh:
    def __init__(self):
        self.window = tk.Toplevel(root)
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.initUI()

    def initUI(self):
        self.window.title("Авторизация")
        self.window.geometry("240x120")

        tk.Label(self.window, text="Введите логин:").grid(row=0, column=0, sticky="w")
        tk.Label(self.window, text="Введите пароль:").grid(row=1, column=0, sticky="w")

        nameField = tk.Entry(self.window, textvariable=self.username)
        passwordField = tk.Entry(self.window, textvariable=self.password, show="*")

        nameField.insert(0, "pavel2")
        nameField.grid(row=0, column=1, padx=5, pady=5)
        passwordField.insert(0, "Pavel2108")
        passwordField.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.window,
                  text="Подключиться",
                  background="#555",
                  foreground="#ccc",
                  padx="10",
                  pady="6",
                  command=self.click
                  ).grid(row=3, column=1, padx=0, pady=20)

    def click(self):
        global connectionFlag, currentUser
        try:
            db.conn = psycopg2.connect(
                database=dbName,
                user=self.username.get(),
                password=hashFunc(self.password.get()),
                host=hostnameIP,
                port=port
            )
        except:
            messagebox.showwarning("Неуспешное подключение", "{}:{}".format(hostnameIP, port))
            connectionFlag = False
        else:
            messagebox.showinfo("Успешное подключение", "{}:{}".format(hostnameIP, port))
            connectionFlag = True
            currentUser = self.username.get()
            # print(self.username.get())
            # print(db.getAvailableTables())


class DB:
    def __init__(self, conn):
        self.conn = conn
        self.tables = ["employees", "positions", "dish", "dish_ingredients", "dish_orders",
                       "address", "finance", "ingredients", "menu", "orders",
                       "passport", "pizzeria", "producer", "tables",
                       "units", "warehouse"]

    def getAvailableTables(self):
        availableTables = []
        with self.conn:
            cur = self.conn.cursor()
            for table in self.tables:
                try:
                    cur.execute("SELECT * from \"{}\"".format(table))
                    cur.fetchall()
                    availableTables.append(table)
                except:
                    pass
                finally:
                    self.conn.commit()
        return availableTables

    def cnangeUser(self, conn):
        try:
            self.conn.close()
            self.c.close()
        except:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAA")
        self.conn = conn
        self.c = self.conn.cursor()


def kill():
    time.sleep(1)
    try:
        conn.close()
        sys.exit()
    except:
        sys.exit()


if __name__ == "__main__":
    root = tk.Tk()  # корневое окно программы
    app = EmployeeAuth(root)
    root.mainloop()
    assert connectionFlag, kill()
    db = DB(conn)  # экземпляр класса DB
    # print(db.getAvailableTables())
    root = tk.Tk()  # корневое окно программы
    app = Main(root)
    app.pack()
    root.title("Pizzas")  # название окна
    root.geometry("1000x450+300+200")  # размеры окна
    # root.resizable(False, False)  # фиксация окна по обоим осям
    root.mainloop()  # запуск главного цикла обработки событий
    db.conn.close()
