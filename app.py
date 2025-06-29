import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Konfigurasi halaman Streamlit
st.set_page_config(layout="wide", page_title="Analisis Data E-commerce")

# --- Judul Aplikasi ---
st.title('Dashboard Analisis UAS Data Science')
st.markdown("""
Ini adalah hasil analisis data dari beberapa dataset inventory.csv, order.csv, product.csv, dan users.csv. Analisis ini dibuat sebagai syarat tugas UAS mata kuliah Data Science
""")

# --- Caching Data yang Telah Diproses ---
@st.cache_data
def load_preprocessed_data():
    """
    Memuat data yang sudah bersih dari file Parquet.
    Proses ini sangat cepat.
    """
    base_path = 'processed_data/'
    df_inventory = pd.read_parquet(f'{base_path}inventory.parquet')
    df_users = pd.read_parquet(f'{base_path}users.parquet')
    df_order = pd.read_parquet(f'{base_path}order.parquet')
    df_product = pd.read_parquet(f'{base_path}product.parquet')
    df_gabungan_temp = pd.read_parquet(f'{base_path}gabungan_temp.parquet')
    
    return df_inventory, df_users, df_order, df_product, df_gabungan_temp

# Panggil fungsi untuk memuat data
try:
    df_inventory, df_users, df_order, df_product, df_gabungan_temp = load_preprocessed_data()
except FileNotFoundError:
    st.error(
        "File data yang telah diproses (format .parquet) tidak ditemukan. "
        "Pastikan Anda telah menjalankan skrip `preprocess.py` terlebih dahulu "
        "di terminal dengan perintah: `python preprocess.py`"
    )
    st.stop()


# --- Sidebar untuk Navigasi ---
st.sidebar.title('Navigasi')
page = st.sidebar.radio('Pilih Halaman:', 
                        ['Gambaran & Persiapan Data', 'Analisis Pertanyaan UAS', 'Trend/Poin yang menarik'])


# --- Konten Halaman ---

if page == 'Gambaran & Persiapan Data':
    st.header("1. Data `inventory` (setelah dibersihkan)")
    st.dataframe(df_inventory.head())
    st.subheader("Informasi Data")
    buffer = io.StringIO()
    df_inventory.info(buf=buffer)
    st.text(buffer.getvalue())
    
    st.header("2. Data `users` (setelah dibersihkan)")
    st.dataframe(df_users.head())
    st.subheader("Informasi Data")
    buffer = io.StringIO()
    df_users.info(buf=buffer)
    st.text(buffer.getvalue())

    st.header("3. Data `order` (setelah dibersihkan)")
    st.dataframe(df_order.head())
    st.subheader("Informasi Data")
    buffer = io.StringIO()
    df_order.info(buf=buffer)
    st.text(buffer.getvalue())

    st.header("4. Data `product` (setelah dibersihkan)")
    st.dataframe(df_product.head())
    st.subheader("Informasi Data")
    buffer = io.StringIO()
    df_product.info(buf=buffer)
    st.text(buffer.getvalue())


elif page == 'Analisis Pertanyaan UAS':
    st.header("Jawaban Pertanyaan UAS")

    # Soal 1
    st.subheader("1. Dari data pengguna, ada berapa banyak yang berasal dari Korea Selatan?")
    korea_users = df_users[df_users["country"] == "South Korea"]
    st.metric(label="Jumlah Pengguna dari Korea Selatan", value=len(korea_users))
    with st.expander("Lihat Data"):
        st.dataframe(korea_users)

    # Soal 2
    st.subheader("2. Berapa banyak pelanggan pria dan wanita dari Brandenburg, Jerman?")
    brandenburg_users = df_users[(df_users["state"] == "Brandenburg") & (df_users["country"] == "Germany")]
    gender_counts = brandenburg_users["gender"].value_counts()
    st.write("Jumlah pelanggan dari Brandenburg, Jerman berdasarkan gender:")
    st.dataframe(gender_counts)

    # Soal 3
    st.subheader("3. Berapa usia pelanggan termuda dan tertua? Dari negara mana kah mereka?")
    min_age = df_users["age"].min()
    max_age = df_users["age"].max()
    users_min_age = df_users[df_users["age"] == min_age]
    users_max_age = df_users[df_users["age"] == max_age]
    countries_min_age = users_min_age["country"].unique()
    countries_max_age = users_max_age["country"].unique()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Usia Pelanggan Termuda", value=f"{min_age} tahun")
        st.write("Negara Asal (Termuda):")
        st.write(countries_min_age)
    with col2:
        st.metric(label="Usia Pelanggan Tertua", value=f"{max_age} tahun")
        st.write("Negara Asal (Tertua):")
        st.write(countries_max_age)

    # Soal 4
    st.subheader("4. Sebutkan nama 5 pengguna yang terdaftar paling baru.")
    latest_users = df_users.sort_values(by="created_at", ascending=False).head(5)
    st.write("5 Pengguna Terbaru:")
    st.dataframe(latest_users[['first_name', 'last_name', 'created_at', 'country']])

    # Soal 5
    st.subheader("5. Ada berapa macam kategori produk yang dijual oleh Looker?")
    num_categories = len(df_product["category"].unique())
    st.metric(label="Jumlah Kategori Produk", value=num_categories)
    with st.expander("Lihat semua kategori"):
        st.write(df_product["category"].unique())
        
    # Soal 6
    st.subheader("6. Produk apa yang paling banyak terjual di 2020? Ada berapa transaksi penjualan produk tersebut?")
    # ----> PERBAIKAN DARI 'created_at_order' MENJADI 'created_at' <----
    transaksi_2020 = df_gabungan_temp[df_gabungan_temp["created_at"].dt.year == 2020]
    
    top_product_2020 = transaksi_2020["name"].value_counts().head(1)
    
    if not top_product_2020.empty:
        st.metric(label=f"Produk Terlaris 2020: {top_product_2020.index[0]}", value=f"{top_product_2020.values[0]} transaksi")
    else:
        st.metric(label="Produk Terlaris 2020:", value="Tidak ada data")
        
    with st.expander("Lihat 10 produk terlaris di 2020"):
        st.dataframe(transaksi_2020["name"].value_counts().head(10))

    # Soal 7
    st.subheader("7. Berapa banyak transaksi yang dibatalkan dari tahun 2019 ke tahun 2022? Bagaimana pendapatmu tentang informasi tersebut?")
    cancelled_transactions = df_order[df_order["status"].str.contains("Cancelled", case=False, na=False)]
    filtered_years_cancelled = cancelled_transactions[(cancelled_transactions["year"] >= 2019) & (cancelled_transactions["year"] <= 2022)]
    cancelled_by_year = filtered_years_cancelled["year"].value_counts().sort_index()
    st.write("Jumlah Transaksi yang Dibatalkan per Tahun:")
    st.dataframe(cancelled_by_year)
    
    st.info("""
    **Pendapat saya terkait informasi ini:**
    
    Terjadi peningkatan yang sangat dramatis pada jumlah transaksi yang dibatalkan pada tahun 2020 ke 2021. Hal itu dipengaruhi karena adanya pandemi covid-19 pada tahun tersebut. Faktor spesifik yang menyebabkan peningkatan transaksi yang dibatalkan antara lain:
    - Banyak pabrik yang tutup atau sedang melakukan pengurangan operasi karena lockdown dan mengikuti protokol kesehatan.
    - Pengiriman yang mengalami kemacetan di pelabuhan dan penundaan pengiriman, sehingga membuat barang yang sudah dikirim di-cancel.
    - Ketika pengiriman mengalami penundaan yang cukup lama, banyak pelanggan yang meng-cancel produk yang sudah dipesan.
    """)

    # Soal 8
    st.subheader("8. Tabel distribusi pelanggan berdasarkan sumber trafiknya (global dan per negara).")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Distribusi Global:")
        distribusi_global = df_users["traffic_source"].value_counts()
        st.dataframe(distribusi_global)
    with col2:
        st.write("Distribusi per Negara:")
        distribusi_per_negara = df_users.groupby("country")["traffic_source"].value_counts().unstack(fill_value=0)
        st.dataframe(distribusi_per_negara)


elif page == 'Trend/Poin yang menarik':
    st.header("Trend/Poin yang menarik Menarik dari Data")
    
    # Tren penjualan bulanan
    st.subheader("Tren Jumlah Transaksi Bulanan")
    st.write("""Grafik ini menunjukkan pertumbuhan jumlah transaksi yang sangat kuat dan konsisten dari awal tahun 2019 hingga kuartal pertama tahun 2022.
             """)
    df_order_viz = df_order.copy().set_index("created_at")
    monthly_sales = df_order_viz.resample("M").size()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_sales.plot(kind="line", marker="o", ax=ax)
    ax.set_title("Tren Jumlah Transaksi Bulanan", fontsize=16)
    ax.set_xlabel("Tanggal", fontsize=12)
    ax.set_ylabel("Jumlah Transaksi", fontsize=12)
    ax.grid(True)
    st.pyplot(fig)
    plt.clf()

    # Distribusi Usia dan Gender
    st.subheader("Distribusi Pelanggan Berdasarkan Usia dan Gender")
    st.write("""Target pasar e-commerce ini sangat luas dan seimbang, mencakup rentang usia dari remaja hingga lansia dengan distribusi gender yang hampir setara antara pria dan wanita.
              """)
    col1, col2 = st.columns(2)
    with col1:
        fig_age, ax_age = plt.subplots(figsize=(8, 6))
        sns.histplot(df_users["age"], bins=20, kde=True, palette="viridis", ax=ax_age)
        ax_age.set_title("Distribusi Usia Pelanggan")
        ax_age.set_xlabel("Usia")
        ax_age.set_ylabel("Jumlah Pelanggan")
        st.pyplot(fig_age)
        plt.clf()
    
    with col2:
        fig_gender, ax_gender = plt.subplots(figsize=(8, 6))
        gender_counts = df_users["gender"].value_counts()
        ax_gender.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%", startangle=90, colors=sns.color_palette("pastel"))
        ax_gender.set_title("Distribusi Gender Pelanggan")
        ax_gender.set_ylabel("")
        st.pyplot(fig_gender)
        plt.clf()
    
    # Kuantitas Pesanan Berdasarkan Status
    st.subheader("Jumlah Pesanan per Status")
    st.write("""Sebagian besar pesanan berada dalam status "Shipped" (Terkirim) dan "Complete" (Selesai), yang menandakan alur operasional yang relatif sehat. Namun, jumlah pesanan yang "Cancelled" (Dibatalkan) cukup signifikan dan memerlukan perhatian.
              """)
    status_counts = df_order['status'].value_counts()
    
    fig_status, ax_status = plt.subplots(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.barplot(x=status_counts.index, y=status_counts.values, ax=ax_status)
    ax_status.set_title('Jumlah Pesanan per Status', fontsize=16)
    ax_status.set_ylabel('Jumlah Pesanan', fontsize=12)
    ax_status.set_xlabel('Status', fontsize=12)
    plt.setp(ax_status.get_xticklabels(), rotation=45)
    st.pyplot(fig_status)
    plt.clf()
    
    # Distribusi Waktu Proses Pesanan
    st.subheader("Distribusi Waktu Proses Pesanan (dalam Jam)")
    st.write("""Proses "Waktu ke Pengiriman" lebih cepat dan lebih konsisten dibandingkan dengan "Waktu ke Penerimaan", yang memiliki variabilitas yang jauh lebih tinggi.
              """)
    # df_order sudah punya created_at, kita perlu tambahkan kolom waktu dari df_order yang belum di-reset indexnya
    df_order_temp = df_order.copy()
    df_order_temp['waktu_ke_pengiriman_jam'] = (df_order_temp['shipped_at'] - df_order_temp['created_at']).dt.total_seconds() / 3600
    df_order_temp['waktu_ke_penerimaan_jam'] = (df_order_temp['delivered_at'] - df_order_temp['shipped_at']).dt.total_seconds() / 3600
    waktu_proses_df = df_order_temp[['waktu_ke_pengiriman_jam', 'waktu_ke_penerimaan_jam']].copy()
    waktu_proses_df.rename(columns={
        'waktu_ke_pengiriman_jam': 'Waktu ke Pengiriman (Jam)',
        'waktu_ke_penerimaan_jam': 'Waktu ke Penerimaan (Jam)'
    }, inplace=True)
    
    waktu_proses_df_filtered = waktu_proses_df[(waktu_proses_df['Waktu ke Pengiriman (Jam)'] < 200) & (waktu_proses_df['Waktu ke Penerimaan (Jam)'] < 200)]
    fig_boxplot, ax_boxplot = plt.subplots(figsize=(10, 7))
    sns.boxplot(data=waktu_proses_df_filtered, palette='pastel', ax=ax_boxplot)
    ax_boxplot.set_title('Distribusi Waktu Proses Pesanan (dalam Jam)', fontsize=16)
    ax_boxplot.set_ylabel('Durasi (Jam)', fontsize=12)
    st.pyplot(fig_boxplot)
    plt.clf()