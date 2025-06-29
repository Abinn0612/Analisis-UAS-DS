import pandas as pd
import os

print("Memulai proses pre-processing data...")

# Buat direktori untuk menyimpan data yang sudah diproses
output_dir = 'processed_data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Direktori '{output_dir}' dibuat.")

# Fungsi untuk memuat dan membersihkan data
def preprocess_all_data():
    # 1. Memuat dan membersihkan inventory.csv
    print("Memproses inventory.csv...")
    df_inventory = pd.read_csv("inventory.csv")
    df_inventory["created_at"] = pd.to_datetime(df_inventory["created_at"], format="mixed", utc=True, errors="coerce")
    df_inventory["sold_at"] = pd.to_datetime(df_inventory["sold_at"], format="mixed", utc=True, errors="coerce")
    df_inventory["product_name"].fillna("Tidak Diketahui", inplace=True)
    df_inventory["product_brand"].fillna("Tidak Diketahui", inplace=True)
    df_inventory.to_parquet(f'{output_dir}/inventory.parquet')
    print("inventory.parquet berhasil disimpan.")

    # 2. Memuat dan membersihkan users.csv
    print("Memproses users.csv...")
    df_users = pd.read_csv("users.csv")
    df_users["city"] = df_users["city"].fillna("Tidak Diketahui")
    df_users["created_at"] = pd.to_datetime(df_users["created_at"], format="mixed", utc=True, errors="coerce")
    df_users.to_parquet(f'{output_dir}/users.parquet')
    print("users.parquet berhasil disimpan.")
    
    # 3. Memuat dan membersihkan order.csv
    print("Memproses order.csv...")
    df_order = pd.read_csv("order.csv")
    df_order["created_at"] = pd.to_datetime(df_order["created_at"], format="mixed", utc=True, errors="coerce")
    df_order["shipped_at"] = pd.to_datetime(df_order["shipped_at"], format="mixed", utc=True, errors="coerce")
    df_order["delivered_at"] = pd.to_datetime(df_order["delivered_at"], format="mixed", utc=True, errors="coerce")
    df_order["returned_at"] = pd.to_datetime(df_order["returned_at"], format="mixed", utc=True, errors="coerce")
    df_order["year"] = df_order["created_at"].dt.year
    df_order.to_parquet(f'{output_dir}/order.parquet')
    print("order.parquet berhasil disimpan.")
    
    # 4. Memuat dan membersihkan product.csv
    print("Memproses product.csv...")
    df_product = pd.read_csv("product.csv")
    df_product["name"] = df_product["name"].fillna("Tidak Diketahui")
    df_product["brand"] = df_product["brand"].fillna("Tidak Diketahui")
    df_product.to_parquet(f'{output_dir}/product.parquet')
    print("product.parquet berhasil disimpan.")
    
    # 5. Membuat dan menyimpan data gabungan untuk analisis Q6
    print("Membuat data gabungan...")
    df_gabungan_temp = pd.merge(df_order, df_product, left_on="product_id", right_on="id", how="left", suffixes=("_order", "_product"))
    df_gabungan_temp.to_parquet(f'{output_dir}/gabungan_temp.parquet')
    print("gabungan_temp.parquet berhasil disimpan.")
    
    print("\nPre-processing selesai. Semua file Parquet telah dibuat di folder 'processed_data'.")

if __name__ == '__main__':
    preprocess_all_data()