import streamlit as st

# Inicjalizacja magazynu w sesji (dzięki temu dane nie znikają po kliknięciu przycisku)
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = []

st.title("📦 Prosty System Magazynowy")

# --- PANEL BOCZNY: Dodawanie produktów ---
st.sidebar.header("Dodaj nowy towar")
nazwa = st.sidebar.text_input("Nazwa towaru")
kategoria = st.sidebar.selectbox("Kategoria", ["Spożywcze", "Elektronika", "Dom i Ogród", "Inne"])
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
    st.info("Magazyn jest pusty.")
else:
    # Wyświetlanie listy towarów z opcją usunięcia
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
        # Grupowanie danych do raportu
        raport = {}
        for t in st.session_state.magazyn:
            kat = t['kategoria']
            raport[kat] = raport.get(kat, 0) + t['ilosc']
        
        st.write("Podsumowanie ilościowe wg kategorii:")
        for kat, suma in raport.items():
            st.info(f"{kat}: **{suma} szt.**")
        
        st.write(f"Całkowita liczba pozycji w magazynie: {len(st.session_state.magazyn)}")
    else:
        st.warning("Brak danych do wygenerowania raportu.")
