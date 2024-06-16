#SKRYPT3
from tkinter import *
from tkinter import messagebox

zalogowany = False

# Lista policjantów
policjanci = [
    {"nazwa": "Jan Kowalski", "wspolrzedne": (50.0, 20.0)},
    {"nazwa": "Anna Nowak", "wspolrzedne": (51.0, 21.0)},
    {"nazwa": "Piotr Wiśniewski", "wspolrzedne": (52.0, 22.0)},
    {"nazwa": "Krzysztof Wójcik", "wspolrzedne": (53.0, 23.0)},
    {"nazwa": "Agnieszka Kowalczyk", "wspolrzedne": (54.0, 24.0)},
    {"nazwa": "Michał Kamiński", "wspolrzedne": (55.0, 25.0)},
    {"nazwa": "Ewa Lewandowska", "wspolrzedne": (56.0, 26.0)}
]

def logowanie():
    global zalogowany
    nazwa_uzytkownika = entry_nazwa_uzytkownika.get()
    haslo = entry_haslo.get()
    if nazwa_uzytkownika == "user" and haslo == "user":
        zalogowany = True
        login_frame.grid_forget()
        main_frame.grid(row=0, column=0, padx=50)
        lista_policjantow()
    else:
        messagebox.showerror("Błąd logowania", "Niepoprawna nazwa użytkownika lub hasło")

# Funkcje CRUD
def lista_policjantow():
    listbox_lista_policjantow.delete(0, END)
    for idx, policjant in enumerate(policjanci):
        listbox_lista_policjantow.insert(idx, f"{policjant['nazwa']} ({policjant['wspolrzedne'][0]}, {policjant['wspolrzedne'][1]})")

def dodaj_policjanta():
    nazwa = entry_nazwa.get()
    wsp_x = entry_wsp_x.get()
    wsp_y = entry_wsp_y.get()
    wspolrzedne = (float(wsp_x), float(wsp_y))
    nowy_policjant = {"nazwa": nazwa, "wspolrzedne": wspolrzedne}
    policjanci.append(nowy_policjant)
    lista_policjantow()
    entry_nazwa.delete(0, END)
    entry_wsp_x.delete(0, END)
    entry_wsp_y.delete(0, END)
    entry_nazwa.focus()

def usun_policjanta():
    listbox_lista_policjantow.curselection()
    i = listbox_lista_policjantow.curselection()[0]
    policjanci.pop(i)
    lista_policjantow()

def pokaz_szczegoly_policjanta():
    listbox_lista_policjantow.curselection()
    i = listbox_lista_policjantow.curselection()[0]
    policjant = policjanci[i]
    label_nazwa_szczegoly.config(text=policjant['nazwa'])
    label_wspolrzedne_szczegoly.config(text=f"{policjant['wspolrzedne'][0]}, {policjant['wspolrzedne'][1]}")

def edytuj_policjanta():
    listbox_lista_policjantow.curselection()
    i = listbox_lista_policjantow.curselection()[0]
    entry_nazwa.insert(0, policjanci[i]['nazwa'])
    entry_wsp_x.insert(0, policjanci[i]['wspolrzedne'][0])
    entry_wsp_y.insert(0, policjanci[i]['wspolrzedne'][1])
    button_dodaj_policjanta.config(text="Zapisz zmiany", command=lambda: aktualizuj_policjanta(i))

def aktualizuj_policjanta(i):
    policjanci[i]['nazwa'] = entry_nazwa.get()
    policjanci[i]['wspolrzedne'] = (float(entry_wsp_x.get()), float(entry_wsp_y.get()))
    lista_policjantow()
    button_dodaj_policjanta.config(text="Dodaj policjanta", command=dodaj_policjanta)
    entry_nazwa.delete(0, END)
    entry_wsp_x.delete(0, END)
    entry_wsp_y.delete(0, END)
    entry_nazwa.focus()

# GUI
root = Tk()
root.title("MapBook")
root.geometry("800x600")

# Login frame
login_frame = Frame(root)
label_nazwa_uzytkownika = Label(login_frame, text="Nazwa użytkownika:")
entry_nazwa_uzytkownika = Entry(login_frame)
label_haslo = Label(login_frame, text="Hasło:")
entry_haslo = Entry(login_frame, show="*")
button_login = Button(login_frame, text="Zaloguj się", command=logowanie)

label_nazwa_uzytkownika.grid(row=0, column=0, sticky=W)
entry_nazwa_uzytkownika.grid(row=0, column=1)
label_haslo.grid(row=1, column=0, sticky=W)
entry_haslo.grid(row=1, column=1)
button_login.grid(row=2, column=0, columnspan=2)

login_frame.grid(row=0, column=0, padx=200, pady=100)

# Main frame
main_frame = Frame(root)
main_frame.grid_forget()

# Lista policjantów
label_lista_policjantow = Label(main_frame, text="Lista policjantów:")
label_lista_policjantow.grid(row=0, column=0, columnspan=3)
listbox_lista_policjantow = Listbox(main_frame, width=50)
listbox_lista_policjantow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly = Button(main_frame, text="Pokaż szczegóły", command=pokaz_szczegoly_policjanta)
button_pokaz_szczegoly.grid(row=2, column=0)
button_usun_policjanta = Button(main_frame, text="Usuń policjanta", command=usun_policjanta)
button_usun_policjanta.grid(row=2, column=1)
button_edytuj_policjanta = Button(main_frame, text="Edytuj policjanta", command=edytuj_policjanta)
button_edytuj_policjanta.grid(row=2, column=2)

# Formularz
label_formularz = Label(main_frame, text="Formularz")
label_formularz.grid(row=3, column=0, columnspan=2)
label_nazwa = Label(main_frame, text="Nazwa policjanta:")
label_nazwa.grid(row=4, column=0, sticky=W)
label_wsp_x = Label(main_frame, text="Współrzędne X:")
label_wsp_x.grid(row=5, column=0, sticky=W)
label_wsp_y = Label(main_frame, text="Współrzędne Y:")
label_wsp_y.grid(row=6, column=0, sticky=W)

entry_nazwa = Entry(main_frame)
entry_nazwa.grid(row=4, column=1)
entry_wsp_x = Entry(main_frame)
entry_wsp_x.grid(row=5, column=1)
entry_wsp_y = Entry(main_frame)
entry_wsp_y.grid(row=6, column=1)

button_dodaj_policjanta = Button(main_frame, text="Dodaj policjanta", command=dodaj_policjanta)
button_dodaj_policjanta.grid(row=7, column=0, columnspan=2)

# Szczegóły policjanta
label_szczegoly = Label(main_frame, text="Szczegóły policjanta:")
label_szczegoly.grid(row=8, column=0, sticky=W)
label_nazwa_szczegoly = Label(main_frame, text="Nazwa: ...")
label_nazwa_szczegoly.grid(row=9, column=0, sticky=W)
label_wspolrzedne_szczegoly = Label(main_frame, text="Współrzędne: ...")
label_wspolrzedne_szczegoly.grid(row=10, column=0, sticky=W)

# Wywołanie funkcji
lista_policjantow()

root.mainloop()
