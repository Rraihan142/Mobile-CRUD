import os
import pandas as pd
import PySimpleGUI as sg
import mysql.connector
from bcrypt import hashpw, gensalt, checkpw

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="database_aplikasi"
)
cursor = db.cursor()

# File Excel untuk backup pendaftaran
EXCEL_FILE = 'Pendaftaran.xlsx'
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['Nama', 'Tlp', 'Alamat', 'Tgl Lahir', 'Jekel', 'Hobi'])
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

# GUI Themes
sg.theme('Darkgreen')

# Login Layout
login_layout = [
    [sg.Text('Username', size=(10, 1)), sg.InputText(key='Username')],
    [sg.Text('Password', size=(10, 1)), sg.InputText(key='Password', password_char='*')],
    [sg.Button('Login'), sg.Button('Register'), sg.Exit()]
]

# Registration Layout
register_layout = [
    [sg.Text('Daftar Akun Baru')],
    [sg.Text('Username', size=(10, 1)), sg.InputText(key='Reg_Username')],
    [sg.Text('Password', size=(10, 1)), sg.InputText(key='Reg_Password', password_char='*')],
    [sg.Text('Role', size=(10, 1)), sg.Combo(['konsumen', 'admin'], default_value='konsumen', key='Reg_Role')],
    [sg.Button('Submit'), sg.Button('Cancel')]
]

# Admin Layout
admin_layout = [
    [sg.Text('Admin Dashboard')],
    [sg.Button('Lihat Data Konsumen'), sg.Button('Tambah Data Konsumen')],
    [sg.Exit()]
]

# Konsumen Dashboard Layout
konsumen_dashboard_layout = [
    [sg.Text('Konsumen Dashboard')],
    [sg.Button('Tambah Data Konsumen'), sg.Button('Cek Data')],
    [sg.Exit()]
]

# Konsumen Form Layout
form_layout = [
    [sg.Text('Masukkan Data Kamu: ')],
    [sg.Text('Nama', size=(15, 1)), sg.InputText(key='Nama')],
    [sg.Text('No Telp', size=(15, 1)), sg.InputText(key='Tlp')],
    [sg.Text('Alamat', size=(15, 1)), sg.Multiline(key='Alamat')],
    [sg.Text('Tgl Lahir', size=(15, 1)), sg.InputText(key='Tgl Lahir'),
     sg.CalendarButton('Kalendar', target='Tgl Lahir', format='%Y-%m-%d')],
    [sg.Text('Jenis Kelamin', size=(15, 1)), sg.Combo(['Pria', 'Wanita'], key='Jekel')],
    [sg.Text('Hobi', size=(15, 1)), sg.Checkbox('Belajar', key='Belajar'),
     sg.Checkbox('Menonton', key='Menonton'), sg.Checkbox('Musik', key='Musik')],
    [sg.Submit(), sg.Button('Clear'), sg.Exit()]
]

# Fungsi Clear Input
def clear_input(window):
    for key in ['Nama', 'Tlp', 'Alamat', 'Tgl Lahir', 'Jekel', 'Belajar', 'Menonton', 'Musik']:
        window[key].update('' if key not in ['Belajar', 'Menonton', 'Musik'] else False)

# Fungsi Tambah Data Konsumen
def tambah_data_konsumen():
    form_window = sg.Window('Tambah Data Konsumen', form_layout)
    while True:
        event, values = form_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Submit':
            nama = values['Nama']
            tlp = values['Tlp']
            alamat = values['Alamat']
            tgl_lahir = values['Tgl Lahir']
            jekel = values['Jekel']
            hobi = ', '.join([h for h in ['Belajar', 'Menonton', 'Musik'] if values[h]])

            cursor.execute(
                "INSERT INTO pendaftaran (nama, tlp, alamat, tgl_lahir, jekel, hobi) VALUES (%s, %s, %s, %s, %s, %s)",
                (nama, tlp, alamat, tgl_lahir, jekel, hobi)
            )
            db.commit()
            sg.popup('Data berhasil ditambahkan!')
            clear_input(form_window)
    form_window.close()

# Fungsi Lihat Data Konsumen
def lihat_data_konsumen():
    cursor.execute("SELECT * FROM pendaftaran")
    data = cursor.fetchall()
    if not data:
        sg.popup('Tidak ada data untuk ditampilkan.')
        return

    # Layout for displaying the data
    lihat_layout = [
        [sg.Text('Data Konsumen')],
        [sg.Table(values=[[d[1], d[2], d[3], d[4], d[5], d[6]] for d in data],
                  headings=['Nama', 'Telp', 'Alamat', 'Tgl Lahir', 'Jekel', 'Hobi'],
                  auto_size_columns=False, justification='right', key='-TABLE-', col_widths=[20, 15, 30, 15, 10, 20])],
        [sg.Button('Kembali')]
    ]

    # Display window to show the data
    lihat_window = sg.Window('Lihat Data Konsumen', lihat_layout)
    while True:
        event, _ = lihat_window.read()
        if event == sg.WIN_CLOSED or event == 'Kembali':
            break
    lihat_window.close()

# Fungsi Cek Data Konsumen
def cek_data_konsumen(username):
    # Fetch the logged-in user's data from the database
    cursor.execute("SELECT nama, tlp, alamat, tgl_lahir, jekel, hobi FROM pendaftaran WHERE nama = %s", (username,))
    data = cursor.fetchall()

    if not data:
        sg.popup('Tidak ada data untuk ditampilkan.')
        return

    # Layout for displaying the data
    cek_layout = [
        [sg.Text('Data Konsumen')],
        [sg.Table(values=[[d[0], d[1], d[2], d[3], d[4], d[5]] for d in data],
                  headings=['Nama', 'Telp', 'Alamat', 'Tgl Lahir', 'Jekel', 'Hobi'],
                  auto_size_columns=False, justification='right', key='-TABLE-', col_widths=[20, 15, 30, 15, 10, 20])],
        [sg.Button('Kembali')]
    ]

    # Display window to show the data
    cek_window = sg.Window('Cek Data Konsumen', cek_layout)
    while True:
        event, _ = cek_window.read()
        if event == sg.WIN_CLOSED or event == 'Kembali':
            break
    cek_window.close()

# Login Window
login_window = sg.Window('Login', login_layout)

while True:
    event, values = login_window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Login':
        username = values['Username']
        password = values['Password']
        query = "SELECT password, role FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result and checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            role = result[1]
            login_window.close()

            if role == 'admin':
                admin_window = sg.Window('Admin Dashboard', admin_layout)
                while True:
                    admin_event, admin_values = admin_window.read()
                    if admin_event == sg.WIN_CLOSED or admin_event == 'Exit':
                        break
                    if admin_event == 'Lihat Data Konsumen':
                        lihat_data_konsumen()  # Show the consumer data
                    if admin_event == 'Tambah Data Konsumen':
                        tambah_data_konsumen()
                admin_window.close()

            elif role == 'konsumen':
                konsumen_window = sg.Window('Konsumen Dashboard', konsumen_dashboard_layout)
                while True:
                    konsumen_event, konsumen_values = konsumen_window.read()
                    if konsumen_event == sg.WIN_CLOSED or konsumen_event == 'Exit':
                        break
                    if konsumen_event == 'Tambah Data Konsumen':
                        tambah_data_konsumen()
                    if konsumen_event == 'Cek Data':
                        cek_data_konsumen(username)  # Call cek_data_konsumen with the logged-in username
                konsumen_window.close()
        else:
            sg.popup('Username atau password salah! Mohon cek kembali.')

    if event == 'Register':
        register_window = sg.Window('Register', register_layout)
        while True:
            reg_event, reg_values = register_window.read()
            if reg_event == sg.WIN_CLOSED or reg_event == 'Cancel':
                break
            if reg_event == 'Submit':
                reg_username = reg_values['Reg_Username']
                reg_password = hashpw(reg_values['Reg_Password'].encode('utf-8'), gensalt()).decode('utf-8')
                reg_role = reg_values['Reg_Role']

                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                               (reg_username, reg_password, reg_role))
                db.commit()
                sg.popup('Registrasi berhasil!')
                break
        register_window.close()

login_window.close()
