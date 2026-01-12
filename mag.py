import streamlit as st
from supabase import create_client, Client

# --- POŁĄCZENIE ---
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except Exception as e:
    st.error("Błąd konfiguracji Secrets! Sprawdź, czy dodałeś SUPABASE_URL i SUPABASE_KEY.")
    st.stop()

st.title("📦 Magazyn z bazą Supabase")

# --- FUNKCJE ---

def pobierz_kategorie():
    # Pobieramy kategorie posortowane alfabetycznie
    res = supabase.table("kategorie").select("*").order("nazwa").execute()
    return res.data

def pobierz_produkty():
    # Kluczowe: pobieramy produkt i nazwę kategorii przez JOIN
    # Upewnij się, że w tabeli 'magazyn' kolumna to 'kategoria_id'
    res = supabase.table("magazyn").select("id, nazwa, ilosc, kategorie(nazwa)").execute()
    return res.data

# --- PANEL BOCZNY ---
st.sidebar.header("Ustawienia")

# Dodawanie Kategorii
nowa_kat = st.sidebar.text_input("Nowa kategoria")
if st.sidebar.button("Dodaj kategorię"):
    if nowa_kat:
        supabase.table("kategorie").insert({"nazwa": nowa_kat}).execute()
        st.rerun()

st.sidebar.divider()

# Dodawanie Towaru
st.sidebar.header("Dodaj towar")
lista_kat = pobierz_kategorie()

if not lista_kat:
    st.sidebar.warning("Najpierw dodaj przynajmniej jedną kategorię!")
else:
    opcje_kat = {k['nazwa']: k['id'] for k in lista_kat}
    nazwa_t = st.sidebar.text_input("Nazwa towaru")
    wybrana_kat_nazwa = st.sidebar.selectbox("Kategoria", list(opcje_kat.keys()))
    ilosc_t = st.sidebar.number_input("Ilość", min_value=1, value=1)

    if st.sidebar.button("Dodaj do magazynu"):
        if nazwa_t:
            supabase.table("magazyn").insert({
                "nazwa": nazwa_t,
                "kategoria_id": opcje_kat[wybrana_kat_nazwa],
                "ilosc": ilosc_t
            }).execute()
            st.rerun()

# --- WIDOK GŁÓWNY ---
st.subheader("Stan magazynu")
dane = pobierz_produkty()

if not dane:
    st.info("Magazyn jest pusty.")
else:
    for p in dane:
        c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
        c1.write(f"**{p['nazwa']}**")
        
        # Obsługa pobierania nazwy z relacji (Supabase zwraca to jako słownik)
        nazwa_kategorii = p.get('kategorie', {}).get('nazwa', 'Brak') if p.get('kategorie') else "Brak"
        
        c2.write(f"📁 {nazwa_kategorii}")
        c3.write(f"{p['ilosc']} szt.")
        
        if c4.button("Usuń", key=f"btn_{p['id']}"):
            supabase.table("magazyn").delete().eq("id", p['id']).execute()
            st.rerun()

# --- RAPORT ---
st.divider()
if st.button("Generuj raport"):
    if dane:
        raport = {}
        for p in dane:
            kat = p.get('kategorie', {}).get('nazwa', 'Nieznana') if p.get('kategorie') else "Nieznana"
            raport[kat] = raport.get(kat, 0) + p['ilosc']
        
        st.table(list(raport.items()))
        st.success(f"Suma wszystkich produktów: {sum(raport.values())}")
