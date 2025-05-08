import re
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

# Database connection details
DB_HOST = 'sql12.freesqldatabase.com'
DB_USER = 'sql12776990'
DB_PASSWORD = 'A22rYY62nK'
DB_NAME = 'sql12776990'
DB_PORT = 3306

def direct_login():
    Vwindow.destroy()
    import login
# Function to connect to the database
def connect_to_database():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return connection
    except Exception as e:
        messagebox.showerror('Error', f'Could not connect to the database: {e}')
        return None


def check_password_strength(password):
    pattern = r"^(?=.*[A-Z])(?=.*[!@#$%^&*()])(?=.*\d).{8,}$"
    return bool(re.match(pattern, password))


def toggle_password_visibility():
    if show_password_var.get():
        code.config(show="")
        conf.config(show="")
    else:
        code.config(show="*")
        conf.config(show="*")


def clear():
    user.delete(0, END)
    code.delete(0, END)
    conf.delete(0, END)
    check.set(0)


def login_page():
    if user.get() == "" or code.get() == "" or conf.get() == "":
        messagebox.showerror('Error', 'All Fields Are Required')
        return

    if conf.get() != code.get():
        messagebox.showerror('Error', 'Password Mismatch')
        return

    if check.get() == 0:
        messagebox.showerror('Error', 'Please Accept Terms and Conditions')
        return

    if not check_password_strength(code.get()):
        messagebox.showerror(
            'Error',
            'Password must contain at least one uppercase letter, one special character, and one digit, and be at least 8 characters long'
        )
        return

    con = connect_to_database()
    if not con:
        return

    try:
        mycursor = con.cursor()
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS dataofuser (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), password VARCHAR(255))"
        )

        mycursor.execute('SELECT * FROM dataofuser WHERE name=%s', (user.get(),))
        row = mycursor.fetchone()

        if row:
            messagebox.showerror('Error', 'User Already Exists')
        else:
            mycursor.execute('INSERT INTO dataofuser (name, password) VALUES (%s, %s)', (user.get(), code.get()))
            con.commit()
            messagebox.showinfo('Success', 'Registration is Successful')
            clear()
    except Exception as e:
        messagebox.showerror('Error', f'Database Error: {e}')
    finally:
        con.close()


# GUI Setup
Vwindow = Tk()
Vwindow.title("SIGN UP")
Vwindow.geometry('925x500+185+85')
Vwindow.configure(bg='#fff')
Vwindow.resizable(False, False)

show_password_var = BooleanVar()
show_password_var.set(False)

bgOriginal = Image.open('assets/new1.png').resize((925, 500))
img = ImageTk.PhotoImage(bgOriginal)
Label(Vwindow, image=img, border=0, bg='white').place(x=0, y=0)

frame = Frame(Vwindow, width=350, height=350, bg='white')
frame.place(x=500, y=65)

heading = Label(frame, text='SignUp', fg='#006666', bg='white', font=('Microsoft Yahei UI', 23, 'bold'))
heading.place(x=120, y=20)

user = Entry(frame, width=30, fg='black', border=2, bg="white", font=('Microsoft Yahei UI', 10), bd=0)
user.place(x=30, y=80)
user.insert(0, 'Username')
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

code = Entry(frame, width=30, fg='black', border=2, bg="white", font=('Microsoft Yahei UI', 10), bd=0, show="*")
code.place(x=30, y=120)
code.insert(0, 'Password')
Frame(frame, width=295, height=2, bg='black').place(x=25, y=147)

conf = Entry(frame, width=30, fg='black', border=2, bg="white", font=('Microsoft Yahei UI', 10), bd=0, show="*")
conf.place(x=30, y=160)
conf.insert(0, 'Confirm Password')
Frame(frame, width=295, height=2, bg='black').place(x=25, y=187)

Button(frame, width=39, pady=7, text='Sign Up', bg='#006666', fg='white', border=0, command=login_page).place(x=35, y=224)

check = IntVar()
termsandconditions = Checkbutton(
    frame, text='I Agree to the Terms and Conditions', variable=check, bg='white', fg='#006666', activeforeground='#006666', font=('Microsoft Yahei UI', 9, 'bold')
)
termsandconditions.place(x=50, y=260)

show_password_checkbox = Checkbutton(
    frame, text="Show Password", variable=show_password_var, command=toggle_password_visibility, bg='white', fg='#006666', activeforeground='#006666'
)
show_password_checkbox.place(x=220, y=190)

footer = Label(frame, text='Already have an Account?', fg='black', bg='white', font=('Microsoft Yahei UI', 9, 'italic'))
footer.place(x=50, y=320)

footer1 = Button(frame, width=5, text='Log In', bg='white', fg='blue', activeforeground='#8c03fc',
                 activebackground='white',
                 border=0, command=direct_login).place(x=210, y=320)

Vwindow.mainloop()
