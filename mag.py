import streamlit as st

# 1. Inicjalizacja danych w sesji
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = []

if 'kategorie' not in st.session_state:
    # Początkowe domyślne kategorie
    st.session_state.kategorie = ["Ogólne", "Spożywcze", "Elektronika"]

st.title("📦 Magazyn z własnymi kategoriami")

# --- PANEL BOCZNY: Zarządzanie Kategoriami ---
st.sidebar.header("Ustawienia Kategorii")
nowa_kat = st.sidebar.text_input("Nazwa nowej kategorii")
if st.sidebar.button("Dodaj kategorię"):
    if nowa_kat and nowa_kat not in st.session_state.kategorie:
        st.session_state.kategorie.append(nowa_kat)
        st.sidebar.success(f"Dodano kategorię: {nowa_kat}")
    elif nowa_kat in st.session_state.kategorie:
        st.sidebar.warning("Ta kategoria już istnieje.")

st.sidebar.divider()

# --- PANEL BOCZNY: Dodawanie produktów ---
st.sidebar.header("Dodaj nowy towar")
nazwa = st.sidebar.text_input("Nazwa towaru")
# Lista rozwijana korzysta teraz z dynamicznej listy st.session_state.kategorie
kategoria = st.sidebar.selectbox("Wybierz kategorię", st.session_state.kategorie)
ilosc = st.sidebar.number_input("Ilość", min_value=1, value=1)

if st.sidebar.button("Dodaj do magazynu"):
    if nazwa:
        nowy_towar = {"nazwa": nazwa, "kategoria": kategoria, "ilosc": ilosc}
        st.session_state.magazyn.append(nowy_towar)
        st.success(f"Dodano: {nazwa}")
    else:
        st.error("Podaj nazwę towaru!")

# --- GŁÓWNA SEKCJA: Lista i Usuwanie ---
st.subheader("Aktualny stan magazynu")

if not st.session_state.magazyn:
    st.info("Magazyn jest pusty. Dodaj pierwszy produkt w panelu bocznym.")
else:
    for i, towar in enumerate(st.session_state.magazyn):
        cols = st.columns([3, 2, 1, 1])
        cols[0].write(f"**{towar['nazwa']}**")
        cols[1].write(f"📁 {towar['kategoria']}")
        cols[2].write(f"szt: {towar['ilosc']}")
        
        if cols[3].button("Usuń", key=f"del_{i}"):
            st.session_state.magazyn.pop(i)
            st.rerun()

# --- RAPORT ---
st.divider()
st.subheader("📊 Raport o stanie magazynu")

if st.button("Generuj raport"):
    if st.session_state.magazyn:
        # Grupowanie danych
        raport = {}
        for t in st.session_state.magazyn:
            kat = t['kategoria']
            raport[kat] = raport.get(kat, 0) + t['ilosc']
        
        # Wyświetlanie wyników
        for kat, suma in raport.items():
            st.info(f"Kategoria **{kat}**: {suma} sztuk łącznie")
        
        st.write(f"Łączna liczba unikalnych produktów: {len(st.session_state.magazyn)}")
    else:
        st.warning("Magazyn jest pusty – nie można wygenerować raportu.")
