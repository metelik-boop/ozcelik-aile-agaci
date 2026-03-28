Python
import streamlit as st
import pandas as pd

# 1. SAYFA VE BAŞLIK AYARLARI
st.set_page_config(page_title="Özçelik Ailesi Soy Ağacı", layout="centered")

st.markdown("""
    <style>
    .ana-baslik {
        font-family: 'Times New Roman', serif;
        color: #4A2C2A;
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        border-bottom: 2px solid #4A2C2A;
    }
    .kisi-kart {
        text-align: center;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-bottom: 10px;
    }
    </style>
    <div class="ana-baslik">ÖZÇELİK AİLESİ</div>
    """, unsafe_allow_html=True)

# 2. VERİLERİ YÜKLEME
# Buraya sizin Google Sheets ID'nizi yapıştırdığınızdan emin olun!
sheet_id = "BURAYA_KENDI_ID_NIZI_YAPISTIRIN" 
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(url)
    # Sütun isimlerindeki boşlukları temizleyelim ki hata vermesin
    df.columns = [c.strip().lower() for c in df.columns]
except:
    st.error("Veri tabanına bağlanılamadı. Lütfen Google Sheets ID'nizi kontrol edin.")
    st.stop()

# 3. ANA EKRAN (KÖK AİLE - ID 1)
st.write("## ") 
col1, col2 = st.columns(2)

# Tablonuzdaki ID sütununa göre ilk kişiyi (Mahmut) buluyoruz
root_baba = df[df['id'] == 1].iloc[0]

with col1:
    st.markdown(f"""
    <div class="kisi-kart">
        <img src="https://via.placeholder.com/150" style="width:100%; border-radius:50%;">
        <h3>{root_baba['isim'].upper()} {root_baba['soyadı'].upper()}</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kisi-kart">
        <img src="https://via.placeholder.com/150" style="width:100%; border-radius:50%;">
        <h3>{root_baba['eşinin adı'].upper()} {root_baba['soyadı'].upper()}</h3>
    </div>
    """, unsafe_allow_html=True)

# 4. ÇOCUKLAR (TIKLAYINCA AÇILAN LİSTE)
st.divider()

# Mahmut'un çocuklarını bul (Baba adı Mahmut olanlar)
cocuklar = df[df['baba adı'].str.lower() == root_baba['isim'].lower()]

for index, cocuk in cocuklar.iterrows():
    es = cocuk['eşinin adı'] if not pd.isna(cocuk['eşinin adı']) else "Eşi Yok"
    with st.expander(f"📍 {cocuk['isim'].upper()} & {es.upper()} Ailesi"):
        # Bu kısma tıkladığınızda o çocuğun bilgilerini ve varsa kendi çocuklarını gösterecek
        st.write(f"**Doğum Tarihi:** {cocuk['doğum tarihi']}")
        
        # Torunları bul (Babası veya annesi bu çocuk olanlar)
        torunlar = df[(df['baba adı'].str.lower() == cocuk['isim'].lower()) | 
                      (df['anne adı'].str.lower() == cocuk['isim'].lower())]
        
        if not torunlar.empty:
            st.write("---")
            st.write("**Çocukları:**")
            for _, torun in torunlar.iterrows():
                st.write(f"👤 {torun['isim'].upper()} ({torun['doğum tarihi']})")
