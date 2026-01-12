import streamlit as st
from supabase import create_client, Client

# --- 1. POŁĄCZENIE I DIAGNOSTYKA ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Problem z kluczami Secrets: {e}")
        return None

supabase = init_connection()

st.title("📦 Magazyn v3 (Stabilny)")

if supabase:
    # --- 2. FUNKCJE POBIERANIA DANYCH ---
    def get_categories():
        res = supabase.table("kategorie").select("*").execute()
        return res.data if res.data else []

    def get_products():
        # Pobieramy wszystko z tabeli magazyn i dołączamy nazwę z tabeli kategorie
        res = supabase.table("magazyn").select("id, nazwa, ilosc, kategorie(nazwa)").execute()
        return res.data if res.data else []

    # --- 3. PANEL BOCZNY (Dodawanie) ---
    st.sidebar.header("Zarządzanie")
    
    # Dodawanie kategorii
    with st.sidebar.expander("Dodaj nową kategorię"):
        n_kat = st.text_input("Nazwa kategorii")
        if st.button("Zapisz kategorię"):
            if n_kat:
                supabase.table("kategorie").insert({"nazwa": n_kat}).execute()
                st.rerun()

    st.sidebar.divider()

    # Dodawanie produktu
    st.sidebar.subheader("Dodaj produkt")
    kategorie = get_categories()
    
    if kategorie:
        kat_map = {k['nazwa']: k['id'] for k in kategorie}
        p_nazwa = st.sidebar.text_input("Nazwa towaru")
        p_kat = st.sidebar.selectbox("Kategoria", list(kat_map.keys()))
        p_ilosc = st.sidebar.number_input("Ilość", min_value=1, value=1)
        
        if st.sidebar.button("Dodaj do bazy"):
            if p_nazwa:
                supabase.table("magazyn").insert({
                    "nazwa": p_nazwa,
                    "kategoria_id": kat_map[p_kat],
                    "ilosc": p_ilosc
                }).execute()
                st.rerun()
    else:
        st.sidebar.info("Dodaj najpierw kategorię.")

    # --- 4. WYŚWIETLANIE LISTY ---
    st.subheader("Lista towarów")
    produkty = get_products()

    if not produkty:
        st.info("Brak towarów w bazie.")
    else:
        for p in produkty:
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            # Bezpieczne wyciąganie nazwy kategorii (obsługa różnych wersji zwracanych danych)
            kat_data = p.get('kategorie')
            if isinstance(kat_data, list) and len(kat_data) > 0:
                nazwa_k = kat_data[0].get('nazwa', 'Brak')
            elif isinstance(kat_data, dict):
                nazwa_k = kat_data.get('nazwa', 'Brak')
            else:
                nazwa_k = "Ogólne"

            col1.write(f"**{p['nazwa']}**")
            col2.write(f"📁 {nazwa_k}")
            col3.write(f"{p['ilosc']} szt.")
            
            if col4.button("🗑️", key=f"del_{p['id']}"):
                supabase.table("magazyn").delete().eq("id", p['id']).execute()
                st.rerun()

    # --- 5. RAPORT ---
    if st.button("📊 Generuj raport"):
        st.divider()
        if produkty:
            total = sum(p['ilosc'] for p in produkty)
            st.metric("Suma wszystkich towarów", f"{total} szt.")
            # Wyświetlenie surowych danych dla debugowania (opcjonalnie)
            # st.write(produkty) 
        else:
            st.warning("Brak danych.")

# --- 6. LISTA KONTROLNA (Co sprawdzić, jeśli nadal nie działa) ---
else:
    st.warning("Aplikacja nie mogła połączyć się z bazą.")
