#SKRYPT2
from tkinter import *
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import tkintermapview

# ustawienia
jednostki = []
policjanci = []
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

class Policjant:
    def __init__(self, nazwa, wsp_x, wsp_y, komisariat):
        self.nazwa = nazwa
        self.wspolrzedne = (wsp_x, wsp_y)
        self.komisariat = komisariat
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=self.nazwa)

def lista_jednostek():
    listbox_lista_jednostek.delete(0, END)
    for idx, jednostka in enumerate(jednostki):
        listbox_lista_jednostek.insert(idx, f'{jednostka.nazwa} {jednostka.lokalizacja}')

def lista_policjantow():
    listbox_lista_policjantow.delete(0, END)
    for idx, policjant in enumerate(policjanci):
        listbox_lista_policjantow.insert(idx, f'{policjant.nazwa} {policjant.komisariat}')

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
    jednostka = jednostki[i]
    label_nazwa_szczegoly_jednostki_wartosc.config(text=jednostka.nazwa)
    label_lokalizacja_szczegoly_jednostki_wartosc.config(text=jednostka.lokalizacja)
    label_wspolrzedne_szczegoly_jednostki_wartosc.config(text=f"{jednostka.wspolrzedne[0]:.2f}, {jednostka.wspolrzedne[1]:.2f}")
    map_widget.set_position(jednostka.wspolrzedne[0], jednostka.wspolrzedne[1])
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

def dodaj_policjanta():
    nazwa = entry_nazwa_policjanta.get()
    wsp_x = float(entry_wsp_x.get())
    wsp_y = float(entry_wsp_y.get())
    komisariat = entry_komisariat.get()
    nowy_policjant = Policjant(nazwa, wsp_x, wsp_y, komisariat)
    policjanci.append(nowy_policjant)
    lista_policjantow()
    entry_nazwa_policjanta.delete(0, END)
    entry_wsp_x.delete(0, END)
    entry_wsp_y.delete(0, END)
    entry_komisariat.delete(0, END)
    entry_nazwa_policjanta.focus()

def usun_policjanta():
    i = listbox_lista_policjantow.index(ACTIVE)
    policjanci[i].marker.delete()
    policjanci.pop(i)
    lista_policjantow()

def pokaz_szczegoly_policjanta():
    i = listbox_lista_policjantow.index(ACTIVE)
    policjant = policjanci[i]
    label_nazwa_szczegoly_policjanta_wartosc.config(text=policjant.nazwa)
    label_komisariat_szczegoly_policjanta_wartosc.config(text=policjant.komisariat)
    label_wspolrzedne_szczegoly_policjanta_wartosc.config(text=f"{policjant.wspolrzedne[0]}, {policjant.wspolrzedne[1]}")
    # Znajdź komisariat policjanta i ustaw mapę na jego pozycję
    for jednostka in jednostki:
        if jednostka.nazwa == policjant.komisariat:
            map_widget.set_position(jednostka.wspolrzedne[0], jednostka.wspolrzedne[1])
            map_widget.set_zoom(12)
            break

def edytuj_policjanta():
    i = listbox_lista_policjantow.index(ACTIVE)
    entry_nazwa_policjanta.insert(0, policjanci[i].nazwa)
    entry_wsp_x.insert(0, policjanci[i].wspolrzedne[0])
    entry_wsp_y.insert(0, policjanci[i].wspolrzedne[1])
    entry_komisariat.insert(0, policjanci[i].komisariat)
    button_dodaj_policjanta.config(text="Zapisz zmiany", command=lambda: aktualizuj_policjanta(i))

def aktualizuj_policjanta(i):
    policjanci[i].nazwa = entry_nazwa_policjanta.get()
    policjanci[i].wspolrzedne = (float(entry_wsp_x.get()), float(entry_wsp_y.get()))
    policjanci[i].komisariat = entry_komisariat.get()
    policjanci[i].marker.delete()
    policjanci[i].marker = map_widget.set_marker(policjanci[i].wspolrzedne[0], policjanci[i].wspolrzedne[1], text=policjanci[i].nazwa)
    lista_policjantow()
    button_dodaj_policjanta.config(text="Dodaj policjanta", command=dodaj_policjanta)
    entry_nazwa_policjanta.delete(0, END)
    entry_wsp_x.delete(0, END)
    entry_wsp_y.delete(0, END)
    entry_komisariat.delete(0, END)
    entry_nazwa_policjanta.focus()

def logowanie():
    global zalogowany
    nazwa_uzytkownika = entry_nazwa_uzytkownika.get()
    haslo = entry_haslo.get()
    if nazwa_uzytkownika == "user" and haslo == "user":
        zalogowany = True
        login_frame.grid_forget()
        main_frame.grid(row=0, column=0, padx=50)
        dodaj_poczatkowe_jednostki()
        dodaj_poczatkowych_policjantow()
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

def dodaj_poczatkowych_policjantow():
    poczatkowi_policjanci = [
        {"nazwa": "Jan Kowalski", 'wsp_x': 52.59, 'wsp_y': 21.459, 'komisariat': 'Komisariat Wyszków,'},
        {"nazwa": "Adam Nowak", 'wsp_x': 52.23, 'wsp_y': 21.008, 'komisariat': 'Komisariat Warszawa,'},
        {"nazwa": "Ewa Wiśniewska", 'wsp_x': 52.292, 'wsp_y': 21.116, 'komisariat': 'Komisariat Ząbki,'},
        {"nazwa": "Marek Kowal", 'wsp_x': 52.165, 'wsp_y': 20.805556, 'komisariat': 'Komisariat Pruszków,'},
        {"nazwa": "Anna Kwiatkowska", 'wsp_x': 52.339, 'wsp_y': 21.195, 'komisariat': 'Komisariat Kobyłka,'}
    ]
    for policjant in poczatkowi_policjanci:
        nowy_policjant = Policjant(policjant["nazwa"], policjant["wsp_x"], policjant["wsp_y"], policjant["komisariat"])
        policjanci.append(nowy_policjant)
    lista_policjantow()

# GUI
root = Tk()
root.title("Jednostki Policyjne")
root.geometry("1200x1000")

# Login Frame
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

login_frame.grid(row=0, column=0, padx=400, pady=100)

# Główna Frame
main_frame = Frame(root)
main_frame.grid_forget()

# Frames do organizowania struktury
ramka_lista_jednostek = Frame(main_frame)
ramka_lista_policjantow = Frame(main_frame)
ramka_formularz_jednostki = Frame(main_frame)
ramka_formularz_policjant = Frame(main_frame)
ramka_szczegoly_jednostek = Frame(main_frame)
ramka_szczegoly_policjantow = Frame(main_frame)

ramka_lista_jednostek.grid(row=0, column=0, padx=20)
ramka_lista_policjantow.grid(row=0, column=1, padx=20)
ramka_formularz_jednostki.grid(row=1, column=0, padx=20, pady=20)
ramka_formularz_policjant.grid(row=1, column=1, padx=20, pady=20)
ramka_szczegoly_jednostek.grid(row=2, column=0, columnspan=2, padx=20, pady=20)
ramka_szczegoly_policjantow.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

# lista jednostek
label_lista_jednostek = Label(ramka_lista_jednostek, text="Lista jednostek: ")
listbox_lista_jednostek = Listbox(ramka_lista_jednostek, width=50)
button_pokaz_szczegoly_jednostki = Button(ramka_lista_jednostek, text="Pokaż szczegóły", command=pokaz_szczegoly_jednostek)
button_usun_jednostke = Button(ramka_lista_jednostek, text="Usuń jednostkę", command=usun_jednostke)
button_edytuj_jednostke = Button(ramka_lista_jednostek, text="Edytuj jednostkę", command=edytuj_jednostke)

label_lista_jednostek.grid(row=0, column=0, columnspan=3)
listbox_lista_jednostek.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_jednostki.grid(row=2, column=0)
button_usun_jednostke.grid(row=2, column=1)
button_edytuj_jednostke.grid(row=2, column=2)

# lista policjantów
label_lista_policjantow = Label(ramka_lista_policjantow, text="Lista policjantów: ")
listbox_lista_policjantow = Listbox(ramka_lista_policjantow, width=50)
button_pokaz_szczegoly_policjant = Button(ramka_lista_policjantow, text="Pokaż szczegóły", command=pokaz_szczegoly_policjanta)
button_usun_policjanta = Button(ramka_lista_policjantow, text="Usuń policjanta", command=usun_policjanta)
button_edytuj_policjanta = Button(ramka_lista_policjantow, text="Edytuj policjanta", command=edytuj_policjanta)

label_lista_policjantow.grid(row=0, column=0, columnspan=3)
listbox_lista_policjantow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_policjant.grid(row=2, column=0)
button_usun_policjanta.grid(row=2, column=1)
button_edytuj_policjanta.grid(row=2, column=2)

# formularz jednostek
label_formularz_jednostki = Label(ramka_formularz_jednostki, text="Formularz jednostki")
label_nazwa = Label(ramka_formularz_jednostki, text="Nazwa jednostki: ")
label_lokalizacja = Label(ramka_formularz_jednostki, text="Lokalizacja jednostki: ")

entry_nazwa = Entry(ramka_formularz_jednostki)
entry_lokalizacja = Entry(ramka_formularz_jednostki)

label_formularz_jednostki.grid(row=0, column=0, columnspan=2)
label_nazwa.grid(row=1, column=0, sticky=W)
label_lokalizacja.grid(row=2, column=0, sticky=W)

entry_nazwa.grid(row=1, column=1)
entry_lokalizacja.grid(row=2, column=1)

button_dodaj_jednostke = Button(ramka_formularz_jednostki, text="Dodaj jednostkę", command=dodaj_jednostke)
button_dodaj_jednostke.grid(row=3, column=1, columnspan=2)

# formularz policjantów
label_formularz_policjant = Label(ramka_formularz_policjant, text="Formularz policjanta")
label_nazwa_policjanta = Label(ramka_formularz_policjant, text="Nazwa policjanta: ")
label_wsp_x = Label(ramka_formularz_policjant, text="Współrzędna X: ")
label_wsp_y = Label(ramka_formularz_policjant, text="Współrzędna Y: ")
label_komisariat = Label(ramka_formularz_policjant, text="Komisariat: ")

entry_nazwa_policjanta = Entry(ramka_formularz_policjant)
entry_wsp_x = Entry(ramka_formularz_policjant)
entry_wsp_y = Entry(ramka_formularz_policjant)
entry_komisariat = Entry(ramka_formularz_policjant)

label_formularz_policjant.grid(row=0, column=0, columnspan=2)
label_nazwa_policjanta.grid(row=1, column=0, sticky=W)
label_wsp_x.grid(row=2, column=0, sticky=W)
label_wsp_y.grid(row=3, column=0, sticky=W)
label_komisariat.grid(row=4, column=0, sticky=W)

entry_nazwa_policjanta.grid(row=1, column=1)
entry_wsp_x.grid(row=2, column=1)
entry_wsp_y.grid(row=3, column=1)
entry_komisariat.grid(row=4, column=1)

button_dodaj_policjanta = Button(ramka_formularz_policjant, text="Dodaj policjanta", command=dodaj_policjanta)
button_dodaj_policjanta.grid(row=5, column=1, columnspan=2)

# szczegóły jednostek
label_szczegoly_jednostki = Label(ramka_szczegoly_jednostek, text="Szczegóły jednostki")
label_nazwa_szczegoly_jednostki = Label(ramka_szczegoly_jednostek, text="Nazwa jednostki: ")
label_lokalizacja_szczegoly_jednostki = Label(ramka_szczegoly_jednostek, text="Lokalizacja jednostki: ")
label_wspolrzedne_szczegoly_jednostki = Label(ramka_szczegoly_jednostek, text="Współrzędne jednostki: ")

label_nazwa_szczegoly_jednostki_wartosc = Label(ramka_szczegoly_jednostek, text="")
label_lokalizacja_szczegoly_jednostki_wartosc = Label(ramka_szczegoly_jednostek, text="")
label_wspolrzedne_szczegoly_jednostki_wartosc = Label(ramka_szczegoly_jednostek, text="")

label_szczegoly_jednostki.grid(row=0, column=0, columnspan=2)
label_nazwa_szczegoly_jednostki.grid(row=1, column=0, sticky=W)
label_lokalizacja_szczegoly_jednostki.grid(row=2, column=0, sticky=W)
label_wspolrzedne_szczegoly_jednostki.grid(row=3, column=0, sticky=W)

label_nazwa_szczegoly_jednostki_wartosc.grid(row=1, column=1, sticky=W)
label_lokalizacja_szczegoly_jednostki_wartosc.grid(row=2, column=1, sticky=W)
label_wspolrzedne_szczegoly_jednostki_wartosc.grid(row=3, column=1, sticky=W)

# szczegóły policjantów
label_szczegoly_policjant = Label(ramka_szczegoly_policjantow, text="Szczegóły policjanta")
label_nazwa_szczegoly_policjant = Label(ramka_szczegoly_policjantow, text="Nazwa policjanta: ")
label_komisariat_szczegoly_policjant = Label(ramka_szczegoly_policjantow, text="Komisariat: ")
label_wspolrzedne_szczegoly_policjant = Label(ramka_szczegoly_policjantow, text="Współrzędne policjanta: ")

label_nazwa_szczegoly_policjanta_wartosc = Label(ramka_szczegoly_policjantow, text="")
label_komisariat_szczegoly_policjanta_wartosc = Label(ramka_szczegoly_policjantow, text="")
label_wspolrzedne_szczegoly_policjanta_wartosc = Label(ramka_szczegoly_policjantow, text="")

label_szczegoly_policjant.grid(row=0, column=0, columnspan=2)
label_nazwa_szczegoly_policjant.grid(row=1, column=0, sticky=W)
label_komisariat_szczegoly_policjant.grid(row=2, column=0, sticky=W)
label_wspolrzedne_szczegoly_policjant.grid(row=3, column=0, sticky=W)

label_nazwa_szczegoly_policjanta_wartosc.grid(row=1, column=1, sticky=W)
label_komisariat_szczegoly_policjanta_wartosc.grid(row=2, column=1, sticky=W)
label_wspolrzedne_szczegoly_policjanta_wartosc.grid(row=3, column=1, sticky=W)

# Mapa
map_frame = Frame(main_frame)
map_frame.grid(row=0, column=2, rowspan=4, padx=20, pady=20)

map_widget = tkintermapview.TkinterMapView(map_frame, width=600, height=600, corner_radius=0)
map_widget.set_position(52.237049, 21.017532)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0)

root.mainloop()