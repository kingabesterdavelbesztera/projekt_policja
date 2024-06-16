#SKRYPT1
from tkinter import *
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import tkintermapview

# ustawienia
jednostki = []
zalogowany = False

class Jednostki:
    def __init__(self, nazwa, lokalizacja):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=self.nazwa)

    def pobierz_wspolrzedne(self):
        url = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]

def lista_jednostek():
    listbox_lista_jednostek.delete(0, END)
    for idx, jednostka in enumerate(jednostki):
        listbox_lista_jednostek.insert(idx, f'{jednostka.nazwa} {jednostka.lokalizacja}')

def dodaj_jednostke():
    nazwa = entry_nazwa.get()
    lokalizacja = entry_lokalizacja.get()
    nowa_jednostka = Jednostki(nazwa, lokalizacja)
    jednostki.append(nowa_jednostka)
    lista_jednostek()
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_nazwa.focus()

def usun_jednostke():
    i = listbox_lista_jednostek.index(ACTIVE)
    jednostki[i].marker.delete()
    jednostki.pop(i)
    lista_jednostek()

def pokaz_szczegoly_jednostek():
    i = listbox_lista_jednostek.index(ACTIVE)
    nazwa = jednostki[i].nazwa
    lokalizacja = jednostki[i].lokalizacja
    wspolrzedne = jednostki[i].wspolrzedne
    label_nazwa_szczegoly_jednostki_wartosc.config(text=nazwa)
    label_lokalizacja_szczegoly_jednostki_wartosc.config(text=lokalizacja)
    label_wspolrzedne_szczegoly_jednostki_wartosc.config(text=f"{wspolrzedne[0]:.2f}, {wspolrzedne[1]:.2f}")
    map_widget.set_position(wspolrzedne[0], wspolrzedne[1])
    map_widget.set_zoom(12)

def edytuj_jednostke():
    i = listbox_lista_jednostek.index(ACTIVE)
    entry_nazwa.insert(0, jednostki[i].nazwa)
    entry_lokalizacja.insert(0, jednostki[i].lokalizacja)
    button_dodaj_jednostke.config(text="Zapisz zmiany", command=lambda: aktualizuj_jednostke(i))

def aktualizuj_jednostke(i):
    jednostki[i].nazwa = entry_nazwa.get()
    jednostki[i].lokalizacja = entry_lokalizacja.get()
    jednostki[i].wspolrzedne = jednostki[i].pobierz_wspolrzedne()
    jednostki[i].marker.delete()
    jednostki[i].marker = map_widget.set_marker(jednostki[i].wspolrzedne[0], jednostki[i].wspolrzedne[1], text=jednostki[i].nazwa)
    lista_jednostek()
    button_dodaj_jednostke.config(text="Dodaj jednostkę", command=dodaj_jednostke)
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_nazwa.focus()

def logowanie():
    global zalogowany
    nazwa_uzytkownika = entry_nazwa_uzytkownika.get()
    haslo = entry_haslo.get()
    if nazwa_uzytkownika == "user" and haslo == "user":
        zalogowany = True
        login_frame.grid_forget()
        main_frame.grid(row=0, column=0, padx=50)
        dodaj_poczatkowe_jednostki()
    else:
        messagebox.showerror("Błąd logowania", "Niepoprawna nazwa użytkownika lub hasło")

def dodaj_poczatkowe_jednostki():
    poczatkowe_jednostki = [
        {"nazwa": "Komisariat Wyszków,", 'lokalizacja': 'Wyszków'},
        {"nazwa": "Komisariat Warszawa,", 'lokalizacja': 'Warszawa'},
        {"nazwa": "Komisariat Ząbki,", 'lokalizacja': 'Ząbki'},
        {"nazwa": "Komisariat Pruszków,", 'lokalizacja': 'Pruszków'},
        {"nazwa": "Komisariat Kobyłka,", 'lokalizacja': 'Kobyłka'}
    ]
    for jednostka in poczatkowe_jednostki:
        nowe_jednostki = Jednostki(jednostka["nazwa"], jednostka["lokalizacja"])
        jednostki.append(nowe_jednostki)
    lista_jednostek()

# GUI
root = Tk()
root.title("MapBook")
root.geometry("1100x900")

# Login Frame
login_frame = Frame(root)
label_nazwa_uzytkownika = Label(login_frame, text="Nazwa użytkownika:")
entry_nazwa_uzytkownika = Entry(login_frame)
label_haslo = Label(login_frame, text="Hasło:")
entry_haslo = Entry(login_frame, show="*")
button_login = Button(login_frame, text="Zaloguj się", command=logowanie)

label_nazwa_uzytkownika.grid(row=5, column=5, sticky=W)
entry_nazwa_uzytkownika.grid(row=5, column=6)
label_haslo.grid(row=6, column=5, sticky=W)
entry_haslo.grid(row=6, column=6)
button_login.grid(row=7, column=5, columnspan=2)

login_frame.grid(row=5, column=5, padx=400, pady=100)

# Główna Frame
main_frame = Frame(root)
main_frame.grid_forget()

# Frames do organizowania struktury
ramka_lista_jednostek = Frame(main_frame)
ramka_formularz = Frame(main_frame)
ramka_szczegoly_jednostek = Frame(main_frame)

ramka_lista_jednostek.grid(row=0, column=0, padx=50)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_jednostek.grid(row=1, column=0, columnspan=2, padx=50, pady=20)

# lista jednostek
label_lista_jednostek = Label(ramka_lista_jednostek, text="Lista jednostek: ")
listbox_lista_jednostek = Listbox(ramka_lista_jednostek, width=50)
button_pokaz_szczegoly = Button(ramka_lista_jednostek, text="Pokaż szczegóły", command=pokaz_szczegoly_jednostek)
button_usun_jednostke = Button(ramka_lista_jednostek, text="Usuń jednostkę", command=usun_jednostke)
button_edytuj_jednostke = Button(ramka_lista_jednostek, text="Edytuj jednostkę", command=edytuj_jednostke)

label_lista_jednostek.grid(row=0, column=0, columnspan=3)
listbox_lista_jednostek.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly.grid(row=2, column=0)
button_usun_jednostke.grid(row=2, column=1)
button_edytuj_jednostke.grid(row=2, column=2)

# formularz
label_formularz = Label(ramka_formularz, text="Formularz")
label_nazwa = Label(ramka_formularz, text="Nazwa jednostki: ")
label_lokalizacja = Label(ramka_formularz, text="Lokalizacja jednostki: ")

entry_nazwa = Entry(ramka_formularz)
entry_lokalizacja = Entry(ramka_formularz)

label_formularz.grid(row=0, column=0, columnspan=2)
label_nazwa.grid(row=1, column=0, sticky=W)
label_lokalizacja.grid(row=2, column=0, sticky=W)

entry_nazwa.grid(row=1, column=1)
entry_lokalizacja.grid(row=2, column=1)

button_dodaj_jednostke = Button(ramka_formularz, text="Dodaj jednostkę", command=dodaj_jednostke)
button_dodaj_jednostke.grid(row=3, column=1, columnspan=2)

# szczegóły jednostek
label_szczegoly_jednostek = Label(ramka_szczegoly_jednostek, text="Szczegóły jednostek: ")
label_nazwa_szczegoly_jednostki = Label(ramka_szczegoly_jednostek, text="Nazwa: ")
label_lokalizacja_szczegoly_jednostki = Label(ramka_szczegoly_jednostek, text="Lokalizacja: ")
label_wspolrzedne_szczegoly_jednostki = Label(ramka_szczegoly_jednostek, text="Współrzędne: ")

label_nazwa_szczegoly_jednostki_wartosc = Label(ramka_szczegoly_jednostek, text="...", width=30)
label_lokalizacja_szczegoly_jednostki_wartosc = Label(ramka_szczegoly_jednostek, text="...", width=20)
label_wspolrzedne_szczegoly_jednostki_wartosc = Label(ramka_szczegoly_jednostek, text="...", width=20)

label_szczegoly_jednostek.grid(row=0, column=0, sticky=W)
label_nazwa_szczegoly_jednostki.grid(row=1, column=0, sticky=W)
label_nazwa_szczegoly_jednostki_wartosc.grid(row=1, column=1)
label_lokalizacja_szczegoly_jednostki.grid(row=1, column=2)
label_lokalizacja_szczegoly_jednostki_wartosc.grid(row=1, column=3)
label_wspolrzedne_szczegoly_jednostki.grid(row=1, column=4)
label_wspolrzedne_szczegoly_jednostki_wartosc.grid(row=1, column=5)

map_widget = tkintermapview.TkinterMapView(ramka_szczegoly_jednostek, width=900, height=500)
map_widget.set_position(52.2, 21.0)
map_widget.set_zoom(8)

map_widget.grid(row=2, column=0, columnspan=8)

root.mainloop()
