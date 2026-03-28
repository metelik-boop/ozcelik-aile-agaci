import streamlit as st
import pandas as pd

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Özçelik Ailesi Soy Ağacı", layout="centered")

st.markdown("""
    <style>
    .ana-baslik {
        font-family: 'Times New Roman', serif;
        color: #4A2C2A;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        border-bottom: 2px solid #4A2C2A;
        margin-bottom: 20px;
    }
    .kisi-kart {
        text-align: center;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    <div class="ana-baslik">ÖZÇELİK AİLESİ</div>
    """, unsafe_allow_html=True)

# 2. VERİ YÜKLEME
sheet_id = "1hGIDYimZfmCqZhJESg_C0QzY-MpiV9r6p6q4qczEjCo"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(url)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.fillna("")
except Exception as e:
    st.error("Veri tabanı hatası.")
    st.stop()

# 3. KÖK AİLE (MAHMUT & FİRDEVS)
root = df[df['id'] == 1].iloc[0]

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="kisi-kart"><h3>{root["isim"].upper()}</h3><p>BABA</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kisi-kart"><h3>{root["eşinin adı"].upper()}</h3><p>ANNE</p></div>', unsafe_allow_html=True)

st.divider()

# 4. 1. KUŞAK (MAHMUT & FİRDEVS ÇOCUKLARI)
kuşak_1 = df[(df['baba adı'].str.lower() == root['isim'].lower()) & 
             (df['anne adı'].str.lower() == root['eşinin adı'].lower())]

for _, cocuk in kuşak_1.iterrows():
    es_adi = cocuk['eşinin adı'] if cocuk['eşinin adı'] != "" else ""
    
    with st.expander(f"📍 {cocuk['isim'].upper()} & {es_adi.upper()} Ailesi"):
        st.write(f"📅 **Doğum:** {cocuk['doğum tarihi']}")
        
        # 5. 2. KUŞAK (Kız veya Erkek ayrımı yapmadan çocuklarını bulma)
        # ÖNEMLİ: Burada hem "Babası bu kişi olanlar" VEYA "Annesi bu kişi olanlar" diye arıyoruz.
        torunlar = df[(df['baba adı'].str.lower() == cocuk['isim'].lower()) | 
                      (df['anne adı'].str.lower() == cocuk['isim'].lower())]
        
        if not torunlar.empty:
            st.write("---")
            st.write("**Çocukları:**")
            for _, torun in torunlar.iterrows():
                # Torun bilgisi
                st.info(f"👤 {torun['isim'].upper()} {torun['soyadı'].upper()} ({torun['doğum tarihi']})")
                
                # 6. 3. KUŞAK (Torunların Çocukları)
                torun_cocuklar = df[(df['baba adı'].str.lower() == torun['isim'].lower()) | 
                                    (df['anne adı'].str.lower() == torun['isim'].lower())]
                
                if not torun_cocuklar.empty:
                    for _, t_cocuk in torun_cocuklar.iterrows():
                        st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;↳ 👶 {t_cocuk['isim'].upper()} {t_cocuk['soyadı'].upper()} ({t_cocuk['doğum tarihi']})")
        else:
            st.write("_Bu kol için çocuk kaydı bulunamadı._")
