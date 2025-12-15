import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Magazyn z Ilościami", page_icon="📦")

st.title("📦 Magazyn z zarządzaniem ilością")

# Inicjalizacja magazynu w sesji (słownik: nazwa -> ilość)
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = {"Chleb": 10, "Mleko": 5}

# --- SEKCJA DODAWANIA NOWEGO PRODUKTU ---
st.subheader("Dodaj nowy produkt do bazy")
col_a, col_b = st.columns([2, 1])

with col_a:
    nowy_towar = st.text_input("Nazwa nowego towaru:", placeholder="Np. Jabłka")
with col_b:
    ilosc_poczatkowa = st.number_input("Ilość startowa:", min_value=0, value=1)

if st.button("Dodaj do bazy"):
    if nowy_towar:
        if nowy_towar not in st.session_state.magazyn:
            st.session_state.magazyn[nowy_towar] = ilosc_poczatkowa
            st.success(f"Dodano produkt: {nowy_towar}")
            st.rerun()
        else:
            st.warning("Ten produkt już istnieje! Użyj przycisków poniżej, aby zmienić ilość.")
    else:
        st.error("Wpisz nazwę produktu.")

st.divider()

# --- SEKCJA ZARZĄDZANIA STANEM ---
st.subheader("Aktualne stany magazynowe")

if not st.session_state.magazyn:
    st.info("Magazyn jest pusty.")
else:
    # Nagłówki tabeli
    h1, h2, h3, h4 = st.columns([2, 2, 1, 1])
    h1.write("**Produkt**")
    h2.write("**Zmień ilość**")
    h3.write("**Stan**")
    h4.write("**Akcja**")

    # Wyświetlanie produktów
    # Tworzymy kopię kluczy, aby móc bezpiecznie usuwać elementy podczas iteracji
    for produkt in list(st.session_state.magazyn.keys()):
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        
        with c1:
            st.write(f"**{produkt}**")
        
        with c2:
            # Przyciski + i - w jednej linii
            sub_col1, sub_col2 = st.columns(2)
            if sub_col1.button("➕", key=f"add_{produkt}"):
                st.session_state.magazyn[produkt] += 1
                st.rerun()
            if sub_col2.button("➖", key=f"sub_{produkt}"):
                if st.session_state.magazyn[produkt] > 0:
                    st.session_state.magazyn[produkt] -= 1
                    st.rerun()
        
        with c3:
            st.write(f"{st.session_state.magazyn[produkt]} szt.")
            
        with c4:
            if st.button("Usuń", key=f"del_{produkt}"):
                del st.session_state.magazyn[produkt]
                st.rerun()
