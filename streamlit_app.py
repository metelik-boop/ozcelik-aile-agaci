import streamlit as st
import pandas as pd

# 1. SAYFA VE BAŞLIK AYARLARI
st.set_page_config(page_title="Özçelik Ailesi Soy Ağacı", layout="centered")

# Özel Tasarım (Font ve Renkler)
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
    .expander-header {
        font-size: 1.2rem;
        font-weight: bold;
    }
    </style>
    <div class="ana-baslik">ÖZÇELİK AİLESİ</div>
    """, unsafe_allow_html=True)

# 2. VERİLERİ YÜKLEME (GÜNCELLEME GEREKİR)
# Sizin Google Sheets linkinizi buraya eklemeniz gerekecek.
# Şimdilik örnek veri yüklüyorum.
sheet_id = "1hGIDYimZfmCqZhJESg_C0QzY-MpiV9r6p6q4qczEjCo" # Burayı güncelleyin!
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(url)
except:
    st.error("Veri tabanına bağlanılamadı. Lütfen Google Sheets ID'nizi ve dosyanın 'Herkese Açık' olduğunu kontrol edin.")
    st.stop()

# 3. ANA EKRAN (KÖK AİLE - MAHMUT & FİRDEVS)
st.write("## ") # Boşluk
col1, col2 = st.columns(2)

# Kök Baba (ID 1)
root_baba = df[df['ID'] == 1].iloc[0]
with col1:
    st.markdown(f"""
    <div class="kisi-kart">
        <img src="https://via.placeholder.com/150" alt="{root_baba['isim']}" style="width:100%; border-radius:50%;">
        <h3>{root_baba['isim'].upper()} {root_baba['soy adı'].upper()}</h3>
        <p>Doğum: {root_baba['doğum tarihi'] if not pd.isna(root_baba['doğum tarihi']) else '-'} | Ölüm: -</p>
    </div>
    """, unsafe_allow_html=True)

# Kök Anne (Eşi)
root_anne = root_baba['eşinin adı']
with col2:
    st.markdown(f"""
    <div class="kisi-kart">
        <img src="https://via.placeholder.com/150" alt="{root_anne}" style="width:100%; border-radius:50%;">
        <h3>{root_anne.upper()} {root_baba['soy adı'].upper()}</h3>
        <p>Doğum: - | Ölüm: -</p>
    </div>
    """, unsafe_allow_html=True)

# 4. AĞAÇ YAPISINI KURMA (Tıklayınca Detay Açılan Yapı)
st.divider()
st.write("## ") 

# Mahmut & Firdevs'in Çocukları (1. Kuşak)
# Hem baba adı Mahmut hem anne adı Firdevs olanları süzüyoruz (Sıfır hata)
cocuklar_list = df[(df['baba adı'].str.lower() == root_baba['isim'].lower()) & 
                   (df['anne adı'].str.lower() == root_anne.lower())]

for index, cocuk in cocuklar_list.iterrows():
    
    # Her çocuk için tıklanabilir bir expander açıyoruz
    es_adi = cocuk['eşinin adı'] if not pd.isna(cocuk['eşinin adı']) else "Eşi Yok/Boşanmış"
    with st.expander(f"📍 {cocuk['isim'].upper()} & {es_adi.upper()} Ailesi"):
        
        c1, c2 = st.columns(2)
        
        # Çocuk Bilgileri (Hücre 1)
        with c1:
            st.markdown(f"""
            <div class="kisi-kart" style="border: 2px solid #ddd;">
                <img src="https://via.placeholder.com/100" alt="{cocuk['isim']}" style="border-radius:50%;">
                <p><strong>{cocuk['isim'].upper()} {cocuk['soy adı'].upper()}</strong></p>
                <p>Doğum: {cocuk['doğum tarihi'] if not pd.isna(cocuk['doğum tarihi']) else '-'}</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Eş Bilgileri (Hücre 2 - Varsa)
        with c2:
            if not pd.isna(cocuk['eşinin adı']):
                st.markdown(f"""
                <div class="kisi-kart" style="border: 2px solid #ddd;">
                    <img src="https://via.placeholder.com/100" alt="{cocuk['eşinin adı']}" style="border-radius:50%;">
                    <p><strong>{cocuk['eşinin adı'].upper()} (EŞİ)</strong></p>
                    <p>Doğum: -</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="kisi-kart" style="border: 1px dashed #aaa; color: #aaa;">
                    <p>(Eş Bilgisi Yok)</p>
                </div>
                """, unsafe_allow_html=True)

        # Torunları Listeleme (Bu ailenin çocukları)
        # Sadece bu kişinin (ID'sini veya ismini kullanarak) çocuklarını süzüyoruz.
        # İsim karışıklığını önlemek için hem anne hem baba adını kontrol ediyoruz.
        torunlar_list = df[(df['baba adı'].str.lower() == cocuk['isim'].lower()) & 
                          (df['anne adı'].str.lower() == es_adi.lower())]
        
        if not torunlar_list.empty:
            st.write("### ") # Boşluk
            st.write("**Torunlar/Çocuklar:**")
            
            # Torunları daha ufak kartlar halinde listeliyoruz
            for _, torun in torunlar_list.iterrows():
                st.markdown(f"""
                <div class="kisi-kart" style="text-align: left; padding: 5px 15px; border-radius: 5px; background-color: #f1f1f1;">
                    👤 <strong>{torun['isim'].upper()} {torun['soy adı'].upper()}</strong> 
                    <span style="color: #666; font-size: 0.9em;">
                        (Doğum: {torun['doğum tarihi'] if not pd.isna(torun['doğum tarihi']) else '-'})
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
                # Buraya bir kod daha ekleyip, torunların çocuklarını (3. kuşak) 
                # da tıklanabilir hale getirebiliriz (Sizin planınızdaki 5. ve 6. maddeler)
                
        else:
            st.write("_Bu kolun çocuk bilgisi bulunmamaktadır._")
