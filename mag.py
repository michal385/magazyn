import streamlit as st

# 1. Inicjalizacja danych (Session State)
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = []

if 'kategorie' not in st.session_state:
    st.session_state.kategorie = ["Ogólne", "Spożywcze", "Elektronika"]

st.set_page_config(page_title="Magazyn v2", layout="wide")
st.title("📦 Prosty Magazyn z Zarządzaniem Kategoriami")

# --- PANEL BOCZNY: Kategorie ---
st.sidebar.header("⚙️ Zarządzanie Kategoriami")

# Dodawanie kategorii
nowa_kat = st.sidebar.text_input("Dodaj nową kategorię")
if st.sidebar.button("Dodaj"):
    if nowa_kat and nowa_kat not in st.session_state.kategorie:
        st.session_state.kategorie.append(nowa_kat)
        st.rerun()

st.sidebar.write("---")

# Usuwanie kategorii
st.sidebar.subheader("Usuń kategorię")
kat_do_usuniecia = st.sidebar.selectbox("Wybierz kategorię do usunięcia", st.session_state.kategorie)
if st.sidebar.button("Usuń kategorię"):
    # Sprawdzenie, czy kategoria jest używana przez jakiś towar
    uzywana = any(p['kategoria'] == kat_do_usuniecia for p in st.session_state.magazyn)
    
    if uzywana:
        st.sidebar.error("Nie można usunąć kategorii, która jest przypisana do produktów!")
    elif len(st.session_state.kategorie) <= 1:
        st.sidebar.warning("Musi zostać przynajmniej jedna kategoria.")
    else:
        st.session_state.kategorie.remove(kat_do_usuniecia)
        st.rerun()

# --- GŁÓWNA SEKCJA: Dodawanie towaru ---
st.subheader("➕ Dodaj nowy towar")
c1, c2, c3, c4 = st.columns([3, 2, 1, 1])

with c1:
    nazwa_t = st.text_input("Nazwa produktu", key="nazwa_t")
with c2:
    kat_t = st.selectbox("Wybierz kategorię", st.session_state.kategorie)
with c3:
    ilosc_t = st.number_input("Ilość", min_value=1, value=1)
with c4:
    st.write(" ") # Odstęp dla wyrównania
    if st.button("Dodaj produkt"):
        if nazwa_t:
            st.session_state.magazyn.append({
                "nazwa": nazwa_t,
                "kategoria": kat_t,
                "ilosc": ilosc_t
            })
            st.rerun()
        else:
            st.error("Podaj nazwę!")

st.divider()

# --- LISTA TOWARÓW ---
st.subheader("📋 Lista towarów w magazynie")

if not st.session_state.magazyn:
    st.info("Magazyn jest pusty.")
else:
    for i, p in enumerate(st.session_state.magazyn):
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        col1.write(f"**{p['nazwa']}**")
        col2.write(f"📁 {p['kategoria']}")
        col3.write(f"{p['ilosc']} szt.")
        if col4.button("Usuń", key=f"del_{i}"):
            st.session_state.magazyn.pop(i)
            st.rerun()

# --- RAPORT ---
st.divider()
if st.button("📊 Generuj raport stanu"):
    st.subheader("Raport zbiorczy")
    if st.session_state.magazyn:
        raport = {}
        for p in st.session_state.magazyn:
            k = p['kategoria']
            raport[k] = raport.get(k, 0) + p['ilosc']
        
        # Wyświetlenie statystyk
        st.table(list(raport.items()))
        st.write(f"**Łączna liczba wszystkich przedmiotów:** {sum(raport.values())}")
    else:
        st.warning("Brak danych do raportu.")
