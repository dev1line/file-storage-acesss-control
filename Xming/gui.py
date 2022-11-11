from tkinter import *
from tkinter import ttk
from getpass import getuser
from tkinter.filedialog import askopenfilename
import pathlib
import os
import tkinter as tk
from call_script import call_transaction
import numpy as np
# import matplotlib
# matplotlib.use('Agg')

def get_file_name(file_path, extension=False):
    """Returns file name from given path
    either with extension or without extension

    :param file_path:
    :param extension:
    :return file_name:
    """
    if not extension:
        file_name = pathlib.Path(file_path).stem

    else:
        file_name = os.path.basename(file_path)

    return file_name


def open_file():
    """
    This function open the file dialog box for choosing the file.
    And then making two buttons : encrypt_button, decrypt_button
    """
    
    username = getuser()
    initialdirectory = "C:/Users/{}".format(username)
    name = askopenfilename(initialdir=initialdirectory,
                           filetypes=[("All Files", "*.*")],
                           title="Choose a file."
                           )
   
    if name:
        file_name = get_file_name(name, extension=True)
        label_upload.config(text=file_name)
       

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        # self.configure(width=100)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar_ = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(xscrollcommand=scrollbar_.set)

        scrollbar.pack(side="right", fill="y", anchor="e")
        canvas.pack(side="top", fill="none", expand=True)
        scrollbar_.pack(side="bottom", fill="x", anchor="s")
   
   
class Table:
     
    def __init__(self, root):
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                if j == 0: 
                    self.e = Entry(root, width=5, fg='blue',
                                font=('Arial',8,'bold'))
                    self.e.grid(row=i, column=j)
              
                elif j == int(total_columns - 1):
                    self.e = Entry(root, width=50, fg='blue',
                                font=('Arial',8,'bold'))
                    self.e.grid(row=i, column=j, ipadx=5, columnspan=2, sticky=W)
                    
                else:
                    self.e = Entry(root, width=30, fg='blue',
                                font=('Arial',8,'bold'))
                    self.e.grid(row=i, column=j)
                    
                self.e.insert(END, data[i][j])
                
def handle_get():
    id = txt_box.get()
    tx, data = call_transaction("AccessControl", "getFile", [int(id)])
    print(data)
    txt_field.delete(1.0, END)
    txt_field.insert(END, data)
    # txt_field.insert(0, data)

 
# take the data
tx, data = call_transaction("AccessControl", "getMyFiles", [])
lst = [(1,"QmP3cmZ4U942Zfq8tAsuJWvZyMY6umhUYP333vMq6zikyi", "Stephen S"),
       (2,"QmQhq4DBq2EQ7rySwyEBhFkSAv3qTBqhpsh2Vjo82uh5qr", "Stephen S"),
       (3,"QmWvRmjAQX5uETCZ3AzJGSqS8WuW2R5TnJr7z13XPEVJZS", "Stephen S"),
       (4,"QmX2AE68ZToRwns5L5dUacpZeMswjqcnYuuZiBFv8YGUWL", "Stephen S"),
       (1,"QmP3cmZ4U942Zfq8tAsuJWvZyMY6umhUYP333vMq6zikyi", "Stephen S"),
       (2,"QmQhq4DBq2EQ7rySwyEBhFkSAv3qTBqhpsh2Vjo82uh5qr", "Stephen S"),
       (3,"QmWvRmjAQX5uETCZ3AzJGSqS8WuW2R5TnJr7z13XPEVJZS", "Stephen S"),
       (4,"QmX2AE68ZToRwns5L5dUacpZeMswjqcnYuuZiBFv8YGUWL", "Stephen S"),
       (1,"QmP3cmZ4U942Zfq8tAsuJWvZyMY6umhUYP333vMq6zikyi", "Stephen S"),
       (2,"QmQhq4DBq2EQ7rySwyEBhFkSAv3qTBqhpsh2Vjo82uh5qr", "Stephen S"),
       (3,"QmWvRmjAQX5uETCZ3AzJGSqS8WuW2R5TnJr7z13XPEVJZS", "Stephen S"),
       (4,"QmX2AE68ZToRwns5L5dUacpZeMswjqcnYuuZiBFv8YGUWL", "Stephen S"),
       (1,"QmP3cmZ4U942Zfq8tAsuJWvZyMY6umhUYP333vMq6zikyi", "Stephen S"),
       (2,"QmQhq4DBq2EQ7rySwyEBhFkSAv3qTBqhpsh2Vjo82uh5qr", "Stephen S"),
       (3,"QmWvRmjAQX5uETCZ3AzJGSqS8WuW2R5TnJr7z13XPEVJZS", "Stephen S"),
       (4,"QmX2AE68ZToRwns5L5dUacpZeMswjqcnYuuZiBFv8YGUWL", "Stephen S"),
       (1,"QmP3cmZ4U942Zfq8tAsuJWvZyMY6umhUYP333vMq6zikyi", "Stephen S"),
       (2,"QmQhq4DBq2EQ7rySwyEBhFkSAv3qTBqhpsh2Vjo82uh5qr", "Stephen S"),
       (3,"QmWvRmjAQX5uETCZ3AzJGSqS8WuW2R5TnJr7z13XPEVJZS", "Stephen S"),
       (4,"QmX2AE68ZToRwns5L5dUacpZeMswjqcnYuuZiBFv8YGUWL", "Stephen S"),
       (1,"QmP3cmZ4U942Zfq8tAsuJWvZyMY6umhUYP333vMq6zikyi", "Stephen S"),
       (2,"QmQhq4DBq2EQ7rySwyEBhFkSAv3qTBqhpsh2Vjo82uh5qr", "Stephen S"),
       (3,"QmWvRmjAQX5uETCZ3AzJGSqS8WuW2R5TnJr7z13XPEVJZS", "Stephen S"),
       (4,"QmX2AE68ZToRwns5L5dUacpZeMswjqcnYuuZiBFv8YGUWL", "Stephen S"),
       (1,"QmP3cmZ4U942Zfq8tAsuJWvZyMY6umhUYP333vMq6zikyi", "Stephen S"),
       (2,"QmQhq4DBq2EQ7rySwyEBhFkSAv3qTBqhpsh2Vjo82uh5qr", "Stephen S"),
       (3,"QmWvRmjAQX5uETCZ3AzJGSqS8WuW2R5TnJr7z13XPEVJZS", "Stephen S"),
       (4,"QmX2AE68ZToRwns5L5dUacpZeMswjqcnYuuZiBFv8YGUWL", "Stephen S"),
       (5,"QmP3cmZ4U942Zfq8tAsuJWvZyMY6umhUYP333vMq6zikyi", "Stephen S")]
print(data)
# find total number of rows and
# columns in list
if isinstance(data, type(None)) and data != []:
    total_rows = len(lst)
    total_columns = len(lst[0])
else:
    total_rows = len(data)
    total_columns = len(np.asarray(data[0]))


root = Tk()
root.title("FILE STORAGE TOOL");
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# # Evaluating X and Y coordinate such that, window always comes into the center.
# x = int((screen_width / 2) - (app_width / 2))
# y = int((screen_height / 2) - (app_height / 2))
# root.geometry(f"{app_width}x{app_height}+{x}+{y}")
root.resizable(width=False, height=False)  # Window size constant

tabControl = ttk.Notebook(root)
  
mainTab = Frame(tabControl)
whiteListTab = Frame(tabControl)
deployTab = Frame(tabControl)

tabControl.add(mainTab, text ='Main')
tabControl.add(whiteListTab, text ='WhiteList')
tabControl.add(deployTab, text ='Deploy')
tabControl.pack(expand = 1, fill ="both")

# MAIN_TAB
label_txt = Label(mainTab, text="File ID:")
label_txt.grid(row=0, column=1, padx=10, pady=10, sticky=W)
txt_box = Entry(mainTab, width=20)
txt_box.grid(row=0, column=2, padx=5, pady=5, sticky=W)
button_read = Button(mainTab, text="GET FILE", border=1, command=handle_get)
button_read.grid(row=0, column=3, padx=5, pady=10)

label_result = Label(mainTab, text="Result:")
label_result.grid(row=1, column=1, padx=10, sticky=W)
txt_field = Text(mainTab, bg="#d8eded", height=3, width=48, pady=5)
txt_field.grid(row=2, columnspan=4)

label_list = Label(mainTab, text="Your files:")
label_list.grid(row=3, columnspan=3, padx=10, sticky=W)

frame = ScrollableFrame(mainTab)
frame.grid(row=4, columnspan=4)
table = Table(frame.scrollable_frame)

choose_button = Button(mainTab, text="Chose File", command=open_file)
choose_button.grid(row=5, column=1, padx=10, pady=10, sticky=W)
label_upload = Label(mainTab, text="No chosen file ...", wraplength=100)
label_upload.grid(row=5, column=2, columnspan=2, padx=20, sticky=W)
upload_button = ttk.Button(mainTab, text="Upload", command=lambda: message( name, upload_button, mgs_label))
upload_button.grid(row=5, column=3, pady=10, padx=10)

entry_download = Entry(mainTab, width=35) 
entry_download.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky=W)
download_button = ttk.Button(mainTab, text="Download", command=lambda: message( name, download_button, mgs_label))
download_button.grid(row=6, column=3, sticky=E, pady=10, padx=10)

# WHITELIST_TAB
# DEPLOY_TAB
root.mainloop()
