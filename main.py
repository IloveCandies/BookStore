import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime


#Главная форма
class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_objects()


      
   
    def init_main(self):
       
        
        toolbar = tk.Frame(bg='#d7d8e0',bd=2,width = 800, height=1)
        toolbar.pack(side=tk.TOP,fill=tk.X)

        btn_open_dialog = tk.Button(toolbar,text='Добавить',command=self.open_dialog,bg='#d7d8e0',bd=0,compound=tk.TOP)
        btn_open_dialog_delete = tk.Button(toolbar, text='Удалить', command=self.open_dialog_delete, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP,)
        btn_show_all = tk.Button(toolbar, text='Обновить', command=self.view_objects_all, bg='#d7d8e0', bd=0,
                                   compound=tk.TOP,)
    
        btn_open_dialog.pack(side=tk.LEFT)
        btn_open_dialog_delete.pack(side=tk.LEFT)
        btn_search.pack(side=tk.LEFT)
        btn_show_all.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self,columns=('ID','title','author','cost','quantity','price','date'),height=19, show='headings',selectmode='browse')
        self.tree.column("ID",minwidth=30,width=30,anchor=tk.CENTER)
        self.tree.column("title",minwidth=200,width=200,anchor=tk.CENTER)
        self.tree.column("author",minwidth=150,width=150,anchor=tk.CENTER)
        self.tree.column("cost",minwidth=160,width=160,anchor=tk.CENTER)
        self.tree.column("quantity",minwidth=100,width=100,anchor=tk.CENTER)
        self.tree.column("date",minwidth=100,width=100,anchor=tk.CENTER)
        self.tree.column("price",minwidth=100,width=100,anchor=tk.CENTER)
        self.tree.heading("ID",text='ID')
        self.tree.heading("title",text='Название')
        self.tree.heading("author",text='Автор')
        self.tree.heading("cost",text='Цена за единицу (₽)')
        self.tree.heading("quantity",text='Количество')
        self.tree.heading("date",text='Дата')
        self.tree.heading("price",text='Итого (₽)')
        
        self.tree.pack(side=tk.TOP,fill=tk.X)

        self.item_search = ttk.Entry(self, width = 117)
        self.item_search.place(x=2,y=384)
        self.a = self.item_search.get()
        self.btn_ok = ttk.Button(self,text='Поиск',width = 20,)
        self.btn_ok.bind('<Button-1>',lambda event: self.view_objects_search(self.item_search.get()))
        self.btn_ok.place(x=712,y=381) 
    
    def objects(self,title,author,quantity,cost,date):
        self.db.add_object(title,author,quantity,cost,date)
        self.view_objects()

    def delete_objects(self,num):
        self.db.delete_id(num)
        self.view_objects_delete()
    
    def view_objects_search(self,item):
        self.db.c.execute('''SELECT * FROM book WHERE ((title  LIKE ? )OR (author LIKE ?)OR (date LIKE ?))''',[item,item,item] )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row) for row in self.db.c.fetchall()]

    def view_objects_all(self):
        self.db.c.execute("SELECT * FROM book")
        [self.tree.delete(i) for i in self.tree.get_children()] 
        [self.tree.insert('','end',values=row) for row in self.db.c.fetchall()]
    
    def view_objects_delete(self):
        self.db.c.execute("SELECT * FROM book")  
        [self.tree.delete(i) for i in self.tree.get_children()] 
        [self.tree.insert('','end',values=row) for row in self.db.c.fetchall()]  


    def view_objects(self):
        self.db.c.execute("SELECT * FROM book")  
        [self.tree.delete(i) for i in self.tree.get_children()]  
        [self.tree.insert('','end',values=row) for row in self.db.c.fetchall()]  

    def open_dialog_delete(self):
        DeleteObject()    
    
    def open_dialog(self):
        AddObjectForm()



def testVal(inStr,acttyp):
    if acttyp == '1': 
        if not inStr.isdigit():
            return False
    return True

def testVa2(inStr,acttyp):
    if acttyp == '1': 
        if not inStr.isint():
            return False
    return True



class AddObjectForm(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.view=app
        self.init_child()

    def init_child(self):

        self.geometry('500x220+450+300')
        self.resizable(False,False)
        self.title('Добавить запись')
        label_title = tk.Label(self,text='Наименование:')

        label_title.place(x=10,y=20)
        label_select = tk.Label(self,text='Автор')
        label_select.place(x=10,y=50)
        label_cost = tk.Label(self,text='Цена за единицу (₽):')
        label_cost.place(x=10,y=80)
        label_quantity = tk.Label(self,text='Количество:')
        label_quantity.place(x=10,y=110)
        label_data_production = tk.Label(self,text='Год изготовления:')
        label_data_production.place(x=10,y=140)

        self.entry_title = ttk.Entry(self)
        self.entry_title.place(x=160,y=20, width = '330')
        self.author =  ttk.Entry(self)
        self.author.place(x=160,y=50, width = '330')
        self.cost = ttk.Entry(self,validate="key")
        self.cost['validatecommand']=(self.cost.register(testVal),'%P','%d')
        self.cost.place(x=160,y=80, width = '330')

        self.quantity = ttk.Entry(self,validate="key")
        self.quantity['validatecommand']=(self.quantity.register(testVal),'%P','%d')
        self.quantity.place(x=160,y=110, width = '330')

        self.date = ttk.Entry(self,validate="key")
        self.date['validatecommand']=(self.date.register(testVal),'%P','%d')
        self.date.place(x=160, y=140, width = '330')   

        btn_cancel = ttk.Button(self,text='Отмена',command=self.destroy)
        btn_cancel.place(x=10,y=190, width = '480')
        btn_ok = ttk.Button(self,text='OK',command=self.destroy)
        btn_ok.place(x=10,y=170, width = '480') 
        btn_ok.bind('<Button-1>',lambda event: self.view.objects(self.entry_title.get(),
                                                                    self.author.get(),
                                                                    self.cost.get(),     
                                                                    self.quantity.get(),
                                                                    self.date.get()))
        
        self.grab_set()
        self.focus_set()



class DeleteObject(tk.Toplevel):

    def __init__(self):
        super().__init__(root)
        self.db = db
        self.view=app
        self.init_child()

    def init_child(self):
        self.title('Удалить запись')
        self.geometry('400x150+400+350')
        self.resizable(False,False)
        label_num = tk.Label(self,text='Введите ID:')
        label_num.place(x=50,y=50)
        self.entry_num = ttk.Entry(self)
        self.entry_num.place(x=200,y=50)
        btn_cancel = ttk.Button(self,text='Отмена',command=self.destroy)
        btn_cancel.place(x=210,y=100)
        btn_ok = ttk.Button(self,text='Удалить',command=self.destroy)
        btn_ok.place(x=130,y=100)
        btn_ok.bind('<Button-1>',lambda event: self.view.delete_objects(self.entry_num.get()))
        
        self.grab_set()
        self.focus_set()

class DB: 
    def __init__(self):
        self.conn = sqlite3.connect('book.db',detect_types = sqlite3.PARSE_DECLTYPES)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS book (id integer primary key,title text,author text,cost real,quantity real,total_cost real,date int)''')
        self.conn.commit()

    def delete_id(self,num):
        self.c.execute('''DELETE FROM book WHERE id = (?)''',(num) )
        self.conn.commit()

    def add_object(self, title,author,cost,quantity,date):
        total_cost = int(cost)*int(quantity)#Расчёт итоговой стоимости
        self.c.execute('''INSERT INTO book(title,author,cost,quantity,total_cost,date) VALUES (?,?,?,?,?,?)''',(title,author,cost,quantity,total_cost,date))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Библиотека")
    root.geometry("860x460+300+200")
    root.resizable(False,False)
    root.mainloop()
