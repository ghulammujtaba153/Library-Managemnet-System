from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from plyer import notification
from PIL import ImageTk, Image
from tkcalendar import Calendar
from admin import Admin
from student import Student

backgroundColor = 'aliceblue'
root = tk.Tk()
root.title("LMS")

width = 1000
height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - width) // 2
y = (screen_height - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")

# Disable window resizing
root.resizable(False, False)

c1 = ImageTk.PhotoImage(Image.open('assets/img.jpg'))
c1_label = Label(root, image=c1, width=width, height=150)
c1_label.pack()


style = ttk.Style()
style.configure("Rounded.TButton", borderwidth=5, relief="solid", padding=(10, 10))

######################################################################################################################

def RequestsList():
    global RequestListFrame
    RequestListFrame = Frame(root)
    RequestListFrame.place(x=0, y=0)
    RequestListFrame.pack(side=TOP, pady=10)

    # Main Heading
    main_heading = Label(RequestListFrame, text="Requests", font=('Calibri', 25, "bold"))
    main_heading.grid(row=0, column=0, columnspan=5, padx=(20, 20), sticky="n")

    # Second Label
    second_label = Label(RequestListFrame, text="Please have a look at your requests list", font=('Calibri', 15))
    second_label.grid(row=1, column=0, columnspan=5, padx=(20, 20), pady=10, sticky="n")

    trv = ttk.Treeview(RequestListFrame, selectmode='browse')
    trv.grid(row=2, column=0, columnspan=5, padx=20, pady=20)
    trv["columns"] = ("1", "2", '3', '4')
    trv['show'] = 'headings'
    trv.column("1", width=40, anchor='c')
    trv.column("2", width=180, anchor='c')
    trv.column("3", width=180, anchor='c')
    trv.column("4", width=180, anchor='c')


    trv.heading("1", text="ID")
    trv.heading("2", text="Resource Name")
    trv.heading("3", text="Request Status")
    trv.heading("4", text="Resource Type")

    id = student.id
    data = student.get_all_Requests(id)

    # Loop to insert values into the Treeview
    for data in data:
        trv.insert("", 'end', values=(data[0], data[7], data[3], data[8]))



    back_button = ttk.Button(RequestListFrame, style="Rounded.TButton", text="Back", command=ReqBack, cursor='hand2')
    back_button.grid(row=4, column=1, padx=(5, 20), sticky="e")

def ReqBack():
    RequestListFrame.destroy()
    userMenu()


def personelInventoryList():
    global personelInventoryFrame
    personelInventoryFrame = Frame(root)
    personelInventoryFrame.place(x=0, y=0)
    personelInventoryFrame.pack(side=TOP, pady=10)

    # Main Heading
    main_heading = Label(personelInventoryFrame, text="My Current Resources", font=('Calibri', 25, "bold"))
    main_heading.grid(row=0, column=0, columnspan=5, padx=(20, 20), sticky="n")

    # Second Label
    second_label = Label(personelInventoryFrame, text="Please have a look at your current resource list", font=('Calibri', 15))
    second_label.grid(row=1, column=0, columnspan=5, padx=(20, 20), pady=10, sticky="n")

    trv = ttk.Treeview(personelInventoryFrame, selectmode='browse')
    trv.grid(row=2, column=0, columnspan=5, padx=20, pady=20)
    trv["columns"] = ("1", "2", '3', '4', '5')
    trv['show'] = 'headings'
    trv.column("1", width=40, anchor='c')
    trv.column("2", width=180, anchor='c')
    trv.column("3", width=180, anchor='c')
    trv.column("4", width=180, anchor='c')
    trv.column("5", width=180, anchor='c')

    trv.heading("1", text="ID")
    trv.heading("2", text="Resource Name")
    trv.heading("3", text="Resource Type")
    trv.heading("4", text="Status")
    trv.heading("5", text="Student Assigned")

    id = student.id
    data = student.get_all_personel_assets(id)

    # Loop to insert values into the Treeview
    for data in data:
        trv.insert("", 'end', values=(data[0], data[1], data[2], data[3], data[4]))

    def selectItem(a):
        global curItem
        curItem = trv.focus()
        cur = trv.item(curItem)
        print(trv.item(curItem)['values'][0])
        global selected
        selected = trv.item(curItem)['values'][0]

    trv.bind('<ButtonRelease-1>', selectItem)

    def returned():
        check = student.update_asset_status(selected, 'Available', 0)
        if check:
            messagebox.showinfo('Success', 'Asset Returned!')
            personelInventoryFrame.destroy()
            personelInventoryList()

    status_button = ttk.Button(personelInventoryFrame, style="Rounded.TButton", text="Return Asset", command=returned,cursor='hand2')
    status_button.grid(row=4, column=0, padx=(140, 5), sticky="e")

    back_button = ttk.Button(personelInventoryFrame, style="Rounded.TButton", text="Back", command=togglePersonBackToMenu, cursor='hand2')
    back_button.grid(row=4, column=1, padx=(5, 20), sticky="e")

def togglePersonBackToMenu():
    personelInventoryFrame.destroy()
    userMenu()


def userInventoryList():
    global userInventoryFrame
    userInventoryFrame = Frame(root, width=1000, height=600)
    userInventoryFrame.pack()

    # Main Heading
    main_heading = Label(userInventoryFrame, text="Library Resource List", font=('Calibri', 25, "bold"))
    main_heading.grid(row=0, column=0, columnspan=5, padx=(20, 20), sticky="n")

    # Second Label
    second_label = Label(userInventoryFrame, text="Please have a look at your Resource list", font=('Calibri', 15))
    second_label.grid(row=1, column=0, columnspan=5, padx=(20, 20), pady=10, sticky="n")

    trv = ttk.Treeview(userInventoryFrame, selectmode='browse')
    trv.grid(row=2, column=0, columnspan=5, padx=20, pady=15)
    trv["columns"] = ("1", "2", '3', '4', '5')
    trv['show'] = 'headings'
    trv.column("1", width=40, anchor='c')
    trv.column("2", width=180, anchor='c')
    trv.column("3", width=180, anchor='c')
    trv.column("4", width=180, anchor='c')
    trv.column("5", width=180, anchor='c')

    trv.heading("1", text="ID")
    trv.heading("2", text="Resource name")
    trv.heading("3", text="Resource type")
    trv.heading("4", text="Status")
    trv.heading("5", text="Time Borrowed")

    data = student.get_all_assets()

    # Loop to insert values into the Treeview
    for data in data:
        trv.insert("", 'end', values=(data[0], data[1], data[2], data[3], data[5]))

    def selectItem(a):
        global curItem
        curItem = trv.focus()
        cur = trv.item(curItem)
        print(trv.item(curItem)['values'][3])
        global selected
        selected = trv.item(curItem)['values'][0]
        global status
        status = trv.item(curItem)['values'][3]

    trv.bind('<ButtonRelease-1>', selectItem)

    def assigned():
        duplicate=student.check_dublicate_request(selected, student.id)
        if duplicate:
            messagebox.showerror('Error', 'Your request is already under process!')
        else:
            if status =='New' or status=='Available':
                check = student.request(selected, student.id)
                if check:
                    messagebox.showinfo('Success', 'Your request has been sent!')
            else:
                messagebox.showerror('Error', 'Not Available!')



    status_button = ttk.Button(userInventoryFrame, style="Rounded.TButton", text="Send Request", command=assigned, cursor="hand2")
    status_button.grid(row=5, column=0,  padx=(140, 5), sticky="e")

    back_button = ttk.Button(userInventoryFrame, style="Rounded.TButton", text="Back", command=toggleUListBackToAdminMenu, cursor="hand2")
    back_button.grid(row=5, column=1, padx=(5,20), sticky="e")


def toggleUListBackToAdminMenu():
    userInventoryFrame.destroy()
    userMenu()


def userMenu():
    global userMenuFrame
    userMenuFrame = Frame(root)
    userMenuFrame.place(x=0, y=0)
    userMenuFrame.pack(side=TOP, pady=10)

    lbl_username = Label(userMenuFrame, text="Welcome Resource", fg='black', font=('Calibri', 25, "bold"), bd=18)
    lbl_username.grid(row=1, pady=30)

    b1 = ttk.Button(userMenuFrame, style="Rounded.TButton", text="View Library Resource List", width=20, command=toggletoUInventory, cursor="hand2")
    b1.grid(row=3, pady=10)
    b2 = ttk.Button(userMenuFrame, style="Rounded.TButton", text="My Resource List", width=20, command=toggleToPersonelInventory, cursor="hand2")
    b2.grid(row=5, pady=10)
    b3 = ttk.Button(userMenuFrame, style="Rounded.TButton", text="View Requests", width=20, command=toggleToReqLists, cursor="hand2")
    b3.grid(row=7, pady=10)
    b4 = ttk.Button(userMenuFrame, style="Rounded.TButton", text="Logout", width=20, command=toggleBackUserToMain, cursor="hand2")
    b4.grid(row=9, pady=10)

def toggleToReqLists():
    userMenuFrame.destroy()
    RequestsList()

def toggleToPersonelInventory():
    userMenuFrame.destroy()
    personelInventoryList()


def toggleBackUserToMain():
    userMenuFrame.destroy()
    mainForm()

def toggletoUInventory():
    userMenuFrame.destroy()
    userInventoryList()

def userRegisteration():
    global userRegFrame, lbl_error
    userRegFrame = Frame(root)
    userRegFrame.place(x=0, y=0)
    userRegFrame.pack(side=TOP, pady=10)

    lbl = Label(userRegFrame, text="Student Registeration", fg='black', font=('Calibri', 25,"bold"))
    lbl.grid(row=0, pady=2, columnspan=2, padx=60)

    lbl2 = Label(userRegFrame, text="Please enter your credentials", fg="black", font=('Calibri', 15))
    lbl2.grid(row=1, pady=15, columnspan=2, padx=60)

    email_label = Label(userRegFrame, text="Email:", font=('Calibri', 15))
    email_label.grid(row=2, column=0, padx=20, sticky="w")
    email_entry = Entry(userRegFrame, font=('Calibri', 15))
    email_entry.grid(row=2, pady=(15,15), column=1)

    name_label = Label(userRegFrame, text="Name:", font=('Calibri', 15))
    name_label.grid(row=4, column=0, padx=20, sticky="w")
    name_entry = Entry(userRegFrame, font=('Calibri', 15))
    name_entry.grid(row=4, pady=(15,15), column=1)


    ttk.Label(userRegFrame, text="Gender:", font=('Calibri', 15)).grid(column=0, row=3, padx=10, sticky="w", pady=(15, 15))

    genderchoosen = tk.StringVar()
    R1 = ttk.Radiobutton(userRegFrame, text="Male", variable=genderchoosen, value='Male')
    R1.grid(column=1, row=3)
    R2 = ttk.Radiobutton(userRegFrame, text="Female", variable=genderchoosen, value='Female')
    R2.grid(column=2, row=3)


    password_label = Label(userRegFrame, text="Password:", font=('Calibri', 15))
    password_label.grid(row=8, column=0, padx=20, sticky="w")
    password_entry = Entry(userRegFrame, font=('Calibri', 15), show='*')
    password_entry.grid(row=8, pady=(15,15), column=1)

    lbl_error = Label(userRegFrame, text="", foreground='red', font=('Calibri', 12),
                      cursor="hand2")
    lbl_error.grid(row=9, column=1)

    def registeration_function():
        name = name_entry.get()
        gender = genderchoosen.get()
        email = email_entry.get()
        password = password_entry.get()

        if name == '' or gender == '' or email == '' or password == '':
            messagebox.showerror('Error!', 'Fill all the fields')
        else:
            check = student.register(name, password, gender, email)
            if check:
                toggleToUserLogin()
            else:
                lbl_error.config(text='error')


    # Add a login button if needed
    register_button = ttk.Button(userRegFrame,style="Rounded.TButton", text="Register", command=registeration_function, cursor="hand2")
    register_button.grid(row=12, columnspan=2, pady=20, padx=(180,0), sticky="w")

    back_button = ttk.Button(userRegFrame, style="Rounded.TButton", text="Back", command=toggleToForm, cursor="hand2")
    back_button.grid(row=12, column=1, pady=(20, 20), padx=(150, 60), sticky="w")

    lbl_login = Label(userRegFrame, text="Go For Login", foreground='blue', font=('Calibri', 12),cursor="hand2")
    lbl_login.grid(row=13, column=1, sticky="w", padx=(100,20))
    lbl_login.bind('<Button-1>', lambda event=None: toggleToUserLogin())



def toggleToForm():
    userRegFrame.destroy()
    mainForm()


def toggleToUserLogin():
    userRegFrame.destroy()
    userLogin()


def userLogin():
    global userFrame, lbl_login_error
    userFrame = Frame(root)
    userFrame.place(x=0, y=0)
    userFrame.pack(side=TOP, pady=10)

    lbl = Label(userFrame, text="Dear Student", fg='black', font=('Calibri', 25, "bold"))
    lbl.grid(row=0, pady=2, columnspan=2, padx=60)

    lbl2 = Label(userFrame, text="Please enter your credentials", fg="black", font=('Calibri', 15))
    lbl2.grid(row=1, pady=15, columnspan=2, padx=60)

    email_label = Label(userFrame, text="Email:", font=('Calibri', 15))
    email_label.grid(row=2, column=0, padx=20, sticky="e", pady=40)
    email_entry = Entry(userFrame, font=('Calibri', 15))
    email_entry.grid(row=2, column=1, pady=10, sticky="w")

    password_label = Label(userFrame, text="Password:", font=('Calibri', 15))
    password_label.grid(row=3, column=0, padx=20, sticky="e")
    password_entry = Entry(userFrame, font=('Calibri', 15), show='*')
    password_entry.grid(row=3, column=1, pady=10, sticky="w")

    lbl_login_error = Label(userFrame, text="", font=('Calibri', 12), cursor="hand2", foreground='red')
    lbl_login_error.grid(row=4, column=1, pady=10)

    def login_function():
        email = email_entry.get()
        password = password_entry.get()
        check = student.login(email, password)
        if check:
            toggleToUserMenu()
            if student.get_new_messages(student.id):
                notification.notify('Message!', 'Request Response by Admin!')
                student.update_message_status(student.id)
        else:
            lbl_login_error.config(text='Login Error!')

    login_button = ttk.Button(userFrame, style="Rounded.TButton", text="Login", command=login_function, cursor="hand2")
    login_button.grid(row=5, columnspan=2, pady=20, padx=120, sticky="w")

    back_button = ttk.Button(userFrame, style="Rounded.TButton", text="Back", command=toggleBack, cursor="hand2")
    back_button.grid(row=5, column=1, pady=(20, 20), padx=(120, 60), sticky="w")

    lbl_register = Label(userFrame, text="Don't have an account? Register!", font=('Calibri', 12), foreground='blue',
                         cursor="hand2")
    lbl_register.grid(row=6, column=0, columnspan=2, pady=10, padx=(120, 0), sticky="w")
    lbl_register.bind('<Button-1>', lambda event=None: ToggleToRegister())


def toggleBack():
    userFrame.destroy()
    mainForm()


def ToggleToRegister():
    userFrame.destroy()
    userRegisteration()


def toggleToUserMenu():
    userFrame.destroy()
    userMenu()


####################################################################################################################

def requestList():
    global requestListFrame
    requestListFrame = Frame(root)
    requestListFrame.place(x=0, y=0)
    requestListFrame.pack(side=TOP, pady=3, padx=0)

    # Label for Your Inventory List
    lbl = Label(requestListFrame, text="Your Requests List", fg='black', font=('Calibri', 20, "bold"))
    lbl.grid(row=0, column=0, columnspan=5, padx=(20, 20), pady=3)  # Span all 5 columns

    # Treeview for data display
    trv = ttk.Treeview(requestListFrame, selectmode='browse')
    trv.grid(row=1, column=0, columnspan=5, padx=(20, 20), pady=20, sticky='nsew')
    trv["columns"] = ("1", "2", '3', '4', '5', '6')
    trv['show'] = 'headings'
    trv.column("1", width=80, anchor='c')
    trv.column("2", width=150, anchor='c')
    trv.column("3", width=150, anchor='c')
    trv.column("4", width=120, anchor='c')
    trv.column("5", width=80, anchor='c')
    trv.column("6", width=80, anchor='c')

    trv.heading("1", text="Resource ID")
    trv.heading("2", text="Resource Name")
    trv.heading("3", text="Resource Type")
    trv.heading("4", text="Status")
    trv.heading("5", text="Requested ID")
    trv.heading("6", text="Student ID")

    data = admin.get_all_requests()

    for data in data:
        trv.insert("", 'end', values=(data[0], data[1], data[2], data[3], data[6], data[7]))

    # Function to handle item selection
    def selectItem(event):
        curItem = trv.focus()
        global emp
        emp = trv.item(curItem)['values'][5]
        global asset
        asset = trv.item(curItem)['values'][0]
        global requestId
        requestId = trv.item(curItem)['values'][4]
    trv.bind('<ButtonRelease-1>', selectItem)

    # Function to accept request
    def accept():
        check = admin.accept_request(asset, 'Assigned', emp, requestId, 'Accepted')
        if check:
            messagebox.showinfo('Success', 'Request accepted!')

            requestListFrame.destroy()
            requestList()
        else:
            messagebox.showerror('error', 'Error!')

    # Function to reject request
    def reject():
        check = admin.reject_requests( requestId, 'Rejected')
        if check:
            messagebox.showinfo('Success', 'Request rejected successfully!')

            requestListFrame.destroy()
            requestList()
        else:
            messagebox.showerror('Error', 'Error!')

    button_frame = Frame(requestListFrame)
    button_frame.grid(row=9, column=0, columnspan=5, pady=20)

    def create_identical_button(text, command):
        button = ttk.Button(button_frame, style="Rounded.TButton", text=text, command=command, cursor="hand2")
        button.pack(side=LEFT, padx=20, fill='both', expand=True)
        return button

    accept_button = create_identical_button("Accept", accept)
    reject_button = create_identical_button("Reject", reject)
    back_button = create_identical_button("Back", toggleBackToAdminMenuFromRequest)

    # Configure grid weights for proper resizing
    for i in range(5):
        button_frame.columnconfigure(i, weight=1)

    requestListFrame.update_idletasks()
    trv.configure(height=(requestListFrame.winfo_height() // 22))


def toggleBackToAdminMenuFromRequest():
    requestListFrame.destroy()
    adminMenu()

def inventoryList():
    global inventoryFrame
    inventoryFrame = Frame(root)
    inventoryFrame.place(x=0, y=0)
    inventoryFrame.pack(side=TOP, pady=20)

    # Main Heading
    main_heading = Label(inventoryFrame, text="Library Resource List", font=('Calibri', 25, "bold"))
    main_heading.grid(row=0, column=0, columnspan=5, padx=(20, 20), sticky="n")

    # Second Label
    second_label = Label(inventoryFrame, text="Please have a look at your Library Resource list", font=('Calibri', 15))
    second_label.grid(row=1, column=0, columnspan=5, padx=(20, 20), pady=10, sticky="n")

    trv = ttk.Treeview(inventoryFrame, selectmode='browse')
    trv.grid(row=2, column=0, columnspan=5, padx=20, pady=15)
    trv["columns"] = ("1", "2", '3', '4', '5')
    trv['show'] = 'headings'
    trv.column("1", width=40, anchor='c')
    trv.column("2", width=180, anchor='c')
    trv.column("3", width=180, anchor='c')
    trv.column("4", width=180, anchor='c')
    trv.column("5", width=180, anchor='c')

    trv.heading("1", text="ID")
    trv.heading("2", text="Resource Name")
    trv.heading("3", text="Resource Type")
    trv.heading("4", text="Status")
    trv.heading("5", text="Time Borrowed")

    data = admin.get_all_assets()

    # Loop to insert values into the Treeview
    for data in data:
        trv.insert("", 'end', values=(data[0], data[1], data[2], data[3], data[5]))

    def selectItem(a):
        global curItem
        curItem = trv.focus()
        cur = trv.item(curItem)
        global selected
        selected = trv.item(curItem)['values'][0]

    trv.bind('<ButtonRelease-1>', selectItem)

    # Change Status Label
    ttk.Label(inventoryFrame, text="Change status:", font=('Calibri', 15)).grid(column=0, row=3, padx=20, sticky="w")

    # Status Combobox
    n = tk.StringVar()
    statuschoosen = ttk.Combobox(inventoryFrame, width=27, textvariable=n, state="readonly")
    statuschoosen['values'] = ("Out of Order", "Available",)
    statuschoosen.grid(column=1, row=3)
    statuschoosen.current()

    def change_status():
        admin.update_asset_status(selected, statuschoosen.get())
        inventoryFrame.destroy()
        inventoryList()

    status_button = ttk.Button(inventoryFrame, style="Rounded.TButton", text="Update", command=change_status,
                               cursor="hand2")
    status_button.grid(row=4, column=0, columnspan=5, padx=20, pady=(5, 20))

    # Back Button
    back_button = ttk.Button(inventoryFrame, style="Rounded.TButton", text="Back", command=toggleListBackToAdminMenu,
                             cursor="hand2")
    back_button.grid(row=5, column=0, columnspan=5, padx=20, pady=(5, 20))

def toggleListBackToAdminMenu():
    inventoryFrame.destroy()
    adminMenu()

def newItem():
    global newItemFrame
    newItemFrame = Frame(root)
    newItemFrame.place(x=0, y=0)
    newItemFrame.pack(side=TOP, pady=3, padx=0)

    # Label for Add New Item
    lbl = Label(newItemFrame, text="Add New Item", fg='black', font=('Calibri', 20, "bold"))
    lbl.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 20))

    subtitle_label = Label(newItemFrame, text="Please fill the below details for adding a new item", font=('Calibri', 15))
    subtitle_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 20))

    name_label = Label(newItemFrame, text="Asset Name:", font=('Calibri', 15))
    name_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")

    name_entry = Entry(newItemFrame, font=('Calibri', 15))
    name_entry.grid(row=2, column=1, padx=20, pady=20, sticky="w")

    type_label = Label(newItemFrame, text="Asset Type:", font=('Calibri', 15))
    type_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

    n = tk.StringVar()
    typechoosen = ttk.Combobox(newItemFrame, width=31, height=20,textvariable=n, state="readonly")
    typechoosen['values'] = ("Book", "Journals", "Theses", "Artifacts")
    typechoosen.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    status_label = Label(newItemFrame, text="Status:", font=('Calibri', 15))
    status_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")

    n = tk.StringVar()
    statuschoosen = ttk.Combobox(newItemFrame, width=31, height=30, textvariable=n, state="readonly")
    statuschoosen['values'] = ("Not Available", "New")
    statuschoosen.grid(row=4, column=1, padx=20, pady=10, sticky="w")

    error_label = Label(newItemFrame, text="", font=('Calibri', 15), bd=18)
    error_label.grid(row=5, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="n")

    def register():
        name = name_entry.get()
        type = typechoosen.get()
        status = statuschoosen.get()
        check = admin.insert_asset(name, type, status)
        if check:
            toggleBackToAdminMenu()
        else:
            error_label.config(text='Error: Asset registration failed')

    button_frame = Frame(newItemFrame)
    button_frame.grid(row=6, column=0, columnspan=2, pady=20)

    accept_button = ttk.Button(button_frame, style="Rounded.TButton", text="Add Item", command=register, cursor="hand2")
    accept_button.pack(side=LEFT, padx=20)

    back_button = ttk.Button(button_frame, style="Rounded.TButton", text="Back", command=toggleBackToAdminMenu, cursor="hand2")
    back_button.pack(side=LEFT, padx=20)

def toggleToNewItem():
    adminMenuFrame.destroy()
    newItem()

def toggleBackToAdminMenu():
    newItemFrame.destroy()
    adminMenu()


def DateMenu():
    global dateMenuFrame
    dateMenuFrame = Frame(root)
    dateMenuFrame.place(x=0,y=0)
    dateMenuFrame.pack(side=TOP, pady=10)

    lbl_username = Label(dateMenuFrame, text="Select the date to generate CSV file",fg='black', font=('Calibri', 25,"bold"), bd=18)
    lbl_username.grid(row=0,pady=10)

    def get_selected_date():
        selected_date = cal.get_date()
        formatted_date = datetime.strptime(selected_date, "%m/%d/%y").strftime("%Y-%m-%d")
        print("Selected Date:", formatted_date)
        if admin.generate_request_report(formatted_date):
            messagebox.showinfo('success', "CSV file generated!")
        else:
            messagebox.showerror("falied", "No requests found on this date!")
        dateMenuFrame.destroy()
        adminMenu()


    cal = Calendar(dateMenuFrame, selectmode="day", year=2024, month=3, day=16)
    cal.grid(row=1, pady=10)

    btn_select = ttk.Button(dateMenuFrame, style="Rounded.TButton", text="Generate", width=30, command=get_selected_date, cursor="hand2")
    btn_select.grid(row=2, pady=10)

def adminMenu():
    global adminMenuFrame
    adminMenuFrame = Frame(root)
    adminMenuFrame.place(x=0,y=0)
    adminMenuFrame.pack(side=TOP, pady=5)

    lbl_username = Label(adminMenuFrame, text="Welcome Library Admin",fg='black', font=('Calibri', 25,"bold"), bd=18)
    lbl_username.grid(row=0,pady=5)

    b1 = ttk.Button(adminMenuFrame, style="Rounded.TButton", text="Add New Item", width=30, command=toggleToNewItem, cursor='hand2')
    b1.grid(row=1, pady=10)

    b1 = ttk.Button(adminMenuFrame, style="Rounded.TButton", text="View Library Resource List", width=30, command=toggleToInventoryList, cursor="hand2")
    b1.grid(row=2, pady=10)
    b2 = ttk.Button(adminMenuFrame, style="Rounded.TButton", text="View Student Requests", width=30, command=toggleToRequests, cursor="hand2")
    b2.grid(row=3, pady=10)
    b3 = ttk.Button(adminMenuFrame, style="Rounded.TButton", text="Generate Library Assets CSV file", width=30, command=assetsFile, cursor="hand2")
    b3.grid(row=4, pady=10)
    b4 = ttk.Button(adminMenuFrame, style="Rounded.TButton", text="Generate Students CSV file", width=30, command=usersFile, cursor="hand2")
    b4.grid(row=5, pady=10)
    b5 = ttk.Button(adminMenuFrame, style="Rounded.TButton", text="Student Borrow Requests CSV", width=30, command=toggleToDate, cursor="hand2")
    b5.grid(row=6, pady=10)
    b6 = ttk.Button(adminMenuFrame, style="Rounded.TButton", text="Logout", width=30, command=toggleBackToMain, cursor="hand2")
    b6.grid(row=7, pady=10)

def toggleToRequests():
    adminMenuFrame.destroy()
    requestList()

def toggleToDate():
    adminMenuFrame.destroy()
    DateMenu()

def usersFile():
    admin.save_users_to_csv()
    messagebox.showinfo('Success', 'CSV file of users has been generated!')

def assetsFile():
    admin.save_assets_to_csv()
    messagebox.showinfo('Success', 'CSV file of assets has been generated!')


def toggleBackToMain():
    adminMenuFrame.destroy()
    mainForm()

def toggleToInventoryList():
    adminMenuFrame.destroy()
    inventoryList()


def adminLogin():
    global adminFrame
    adminFrame = Frame(root)
    adminFrame.place(x=0, y=0)
    adminFrame.pack(side=TOP, pady=10)

    lbl = Label(adminFrame, text="Dear Library Admin", fg='black', font=('Calibri', 25, "bold"))
    lbl.grid(row=0, pady=2, padx=60, columnspan=3)  # Span all 3 columns

    lbl2 = Label(adminFrame, text="Please enter your credentials", fg="black", font=('Calibri', 15))
    lbl2.grid(row=1, pady=15, padx=60, columnspan=3)  # Reduced pady value for minimum space

    email_label = Label(adminFrame, text="Email:", font=('Calibri', 15))
    email_label.grid(row=2, column=0, padx=(100, 10), sticky="w", pady=30)  # Adjust left padding
    email_entry = Entry(adminFrame, font=('Calibri', 15))
    email_entry.grid(row=2, column=1,  rowspan=2, pady=30)  # Use rowspan to increase the height

    # Password Label and Entry
    password_label = Label(adminFrame, text="Password:", font=('Calibri', 15))
    password_label.grid(row=4, column=0, padx=(100, 10), sticky="w")  # Adjust left padding
    password_entry = Entry(adminFrame, font=('Calibri', 15), show='*')
    password_entry.grid(row=4, column=1,  rowspan=2)  # Use rowspan to increase the height


    def login_function():
        email = email_entry.get()
        password = password_entry.get()
        if email == 'admin@gmail.com' and password == 'password':
            toggleToAdminMenu()
            if admin.get_new_messages():
                admin.update_message_status()
                notification.notify('New Request', "new Request!")


        else:
            messagebox.showerror('Error!', 'Invalid email or password')


    login_button = ttk.Button(adminFrame, style="Rounded.TButton", text="LogIn", command=login_function, cursor="hand2", width=10)
    login_button.grid(row=6, column=1, pady=35, sticky="w", padx=10)


    back_button = ttk.Button(adminFrame, style="Rounded.TButton", text="Back", command=toggleAdminBackToMain, cursor="hand2", width=10)
    back_button.grid(row=6, column=1, pady=35, padx=140)

def toggleAdminBackToMain():
    adminFrame.destroy()
    mainForm()


def toggleToAdminMenu():
    adminFrame.destroy()

    adminMenu()




def mainForm():
    global mainFrame
    mainFrame = Frame(root)
    mainFrame.place(x=0,y=0)
    mainFrame.pack(side=TOP, pady=10)

    lbl_username = Label(mainFrame, text="Library Management System",fg='black', font=('Calibri', 25, "bold"))
    lbl_username.grid(row=6,pady=10)
    lbl_secondusername=Label(mainFrame, text="Welcome, Please choose your respective role: ", fg="black", font=('Calibri',15))
    lbl_secondusername.grid(row=7,pady=20)

    b1 = ttk.Button(mainFrame, style="Rounded.TButton", text="Library Admin", width=20, command=toggleToAdmin, cursor="hand2")
    b1.grid(row=9, pady=10)

    b2 = ttk.Button(mainFrame, style="Rounded.TButton", text="Student", width=20, command=toggleToUser, cursor="hand2")
    b2.grid(row=13, pady=10)

    b3 = ttk.Button(mainFrame, text="Exit", style="Rounded.TButton", width=20, command=close, cursor="hand2")
    b3.grid(row=15, pady=10)


def close():
    root.destroy()

def toggleToAdmin():
    mainFrame.destroy()

    global admin
    admin=Admin()
    adminLogin()

def toggleToUser():
    mainFrame.destroy()
    global student
    student= Student()

    userLogin()


mainForm()



root.mainloop()
