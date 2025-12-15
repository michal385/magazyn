import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Prosty Magazyn", page_icon="📦")

st.title("📦 System Zarządzania Magazynem")

# Inicjalizacja listy w sesji, jeśli jeszcze nie istnieje
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = ["Chleb", "Mleko", "Woda"]

# --- SEKCJA DODAWANIA ---
st.subheader("Dodaj nowy towar")
nowy_towar = st.text_input("Nazwa towaru:", placeholder="Wpisz co chcesz dodać...")

if st.button("Dodaj do magazynu"):
    if nowy_towar:
        if nowy_towar not in st.session_state.magazyn:
            st.session_state.magazyn.append(nowy_towar)
            st.success(f"Dodano: {nowy_towar}")
        else:
            st.warning("Ten towar już jest na liście!")
    else:
        st.error("Pole nie może być puste.")

st.divider()

# --- SEKCJA LISTY I USUWANIA ---
st.subheader("Aktualny stan magazynu")

if not st.session_state.magazyn:
    st.info("Magazyn jest pusty.")
else:
    for index, towar in enumerate(st.session_state.magazyn):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**{index + 1}.** {towar}")
        
        with col2:
            # Każdy przycisk musi mieć unikalny klucz (key)
            if st.button("Usuń", key=f"btn_{index}"):
                st.session_state.magazyn.pop(index)
                st.rerun() # Odśwież stronę po usunięciu
