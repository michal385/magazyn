import streamlit as st
from supabase import create_client, Client

# --- POŁĄCZENIE Z SUPABASE ---
# Klucze muszą być dodane w Streamlit Cloud -> Settings -> Secrets
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

st.title("📦 Magazyn Cloud (Supabase)")

# --- FUNKCJE POMOCNICZE ---
def pobierz_kategorie():
    res = supabase.table("kategorie").select("*").order("nazwa").execute()
    return res.data

def pobierz_magazyn():
    # Pobieramy produkty i nazwę kategorii (JOIN)
    res = supabase.table("magazyn").select("id, nazwa, ilosc, kategorie(nazwa)").execute()
    return res.data

# --- PANEL BOCZNY: Kategorie ---
st.sidebar.header("⚙️ Zarządzanie Kategoriami")

nowa_kat = st.sidebar.text_input("Dodaj nową kategorię")
if st.sidebar.button("Dodaj"):
    if nowa_kat:
        supabase.table("kategorie").insert({"nazwa": nowa_kat}).execute()
        st.rerun()

st.sidebar.divider()

# Usuwanie kategorii
lista_kat = pobierz_kategorie()
if lista_kat:
    kat_do_usun = st.sidebar.selectbox("Usuń kategorię", [k['nazwa'] for k in lista_kat])
    if st.sidebar.button("Usuń kategorię"):
        supabase.table("kategorie").delete().eq("nazwa", kat_do_usun).execute()
        st.rerun()

# --- DODAWANIE TOWARU ---
st.subheader("➕ Dodaj nowy towar")
if lista_kat:
    c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
    kat_map = {k['nazwa']: k['id'] for k in lista_kat}

    with c1:
        nazwa_t = st.text_input("Nazwa produktu")
    with c2:
        wybrana_kat = st.selectbox("Kategoria", list(kat_map.keys()))
    with c3:
        ilosc_t = st.number_input("Ilość", min_value=1, value=1)
    with c4:
        st.write(" ")
        if st.button("Dodaj produkt"):
            if nazwa_t:
                supabase.table("magazyn").insert({
                    "nazwa": nazwa_t,
                    "kategoria_id": kat_map[wybrana_kat],
                    "ilosc": ilosc_t
                }).execute()
                st.rerun()
else:
    st.warning("Najpierw dodaj kategorię w panelu bocznym.")

st.divider()

# --- LISTA TOWARÓW ---
st.subheader("📋 Lista towarów")
dane = pobierz_magazyn()

if not dane:
    st.info("Magazyn jest pusty.")
else:
    for p in dane:
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        col1.write(f"**{p['nazwa']}**")
        
        # Obsługa złączonej nazwy kategorii
        nazwa_k = p['kategorie']['nazwa'] if p.get('kategorie') else "Brak"
        
        col2.write(f"📁 {nazwa_k}")
        col3.write(f"{p['ilosc']} szt.")
        if col4.button("Usuń", key=f"del_{p['id']}"):
            supabase.table("magazyn").delete().eq("id", p['id']).execute()
            st.rerun()

# --- RAPORT ---
st.divider()
if st.button("📊 Raport stanu"):
    if dane:
        raport = {}
        for p in dane:
            k = p['kategorie']['nazwa'] if p.get('kategorie') else "Nieznane"
            raport[k] = raport.get(k, 0) + p['ilosc']
        st.table([{"Kategoria": k, "Suma": v} for k, v in raport.items()])
