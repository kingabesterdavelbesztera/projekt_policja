#SKRYPT2
from tkinter import *
from tkinter import messagebox
import requests
import tkintermapview
from bs4 import BeautifulSoup

# ustawienia
jednostki = []
zalogowany = False

class Jednostka:
    def __init__(self, nazwa, lokalizacja, policjanci):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.policjanci = policjanci
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"{self.nazwa} ({self.policjanci} policjantów)")

    def pobierz_wspolrzedne(self):
        url = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]

def dodaj_poczatkowe_jednostki():
    poczatkowe_jednostki = [
        {"nazwa": "Komisariat Wyszków", "lokalizacja": "Wyszków", "policjanci": 50},
        {"nazwa": "Komisariat Warszawa", "lokalizacja": "Warszawa", "policjanci": 1},
        {"nazwa": "Komisariat Ząbki", "lokalizacja": "Ząbki", "policjanci": 30},
        {"nazwa": "Komisariat Pruszków", "lokalizacja": "Pruszków", "policjanci": 40},
        {"nazwa": "Komisariat Kobyłka", "lokalizacja": "Kobyłka", "policjanci": 35}
    ]
    for jednostka in poczatkowe_jednostki:
        nowa_jednostka = Jednostka(jednostka["nazwa"], jednostka["lokalizacja"], jednostka["policjanci"])
        jednostki.append(nowa_jednostka)
    lista_jednostek()

def lista_jednostek():
    listbox_lista_jednostek.delete(0, END)
    for idx, jednostka in enumerate(jednostki):
        listbox_lista_jednostek.insert(idx, f'{jednostka.nazwa} {jednostka.lokalizacja} ({jednostka.policjanci} policjantów)')

def dodaj_jednostke():
    nazwa = entry_nazwa.get()
    lokalizacja = entry_lokalizacja.get()
    policjanci = int(entry_policjanci.get())
    nowa_jednostka = Jednostka(nazwa, lokalizacja, policjanci)
    jednostki.append(nowa_jednostka)
    lista_jednostek()
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_policjanci.delete(0, END)
    entry_nazwa.focus()

def usun_jednostke():
    i = listbox_lista_jednostek.index(ACTIVE)
    jednostki[i].marker.delete()
    jednostki.pop(i)
    lista_jednostek()

def pokaz_szczegoly_jednostki():
    i = listbox_lista_jednostek.index(ACTIVE)
    nazwa = jednostki[i].nazwa
    lokalizacja = jednostki[i].lokalizacja
    wspolrzedne = jednostki[i].wspolrzedne
    policjanci = jednostki[i].policjanci
    label_nazwa_szczegoly_jednostki_wartosc.config(text=nazwa)
    label_lokalizacja_szczegoly_jednostki_wartosc.config(text=lokalizacja)
    label_wspolrzedne_szczegoly_jednostki_wartosc.config(text=f"{wspolrzedne[0]:.2f}, {wspolrzedne[1]:.2f}")
    label_policjanci_szczegoly_jednostki_wartosc.config(text=policjanci)
    map_widget.set_position(wspolrzedne[0], wspolrzedne[1])
    map_widget.set_zoom(12)

def edytuj_jednostke():
    i = listbox_lista_jednostek.index(ACTIVE)
    entry_nazwa.insert(0, jednostki[i].nazwa)
    entry_lokalizacja.insert(0, jednostki[i].lokalizacja)
    entry_policjanci.insert(0, jednostki[i].policjanci)
    button_dodaj_jednostke.config(text="Zapisz zmiany", command=lambda: aktualizuj_jednostke(i))

def aktualizuj_jednostke(i):
    jednostki[i].nazwa = entry_nazwa.get()
    jednostki[i].lokalizacja = entry_lokalizacja.get()
    jednostki[i].policjanci = int(entry_policjanci.get())
    jednostki[i].wspolrzedne = jednostki[i].pobierz_wspolrzedne()
    jednostki[i].marker.delete()
    jednostki[i].marker = map_widget.set_marker(jednostki[i].wspolrzedne[0], jednostki[i].wspolrzedne[1], text=f"{jednostki[i].nazwa} ({jednostki[i].policjanci} policjantów)")
    lista_jednostek()
    button_dodaj_jednostke.config(text="Dodaj jednostkę", command=dodaj_jednostke)
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_policjanci.delete(0, END)
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

# GUI
root = Tk()
root.title("MapBook")
root.geometry("1100x900")

# Login ramka
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

# Główna ramka
main_frame = Frame(root)
main_frame.grid_forget()

# ramka do organizowania struktury
ramka_lista_jednostek = Frame(main_frame)
ramka_formularz = Frame(main_frame)
ramka_szczegoly_jednostki = Frame(main_frame)

ramka_lista_jednostek.grid(row=0, column=0, padx=50)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_jednostki.grid(row=1, column=0, columnspan=2, padx=50, pady=20)

# lista jednostek
label_lista_jednostek = Label(ramka_lista_jednostek, text="Lista jednostek: ")
listbox_lista_jednostek = Listbox(ramka_lista_jednostek, width=50)
button_pokaz_szczegoly = Button(ramka_lista_jednostek, text="Pokaż szczegóły", command=pokaz_szczegoly_jednostki)
button_usun_jednostke = Button(ramka_lista_jednostek, text="Usuń jednostkę", command=usun_jednostke)
button_edytuj_jednostke = Button(ramka_lista_jednostek, text="Edytuj jednostkę", command=edytuj_jednostke)

label_lista_jednostek.grid(row=0, column=0, columnspan=3)
listbox_lista_jednostek.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly.grid(row=2, column=0)
button_usun_jednostke.grid(row=2, column=1)
button_edytuj_jednostke.grid(row=2, column=2)

# formularz dodawania jednostek
label_nazwa = Label(ramka_formularz, text="Nazwa jednostki:")
label_lokalizacja = Label(ramka_formularz, text="Lokalizacja:")
label_policjanci = Label(ramka_formularz, text="Liczba policjantów:")

entry_nazwa = Entry(ramka_formularz)
entry_lokalizacja = Entry(ramka_formularz)
entry_policjanci = Entry(ramka_formularz)

button_dodaj_jednostke = Button(ramka_formularz, text="Dodaj jednostkę", command=dodaj_jednostke)

label_nazwa.grid(row=0, column=0, sticky=W)
entry_nazwa.grid(row=0, column=1)
label_lokalizacja.grid(row=1, column=0, sticky=W)
entry_lokalizacja.grid(row=1, column=1)
label_policjanci.grid(row=2, column=0, sticky=W)
entry_policjanci.grid(row=2, column=1)
button_dodaj_jednostke.grid(row=3, column=0, columnspan=2)

# szczegóły jednostki
label_szczegoly_jednostki = Label(ramka_szczegoly_jednostki, text="Szczegóły jednostki", font=("Helvetica", 14, "bold"))
label_nazwa_szczegoly_jednostki = Label(ramka_szczegoly_jednostki, text="Nazwa:")
label_nazwa_szczegoly_jednostki_wartosc = Label(ramka_szczegoly_jednostki, text="")
label_lokalizacja_szczegoly_jednostki = Label(ramka_szczegoly_jednostki, text="Lokalizacja:")
label_lokalizacja_szczegoly_jednostki_wartosc = Label(ramka_szczegoly_jednostki, text="")
label_wspolrzedne_szczegoly_jednostki = Label(ramka_szczegoly_jednostki, text="Współrzędne:")
label_wspolrzedne_szczegoly_jednostki_wartosc = Label(ramka_szczegoly_jednostki, text="")
label_policjanci_szczegoly_jednostki = Label(ramka_szczegoly_jednostki, text="Liczba policjantów:")
label_policjanci_szczegoly_jednostki_wartosc = Label(ramka_szczegoly_jednostki, text="")

label_szczegoly_jednostki.grid(row=0, column=0, columnspan=2)
label_nazwa_szczegoly_jednostki.grid(row=1, column=0, sticky=W)
label_nazwa_szczegoly_jednostki_wartosc.grid(row=1, column=1, sticky=W)
label_lokalizacja_szczegoly_jednostki.grid(row=2, column=0, sticky=W)
label_lokalizacja_szczegoly_jednostki_wartosc.grid(row=2, column=1, sticky=W)
label_wspolrzedne_szczegoly_jednostki.grid(row=3, column=0, sticky=W)
label_wspolrzedne_szczegoly_jednostki_wartosc.grid(row=3, column=1, sticky=W)
label_policjanci_szczegoly_jednostki.grid(row=4, column=0, sticky=W)
label_policjanci_szczegoly_jednostki_wartosc.grid(row=4, column=1, sticky=W)

map_widget = tkintermapview.TkinterMapView(ramka_szczegoly_jednostki, width=800, height=400, corner_radius=0)
map_widget.grid(row=5, column=0, columnspan=2)

root.mainloop()
