from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Cryptography.hybrid_encryption import *
from getpass import getuser
from tkinter.filedialog import askopenfilename
import pathlib
import os
import tkinter as tk
from call_script import call_transaction, store_file_ipfs, get_file_ipfs, my_address
import numpy as np
# import matplotlib
# matplotlib.use('Agg')

# Config DISPLAY to run Xming
os.environ["DISPLAY"] = "localhost:0.0"
src_file = ""
src_wl = ""
data = []
wl = []
calc = lambda x : x if(x > 0) else 0
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


def open_file(label, button):
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

    if button["text"] == "Chose File":
        global src_file
        src_file = name
        print("src_file", src_file)
    if button["text"] == "Whitelist":
        global src_wl
        src_wl = name
        print("src_wl", src_wl)
    print("button", button["text"])
    print("src_file 0", src_file)
    print("src_wl 0", src_wl)
    if name:
        file_name = get_file_name(name, extension=True)
        label.config(text=file_name)
       

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
     
    def __init__(self, root, data, dimensional):
        # code for creating table
        if dimensional == 1:   
            for widgets in root.winfo_children():
                widgets.destroy()  
            for i in range(len(data)):  
                self.e = Entry(root, width=50, fg='blue',
                            font=('Arial',8,'bold'))
                self.e.grid(row=i, column=1, ipadx=5, columnspan=2, sticky=W)
                self.e.insert(END, data[i])
                # self.e.configure(state=DISABLED)
        elif dimensional == 2:
            for i in range(len(data)):
                for j in range(calc(len(np.asarray(data[0])))):
                    
                    if j == 0: 
                        self.e = Entry(root, width=5, fg='blue',
                                    font=('Arial',8,'bold'))
                        self.e.grid(row=i, column=j)
                
                    elif j == int(calc(len(np.asarray(data[0]))) - 1):
                        self.e = Entry(root, width=50, fg='blue',
                                    font=('Arial',8,'bold'))
                        self.e.grid(row=i, column=j, ipadx=5, columnspan=2, sticky=W)
                        
                    else:
                        self.e = Entry(root, width=30, fg='blue',
                                    font=('Arial',8,'bold'))
                        self.e.grid(row=i, column=j)
                        
                    self.e.insert(END, data[i][j])
                    # self.e.configure(state=DISABLED)
    def update(self,root, data):
       
        for i in range(len(data)):
            for j in range(calc(len(np.asarray(data[0])))):
                
                self.e.delete(0, END)
                if self.e.grid_info() == {}:
                    if j == 0: 
                        self.e = Entry(root, width=5, fg='blue', 
                                    font=('Arial',8,'bold'))
                        self.e.grid(row=i, column=j)
                        
                
                    elif j == int(calc(len(np.asarray(data[0]))) - 1):
                        self.e = Entry(root, width=50, fg='blue', 
                                    font=('Arial',8,'bold'))
                        self.e.grid(row=i, column=j, ipadx=5, columnspan=2, sticky=W)
                        

                    else:
                        self.e = Entry(root, width=30, fg='blue', 
                                    font=('Arial',8,'bold'))
                        self.e.grid(row=i, column=j)
                # else:
                #     self.e.configure(state=NORMAL)       

                self.e.insert(END, data[i][j])
                # self.e.configure(state=DISABLED) 
                
def handle_get():
    txt_field.configure(state=NORMAL)
    id = txt_box.get()
    tx, data = call_transaction("AccessControl", "getFile", [int(id)])
    print(data)
    txt_field.delete(1.0, END)
    txt_field.insert(END, data)
    txt_field.configure(state=DISABLED)
    # messagebox.showinfo("MessageBox")
def handle_get_wl():
    id = txt_box_w.get()
    tx, data = call_transaction("AccessControl", "getAuthorizedUsersOf", [int(id)])
    print(data)
    global wl
    wl = data
    global table_w
    table_w = Table(frame_w.scrollable_frame, wl, 1)
    # table.update(frame.scrollable_frame, data)
    # messagebox.showinfo("Transaction", "Upload sucess")

def handle_upload():
    print("Name file", src_file)
    
    split_tup = os.path.splitext(label_upload.cget("text"))
    print(split_tup)
    
    # extract the file name and extension
    file_name = split_tup[0]
    file_extension = split_tup[1]
    encryption(src_file)
    upload_file = default_path + f"/{file_name}{file_extension}.enc"
    print("upload_file", upload_file)
    file_link = store_file_ipfs(upload_file)

    print("File Name: ", file_name)
    print("File Extension: ", file_extension)
    whitelist = []
    print("src_wl", src_wl)
    with open(f'{src_wl}', mode='r', encoding="utf-8") as in_file:
        for address in in_file:
            whitelist.append(address.strip())
    # response = call_transaction("FileStorage", "getCurrentId", [])
    # whitelist = ["0xc1DcFCB34d21259088924565A6342513Ba987948", "0x29365F5865cEDcee38DcF4CB6A97F806bFd195f1"]
    params = [file_extension, file_name, file_link, whitelist, bytes(f"private_metadata", 'utf-8')]
    rs = call_transaction("AccessControl", "createFile", params)
    
    load_data()
    global table
    table = Table(frame.scrollable_frame, data, 2)
    # table.update(frame.scrollable_frame, data)
    messagebox.showinfo("Transaction", "Upload sucess")

def handle_download():
    file_id = entry_download.get()
    file = call_transaction("AccessControl", "getFile", [int(file_id)])
    data = file[1]
    download_file = get_file_ipfs(data[3], data[1])
    decrypted_file = decryption(download_file)
    messagebox.showinfo("Transaction", f"Download success file: {decrypted_file}")
def handle_update():
    file_id = entry_download.get()
    split_tup = os.path.splitext(label_upload.cget("text"))
    print(split_tup)
    
    # extract the file name and extension
    file_name = split_tup[0]
    file_extension = split_tup[1]
    encryption(src_file)
    upload_file = default_path + f"/{file_name}{file_extension}.enc"
    print("upload_file", upload_file)
    file_link = store_file_ipfs(upload_file)

    print("File Name: ", file_name)
    print("File Extension: ", file_extension)
    # whitelist = []
    # with open(f'{src_wl}', mode='r', encoding="utf-8") as in_file:
    #     for address in in_file:
    #         whitelist.append(address.strip())
    # response = call_transaction("FileStorage", "getCurrentId", [])
    # whitelist = ["0xc1DcFCB34d21259088924565A6342513Ba987948", "0x29365F5865cEDcee38DcF4CB6A97F806bFd195f1"]
    file_info = (int(file_id), file_extension, file_name, file_link, bytes(f"private_metadata", 'utf-8'), my_address)
    params = [int(file_id), file_info]
    rs = call_transaction("AccessControl", "updateFile", params)

    load_data()
    global table
    table = Table(frame.scrollable_frame, data, 2)
    # table.update(frame.scrollable_frame, data)
    messagebox.showinfo("Transaction", "Update sucess")

def handle_delete():
    file_id = entry_download.get()
    params = [int(file_id)]
    rs = call_transaction("AccessControl", "deleteFile", params)

    load_data()
    global table
    table = Table(frame.scrollable_frame, data, 2)
    # table.update(frame.scrollable_frame, data)
    messagebox.showinfo("Transaction", "Delete sucess")

def handle_add_whitelist():
    file_id = entry_file_wl.get()
    authorized_user = auth_user.get()
    params = [int(file_id), authorized_user]
    call_transaction("AccessControl", "addAuthorizedUser", params)
    handle_get_wl()
    messagebox.showinfo("Transaction", "Add sucess")

def handle_remove_whitelist():
    file_id = entry_file_wl.get()
    authorized_user = auth_user.get()
    params = [int(file_id), authorized_user]
    call_transaction("AccessControl", "removeAuthorizedUser", params)
    handle_get_wl()
    messagebox.showinfo("Transaction", "Remove sucess")

def load_data():
    # take the data
    print(my_address)
    global data
    list = call_transaction("AccessControl", "getMyFiles", [])
    data = list[1]
    print(data)
    # global txt_field
    # txt_field.delete(1.0, END)
    # txt_field.insert(END, data)
    

load_data()
# find total number of rows and
# columns in list
# if isinstance(data, type(None)) and data != []:
#     total_rows = 0
#     total_columns = 0
# else:
#     total_rows = len(data)
#     total_columns = calc(len(np.asarray(data[0])))


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
# deployTab = Frame(tabControl)

tabControl.add(mainTab, text ='Main')
tabControl.add(whiteListTab, text ='WhiteList')
# tabControl.add(deployTab, text ='Deploy')
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
table = Table(frame.scrollable_frame, data, 2)


choose_button = Button(mainTab, text="Chose File", width=7, command=lambda: open_file(label_upload, choose_button))
choose_button.grid(row=5, column=1, padx=10, pady=10, sticky=W)
label_upload = Label(mainTab, text="No chosen file ...", wraplength=100)
label_upload.grid(row=5, column=2, columnspan=2, padx=20, sticky=W)
upload_button = ttk.Button(mainTab, text="Upload", command=handle_upload)
upload_button.grid(row=5, column=3, pady=10, padx=10)

download_button = ttk.Button(mainTab, text="Download", command=handle_download)
download_button.grid(row=6, column=3, sticky=E, pady=10, padx=10)
label_txt = Label(mainTab, text="File ID:")
label_txt.grid(row=6, column=1, padx=10, pady=10, sticky=W)
entry_download = Entry(mainTab, width=20)
entry_download.grid(row=6, column=2, padx=5, pady=5, sticky=W)

whitelist_upload = Button(mainTab, text="Whitelist", width=7, command=lambda: open_file(label_whitelist_file, whitelist_upload))
whitelist_upload.grid(row=7, column=1, padx=10, pady=10, sticky=W)
label_whitelist_file = Label(mainTab, text="No chosen file ...", wraplength=100)
label_whitelist_file.grid(row=7, column=2, columnspan=2, padx=20, sticky=W)
update_button = Button(mainTab, text="Update", width=7, command=handle_update)
update_button.grid(row=7, column=3, padx=10, pady=10)

delete_button = Button(mainTab, text="Delete", width=7, command=handle_delete)
delete_button.grid(row=8, column=3, padx=10, pady=10)

###########################################################################

title_whitelist = Label(whiteListTab, text="WhiteList Action:", font=('Arial',20,'bold'))
title_whitelist.grid(row=0, column=1, columnspan=2, padx=10, pady=15)

label_txt_w = Label(whiteListTab, text="File ID:")
label_txt_w.grid(row=1, column=1, padx=10, pady=10, sticky=W)
txt_box_w = Entry(whiteListTab, width=20)
txt_box_w.grid(row=1, column=2, padx=5, pady=5, sticky=W)
button_read_w = Button(whiteListTab, text="GET Auth Users", border=1, command=handle_get_wl)
button_read_w.grid(row=1, column=3, padx=5, pady=10)

frame_w = ScrollableFrame(whiteListTab)
frame_w.grid(row=2, columnspan=4)
table_w = Table(frame_w.scrollable_frame, wl, 1)

label_txt_wlid = Label(whiteListTab, text="File ID:")
label_txt_wlid.grid(row=3, column=1, padx=10, pady=10, sticky=W)
entry_file_wl = Entry(whiteListTab, width=30)
entry_file_wl.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky=W)

label_txt_auth = Label(whiteListTab, text="Auth User:")
label_txt_auth.grid(row=4, column=1, padx=10, pady=10, sticky=W)
auth_user = Entry(whiteListTab, width=30)
auth_user.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky=W)



whitelist_add = Button(whiteListTab, text="Add", width=7, command=handle_add_whitelist)
whitelist_add.grid(row=5, column=1, columnspan=3, padx=10, pady=10, sticky=S)
whitelist_remove = Button(whiteListTab, text="Remove", width=7, command=handle_remove_whitelist)
whitelist_remove.grid(row=5, column=3, padx=10, pady=10, sticky=S)


# WHITELIST_TAB
# DEPLOY_TAB
root.mainloop()
