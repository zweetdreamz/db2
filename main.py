import datetime
import hashlib
import sys
import time
import tkinter as tk  # импорт библиотеки tkinter
from tkinter import ttk, messagebox  # импорт модуля TTk

import psycopg2  # импорт модуля бд


def hashFunc(s):
    return hashlib.sha3_256(s.encode()).hexdigest()


def sqlFilter(s):
    bads = ["/", "\\", "|", "=", ">", "<", "CREATE", "SELECT", "FROM", "ALL", "*", "!",
            "ALL", "ANY", "BETWEEN", "IN", "LIKE", "OR", "SOME", "(", ")", "&", "^", "%",
            "+", "~", "DROP", "DATEBASE", "KEY", "PRIMARY", "FOREIGN", "null", "DELETE",
            "SET", "DISTINCT", "GROUP BY", ";"]
    for i in bads:
        s = s.replace(i, "").replace(i.lower(), "").replace(i.title(), "")
    return s.strip()


hostnameIP = '157.230.19.140'
dbName = "cousedb"
port = "5432"


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

        self.saveImg = tk.PhotoImage(file='save.png')
        self.buttonSave = tk.Button(self.toolbar, text='Сохранить', bg='#d7d8e0', bd=0, image=self.saveImg,
                                    compound=tk.TOP, command=self.save)
        self.buttonSave.pack(side=tk.LEFT)

        self.listBox = tk.Listbox(self.toolbar, height=5, width=16)
        for i in self.availableTables:
            self.listBox.insert(tk.END, i)
        self.listBox.pack(side=tk.RIGHT)

        self.searchImg = tk.PhotoImage(file='search.gif')
        self.buttonSerch = tk.Button(self.toolbar, text='Посмотреть', bg='#d7d8e0', bd=0, image=self.searchImg,
                                     compound=tk.TOP, command=self.showDb)
        self.buttonSerch.pack(side=tk.RIGHT)

        self.addImg = tk.PhotoImage(file='plus.png')
        self.buttonAdd = tk.Button(self.toolbar, text='Добавить', bg='#d7d8e0', bd=0, image=self.addImg,
                                   compound=tk.TOP, command=self.addRecord)
        self.buttonAdd.pack(side=tk.RIGHT)

        self.deleteImg = tk.PhotoImage(file='delete.png')
        self.buttonDelete = tk.Button(self.toolbar, text='Удалить', bg='#d7d8e0', bd=0, image=self.deleteImg,
                                      compound=tk.TOP, command=self.deleteRecord)
        self.buttonDelete.pack(side=tk.RIGHT)

    def save(self):
        try:
            self.currentTable = self.availableTables[self.listBox.curselection()[0]]
        except:
            return
        if self.currentTable == "employees":
            tables = [" ID ", "Номер пиццерии", "Фамилия", "  Имя  ", "Отчество",
                      "Дата рождения", "Количество рабочих часов", "Должность", "Адрес"]
            with db.conn:
                cur = db.conn.cursor()
                cur.execute("""select private_number, pizzeria_number, surname, name, patronymic, birth_date, 
                                work_quota, positions.position_name, address.town, address.street, address.house_number, 
                                address.structure, address.housing, address.apart_office from employees
                                left join address ON address.address_number = employees.address
                                left join positions on positions.position = employees.position
                                order by private_number""")
                records = cur.fetchall()
                db.conn.commit()
            newRecords = []
            for i in [list(j) for j in records]:
                tmp = i[0:8]
                tmp.append(" ".join(list(filter(lambda x: x != "None", map(str, i[8:])))))
                newRecords.append(tmp)
            f = open("{}.csv".format(self.currentTable), "w+")
            f.write(";".join(tables))
            f.write("\n")
            for rec in newRecords:
                f.write(";".join(list(map(str, rec))))
                f.write("\n")
            f.close()
        if self.currentTable == "orders":
            tables = ["Номер заказа", "Номер пиццерии", "Имя сотрудника", "Фамилия сотрудника", "Время заказа",
                      "Дата заказа", "Стоимость", "Название блюда"]
            with db.conn:
                cur = db.conn.cursor()
                cur.execute("""select orders.order_number, orders.pizzeria_number, employees.name, employees.surname, 
                                closing_time, orders.date, orders.price, dish.dish_name from orders
                                left join employees on employees.private_number = orders.employee
                                left join dish_orders on dish_orders.order_number = orders.order_number
                                left join dish on dish_orders.dish_number = dish.dish_number""")
                records = cur.fetchall()
                db.conn.commit()
                f = open("{}.csv".format(self.currentTable), "w+")
                f.write(";".join(tables))
                f.write("\n")
                summ = sum([i[-2] for i in records])
                for rec in records:
                    f.write(";".join(list(map(str, rec))))
                    f.write("\n")

                f.write(";;;;;Общая Сумма;{}".format(summ))
                f.close()
    def deleteRecord(self):
        messagebox.showwarning("Удалять записи может только админ",
                               "Delete давать пользователям не безопасно\nПридётся делать защиту от дурачков")

    def addRecord(self):
        AddRecord()

    def changeUser(self):
        EmployeeAuthRefresh()
        self.refresh()

    def refresh(self):
        self.buttonCurrentUser.configure(text="Текущий пользователь: " + currentUser)
        for i in range(self.availableTables.__len__()):
            self.listBox.delete(i, tk.END)
        self.availableTables = db.getAvailableTables()
        for i in self.availableTables:
            self.listBox.insert(tk.END, i)
        self.showDb()

    def showDb(self):
        try:
            self.currentTable = self.availableTables[self.listBox.curselection()[0]]
        except:
            return
        try:
            self.tree.delete(*self.tree.get_children())
            self.tree.destroy()
        except:
            pass
        if self.currentTable == "employees":
            tables = [" ID ", "Номер пиццерии", "Фамилия", "  Имя  ", "Отчество",
                      "Дата рождения", "Количество рабочих часов", "Должность", "Адрес"]
            with db.conn:
                cur = db.conn.cursor()
                cur.execute("""select private_number, pizzeria_number, surname, name, patronymic, birth_date, 
                                work_quota, positions.position_name, address.town, address.street, address.house_number, 
                                address.structure, address.housing, address.apart_office from employees
                                left join address ON address.address_number = employees.address
                                left join positions on positions.position = employees.position
                                order by private_number""")
                records = cur.fetchall()
                db.conn.commit()
            newRecords = []
            for i in [list(j) for j in records]:
                tmp = i[0:8]
                tmp.append(" ".join(list(filter(lambda x: x != "None", map(str, i[8:])))))
                newRecords.append(tmp)
            self.tree = ttk.Treeview(self, height=25, show='headings', columns=tables)
            [self.tree.column(table, width=table.__len__() * 8, anchor=tk.CENTER) for table in tables]
            [self.tree.heading(table, text=table) for table in tables]
            self.tree.pack()
            [self.tree.insert('', 'end', values=row) for row in newRecords]
        if self.currentTable == "address":
            tables = ["ID", "Город", "Улица", "Номер дома", "Корпус", "Строение", "Номер квартиры/офиса"]

        if self.currentTable == "dish":
            tables = ["ID", "Название", "Цена", "Вес"]

        if self.currentTable == "dish_ingredients":
            tables = ["ID", "Номер блюда", "Ингредиент", "Количество в блюде", "Единицы измерения"]

        if self.currentTable == "dish_orders":
            tables = ["ID", "Номер блюда", "Номер заказа"]

        if self.currentTable == "ingredients":
            tables = ["ID", "Название", "Калорийность", "Белки", "Жиры", "Углеводы",
                      "Количество на складе", "Единицы измения"]

        if self.currentTable == "menu":
            tables = ["ID", "Номер пиццерии", "Блюдо", "Наличие"]

        if self.currentTable == "orders":
            tables = ["Номер заказа", "Номер пиццерии", "Имя сотрудника", "Фамилия сотрудника", "Время заказа",
                      "Дата заказа", "Стоимость", "Название блюда"]
            with db.conn:
                cur = db.conn.cursor()
                cur.execute("""select orders.order_number, orders.pizzeria_number, employees.name, employees.surname, 
                                closing_time, orders.date, orders.price, dish.dish_name from orders
                                left join employees on employees.private_number = orders.employee
                                left join dish_orders on dish_orders.order_number = orders.order_number
                                left join dish on dish_orders.dish_number = dish.dish_number""")
                records = cur.fetchall()
                db.conn.commit()
            newRecords = []
            self.tree = ttk.Treeview(self, height=25, show='headings', columns=tables)
            [self.tree.column(table, width=table.__len__() * 10, anchor=tk.CENTER) for table in tables]
            [self.tree.heading(table, text=table) for table in tables]
            self.tree.pack()
            [self.tree.insert('', 'end', values=row) for row in records]

        if self.currentTable == "passport":
            tables = ["Серия", "Номер", "Владелец", "Место выдачи", "Дата выдачи"]

        if self.currentTable == "pizzeria":
            tables = ["Номер", "Адрес", "Время начала работы", "Время окончания работы"]
        if self.currentTable == "positions":
            tables = ["ID", "Должность", "Зарплата"]
        if self.currentTable == "producer":
            tables = ["Номер договора", "Цена", "Продукт"]
        if self.currentTable == "tables":
            tables = ["Номер стола", "Номер пиццерии", "Занятость", "Время начала резерва", "Время окончания резерва"]
        if self.currentTable == "units":
            tables = ["ID", "Название"]
        if self.currentTable == "warehouse":
            tables = ["ID", "Номер пиццерии", "Производитель"]


class AddRecord:
    def __init__(self):
        self.window = tk.Toplevel(root)
        self.v1 = tk.StringVar()
        self.v2 = tk.StringVar()
        self.v3 = tk.StringVar()
        self.v4 = tk.StringVar()
        self.v5 = tk.StringVar()
        self.v6 = tk.StringVar()
        self.v7 = tk.StringVar()
        self.v8 = tk.StringVar()
        self.v9 = tk.StringVar()
        self.v10 = tk.StringVar()
        self.v11 = tk.StringVar()
        self.v12 = tk.StringVar()
        self.v13 = tk.StringVar()
        self.v14 = tk.StringVar()
        self.initUI()

    def initUI(self):
        if app.currentTable == "employees":
            self.window.title("Добавить запись")
            self.window.geometry("300x480")

            tk.Label(self.window, text="Имя:").grid(row=0, column=0, sticky="w")
            tk.Label(self.window, text="Фамилия:").grid(row=1, column=0, sticky="w")
            tk.Label(self.window, text="Отчество:").grid(row=2, column=0, sticky="w")
            tk.Label(self.window, text="Дата рождения:").grid(row=3, column=0, sticky="w")
            tk.Label(self.window, text="Количество рабочих часов:").grid(row=4, column=0, sticky="w")
            tk.Label(self.window, text="Город:").grid(row=5, column=0, sticky="w")
            tk.Label(self.window, text="Улица:").grid(row=6, column=0, sticky="w")
            tk.Label(self.window, text="Дом:").grid(row=7, column=0, sticky="w")
            tk.Label(self.window, text="Корпус:").grid(row=8, column=0, sticky="w")
            tk.Label(self.window, text="Строение:").grid(row=9, column=0, sticky="w")
            tk.Label(self.window, text="Квартира:").grid(row=10, column=0, sticky="w")
            tk.Label(self.window, text="Должность:").grid(row=11, column=0, sticky="w")
            tk.Label(self.window, text="Зарплата:").grid(row=12, column=0, sticky="w")
            tk.Label(self.window, text="Пароль:").grid(row=13, column=0, sticky="w")

            self.v1f = tk.Entry(self.window, textvariable=self.v1)
            self.v2f = tk.Entry(self.window, textvariable=self.v2)
            self.v3f = tk.Entry(self.window, textvariable=self.v3)
            self.v4f = tk.Entry(self.window, textvariable=self.v4)
            self.v5f = tk.Entry(self.window, textvariable=self.v5)
            self.v6f = tk.Entry(self.window, textvariable=self.v6)
            self.v7f = tk.Entry(self.window, textvariable=self.v7)
            self.v8f = tk.Entry(self.window, textvariable=self.v8)
            self.v9f = tk.Entry(self.window, textvariable=self.v9)
            self.v10f = tk.Entry(self.window, textvariable=self.v10)
            self.v11f = tk.Entry(self.window, textvariable=self.v11)
            self.v12f = tk.Entry(self.window, textvariable=self.v12)
            self.v13f = tk.Entry(self.window, textvariable=self.v13)
            self.v14f = tk.Entry(self.window, textvariable=self.v14)

            self.v1f.insert(0, "")
            self.v1f.grid(row=0, column=1, padx=5, pady=5)
            self.v2f.insert(0, "")
            self.v2f.grid(row=1, column=1, padx=5, pady=5)
            self.v3f.insert(0, "")
            self.v3f.grid(row=2, column=1, padx=5, pady=5)
            self.v4f.insert(0, "")
            self.v4f.grid(row=3, column=1, padx=5, pady=5)
            self.v5f.insert(0, "")
            self.v5f.grid(row=4, column=1, padx=5, pady=5)
            self.v6f.insert(0, "")
            self.v6f.grid(row=5, column=1, padx=5, pady=5)
            self.v7f.insert(0, "")
            self.v7f.grid(row=6, column=1, padx=5, pady=5)
            self.v8f.insert(0, "")
            self.v8f.grid(row=7, column=1, padx=5, pady=5)
            self.v9f.insert(0, "")
            self.v9f.grid(row=8, column=1, padx=5, pady=5)
            self.v10f.insert(0, "")
            self.v10f.grid(row=9, column=1, padx=5, pady=5)
            self.v11f.insert(0, "")
            self.v11f.grid(row=10, column=1, padx=5, pady=5)
            self.v12f.insert(0, "")
            self.v12f.grid(row=11, column=1, padx=5, pady=5)
            self.v13f.insert(0, "")
            self.v13f.grid(row=12, column=1, padx=5, pady=5)
            self.v14f.insert(0, "")
            self.v14f.grid(row=13, column=1, padx=5, pady=5)

        if app.currentTable == "orders":
            self.window.title("Добавить запись")
            self.window.geometry("250x260")

            tk.Label(self.window, text="Номер пиццерии:").grid(row=0, column=0, sticky="w")
            tk.Label(self.window, text="Номер сотрудника:").grid(row=1, column=0, sticky="w")
            tk.Label(self.window, text="Время:").grid(row=2, column=0, sticky="w")
            tk.Label(self.window, text="Цена:").grid(row=3, column=0, sticky="w")
            tk.Label(self.window, text="Дата:").grid(row=4, column=0, sticky="w")
            tk.Label(self.window, text="Номер блюда:").grid(row=5, column=0, sticky="w")

            self.v1f = tk.Entry(self.window, textvariable=self.v1)
            self.v2f = tk.Entry(self.window, textvariable=self.v2)
            self.v3f = tk.Entry(self.window, textvariable=self.v3)
            self.v4f = tk.Entry(self.window, textvariable=self.v4)
            self.v5f = tk.Entry(self.window, textvariable=self.v5)
            self.v6f = tk.Entry(self.window, textvariable=self.v6)

            self.v1f.insert(0, "1")
            self.v1f.grid(row=0, column=1, padx=5, pady=5)
            self.v2f.insert(0, "1")
            self.v2f.grid(row=1, column=1, padx=5, pady=5)
            self.v3f.insert(0, datetime.datetime.now().__str__().split(" ")[1].split(".")[0])
            self.v3f.grid(row=2, column=1, padx=5, pady=5)
            self.v4f.insert(0, "650")
            self.v4f.grid(row=3, column=1, padx=5, pady=5)
            self.v5f.insert(0, datetime.date.today().__str__())
            self.v5f.grid(row=4, column=1, padx=5, pady=5)
            self.v6f.insert(0, "4")
            self.v6f.grid(row=5, column=1, padx=5, pady=5)


        tk.Button(self.window,
                  text="Добавить",
                  background="#555",
                  foreground="#ccc",
                  padx="10",
                  pady="6",
                  command=self.click
                  ).grid(row=6, column=1, padx=0, pady=20)

    def click(self):
        if app.currentTable == "orders":
            pizzNum = sqlFilter(self.v1f.get())
            empNum = sqlFilter(self.v2f.get())
            time = sqlFilter(self.v3f.get())
            price = sqlFilter(self.v4f.get())
            date = datetime.date(year=int(sqlFilter(self.v5f.get()).split("-")[0]),
                                 month=int(sqlFilter(self.v5f.get()).split("-")[1]),
                                 day=int(sqlFilter(self.v5f.get()).split("-")[2]))
            dishNum = sqlFilter(self.v6f.get())
            with db.conn:
                cur = db.conn.cursor()
                cur.execute("""select * from add_order(
                                                        {}::integer,
                                                        {}::integer,
                                                        '{}'::time,
                                                        {}::integer,
                                                        '{}'::date,
                                                        {}::integer
                                                        );
                                                         """.format(
                    pizzNum, empNum, time, price, date, dishNum
                ))
                db.conn.commit()

        if app.currentTable == "employees":
            name = sqlFilter(self.v1f.get())
            surname = sqlFilter(self.v2f.get())
            patronic = sqlFilter(self.v3f.get())
            date = datetime.date(year=int(sqlFilter(self.v4f.get()).split(" ")[2]),
                                 month=int(sqlFilter(self.v4f.get()).split(" ")[1]),
                                 day=int(sqlFilter(self.v4f.get()).split(" ")[0]))
            quota = int(sqlFilter(self.v5f.get()))
            town = sqlFilter(self.v6f.get())
            street = sqlFilter(self.v7f.get())
            houseNumber = int(sqlFilter(self.v8f.get()))
            structure = False if sqlFilter(self.v9f.get()) == "" else int(sqlFilter(self.v9f.get()))
            housing = False if sqlFilter(self.v10f.get()) == "" else int(sqlFilter(self.v10f.get()))
            apart = int(sqlFilter(self.v11f.get()))
            position = sqlFilter(self.v12f.get())
            salary = int(sqlFilter(self.v13f.get()))
            password = hashFunc(sqlFilter(self.v14f.get()))

            with db.conn:
                cur = db.conn.cursor()
                if structure and housing:
                    cur.execute("""select * from register_employee(
                                                    1::integer,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    '{}'::date,
                                                    {}::integer ,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    {}::integer,
                                                    {}::integer,
                                                    {}::integer,
                                                    {}::integer,
                                                    '{}'::varchar,
                                                    {}::integer,
                                                    '{}'::varchar
                                                    );
                                                     """.format(
                        name, surname, patronic, date, quota, town, street, houseNumber, structure, housing,
                        apart, position, salary, password
                    ))
                    db.conn.commit()
                elif not structure and not housing:
                    cur.execute("""select * from register_employee(
                                                    1::integer,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    '{}'::date,
                                                    {}::integer ,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    {}::integer,
                                                    NULL,
                                                    NULL,
                                                    {}::integer,
                                                    '{}'::varchar,
                                                    {}::integer,
                                                    '{}'::varchar
                                                    );
                                                     """.format(
                        name, surname, patronic, date, quota, town, street, houseNumber,
                        apart, position, salary, password
                    ))
                    db.conn.commit()
                elif not structure and housing:
                    cur.execute("""select * from register_employee(
                                                    1::integer,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    '{}'::date,
                                                    {}::integer ,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    {}::integer,
                                                    NULL,
                                                    {}::integer,
                                                    {}::integer,
                                                    '{}'::varchar,
                                                    {}::integer,
                                                    '{}'::varchar
                                                    );
                                                     """.format(
                        name, surname, patronic, date, quota, town, street, houseNumber, housing,
                        apart, position, salary, password
                    ))
                    db.conn.commit()
                elif structure and not housing:
                    cur.execute("""select * from register_employee(
                                                    1::integer,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    '{}'::date,
                                                    {}::integer ,
                                                    '{}'::varchar,
                                                    '{}'::varchar,
                                                    {}::integer,
                                                    {}::integer,
                                                    NULL,
                                                    {}::integer,
                                                    '{}'::varchar,
                                                    {}::integer,
                                                    '{}'::varchar
                                                    );
                                                     """.format(
                        name, surname, patronic, date, quota, town, street, houseNumber, structure,
                        apart, position, salary, password
                    ))
                    db.conn.commit()


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
                user=sqlFilter(self.username.get()),
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
    root = tk.Tk()  # корневое окно программы
    app = Main(root)
    app.pack()
    root.title("Pizzas")  # название окна
    root.geometry("1000x450+300+200")  # размеры окна
    # root.resizable(False, False)  # фиксация окна по обоим осям
    root.mainloop()  # запуск главного цикла обработки событий
    db.conn.close()
