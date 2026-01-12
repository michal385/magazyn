import streamlit as st
from supabase import create_client, Client

# --- KONFIGURACJA POŁĄCZENIA ---
# Dane pobierane są bezpiecznie ze Streamlit Secrets
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(URL, KEY)

st.title("📦 Magazyn z bazą Supabase")

# --- FUNKCJE POMOCNICZE (Operacje na bazie) ---

def pobierz_kategorie():
    """Pobiera listę kategorii z tabeli 'kategorie'"""
    res = supabase.table("kategorie").select("*").execute()
    return res.data

def pobierz_produkty():
    """Pobiera produkty wraz z nazwami ich kategorii (JOIN)"""
    res = supabase.table("magazyn").select("id, nazwa, ilosc, kategorie(nazwa)").execute()
    return res.data

# --- PANEL BOCZNY: Kategorie ---
st.sidebar.header("Ustawienia Kategorii")
nowa_kat = st.sidebar.text_input("Nazwa nowej kategorii")
if st.sidebar.button("Dodaj kategorię"):
    if nowa_kat:
        try:
            supabase.table("kategorie").insert({"nazwa": nowa_kat}).execute()
            st.sidebar.success(f"Dodano kategorię: {nowa_kat}")
            st.rerun()
        except Exception as e:
            st.sidebar.error("Błąd: Kategoria może już istnieć.")

st.sidebar.divider()

# --- PANEL BOCZNY: Dodawanie towaru ---
st.sidebar.header("Dodaj towar")
kategorie_z_bazy = pobierz_kategorie()
# Tworzymy słownik {nazwa: id}, aby łatwo zapisywać relację w bazie
opcje_kat = {k['nazwa']: k['id'] for k in kategorie_z_bazy}

nazwa_towaru = st.sidebar.text_input("Nazwa towaru")
wybrana_kat = st.sidebar.selectbox("Wybierz kategorię", list(opcje_kat.keys()))
ilosc_towaru = st.sidebar.number_input("Ilość", min_value=1, value=1)

if st.sidebar.button("Dodaj do magazynu"):
    if nazwa_towaru:
        supabase.table("magazyn").insert({
            "nazwa": nazwa_towaru,
            "kategoria_id": opcje_kat[wybrana_kat],
            "ilosc": ilosc_towaru
        }).execute()
        st.success(f"Dodano: {nazwa_towaru}")
        st.rerun()
    else:
        st.error("Wpisz nazwę towaru!")

# --- GŁÓWNA SEKCJA: Lista produktów ---
st.subheader("Aktualny stan magazynu")
produkty = pobierz_produkty()

if not produkty:
    st.info("Magazyn jest pusty.")
else:
    for p in produkty:
        cols = st.columns([3, 2, 1, 1])
        cols[0].write(f"**{p['nazwa']}**")
        # Dostęp do nazwy kategorii przez relację (kategorie.nazwa)
        nazwa_k = p.get('kategorie', {}).get('nazwa', 'Brak')
        cols[1].write(f"📁 {nazwa_k}")
        cols[2].write(f"szt: {p['ilosc']}")
        
        if cols[3].button("Usuń", key=f"del_{p['id']}"):
            supabase.table("magazyn").delete().eq("id", p['id']).execute()
            st.rerun()

# --- RAPORT ---
st.divider()
st.subheader("📊 Raport")
if st.button("Generuj raport stanu"):
    if produkty:
        st.write("**Podsumowanie:**")
        # Proste sumowanie ilości dla raportu
        suma_sztuk = sum(item['ilosc'] for item in produkty)
        st.write(f"Łączna ilość wszystkich towarów: **{suma_sztuk}**")
        
        # Wyświetlenie podziału na kategorie
        raport_kat = {}
        for p in produkty:
            n_kat = p.get('kategorie', {}).get('nazwa', 'Brak')
            raport_kat[n_kat] = raport_kat.get(n_kat, 0) + p['ilosc']
        
        st.table(raport_kat)
    else:
        st.warning("Brak danych do raportu.")
