import csv
import os
import datetime
import pandas as pd

CSV_BARANG = 'barang.csv'
CSV_PENGGUNA = 'pengguna.csv'
CSV_TRANSAKSI = 'transaksi.csv'

keranjang = []  #menyimpan item sementara
user_login_name = None  # Variabel untuk username user yang login

def init_user_file():
    if not os.path.exists(CSV_PENGGUNA):
        with open(CSV_PENGGUNA, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['nama', 'password', 'role'])
            writer.writerow(['petani', '24240', 'admin'])

def init_transaksi_file():
    if not os.path.exists(CSV_TRANSAKSI):
        with open(CSV_TRANSAKSI, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'tanggal', 'pelanggan', 'jumlah'])

def init_barang_file():
    if not os.path.exists(CSV_BARANG):
        with open(CSV_BARANG, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'nama', 'stok', 'harga', 'kategori', 'masa_habis'])
            writer.writerow(['1', 'Pestisida Organik Plus', '10', '50000', 'Obat Pertanian', '10'])
            writer.writerow(['2', 'Fungisida Cair Max', '12', '45000', 'Obat Pertanian', '15'])
            writer.writerow(['3', 'Insektisida Serbuk Hijau', '8', '55000', 'Obat Pertanian', '20'])
            writer.writerow(['4', 'Vitamin Daun Super', '20', '30000', 'Obat Pertanian', '20'])
            writer.writerow(['5', 'ZPT Auksin Murni', '15', '60000', 'Obat Pertanian', '26'])
            writer.writerow(['6', 'Herbisida Kontak Cepat', '10', '48000', 'Obat Pertanian', '2'])
            writer.writerow(['7', 'Pupuk Hayati Cair', '14', '35000', 'Obat Pertanian', '24'])
            writer.writerow(['8', 'Bakterisida Klorin-X', '11', '52000', 'Obat Pertanian', '22'])
            writer.writerow(['9', 'Pestisida Biologis Aman', '9', '40000', 'Obat Pertanian', '18'])
            writer.writerow(['10', 'Fungisida Sistemik Gold', '13', '47000', 'Obat Pertanian', '10'])

def lanjutkan_atau_keluar():
    while True:
        pilihan = input("Apakah Anda ingin mencoba lagi? (ya/tidak): ").strip().lower()
        if pilihan == 'tidak':
            return False
        elif pilihan == 'ya':
            return True
        print("Pilihan tidak valid!")
        

def registrasi():
    print("=== Registrasi Pengguna Baru ===")
    while True:
        nama = input('Masukkan nama anda: ').strip().lower()
        password = input('Masukkan PIN (5 digit): ')

        if len(password) != 5 or not password.isdigit():
            print('PIN harus terdiri dari 5 digit angka.')
            if not lanjutkan_atau_keluar():
                return
            continue
        if not nama:  # Cek kosong
            print("Nama tidak boleh kosong!")
            if not lanjutkan_atau_keluar():
                break
            continue
        if not nama.isalpha(): 
            print("Nama harus berupa huruf tanpa angka/spasi!")
            if not lanjutkan_atau_keluar():
                break
            continue

        with open(CSV_PENGGUNA, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == nama:
                    print("Nama sudah digunakan. Buat nama lain.")
                    if not lanjutkan_atau_keluar():
                        return
                    break
            else:
                with open(CSV_PENGGUNA, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([nama, password, 'user'])
                print("Berhasil membuat akun baru.")
                return

def user_login():
    global user_login_name
    print("=== Login Pengguna ===")
    while True:
        nama = input('Masukkan nama anda: ').strip().lower()
        password = input('Masukkan PIN: ')

        with open(CSV_PENGGUNA, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == nama and row[1] == password and row[2] == 'user':
                    print(f"Login berhasil! Selamat datang, {nama}.")
                    user_login_name = nama  
                    menu_pengguna()
                    return
        print("Nama atau PIN salah.")
        if not lanjutkan_atau_keluar():
            return

def admin_login():
    print("=== Login Admin ===")
    while True:
        nama = input('Masukkan nama admin: ').strip().lower()
        password = input('Masukkan PIN: ')

        with open(CSV_PENGGUNA, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == nama and row[1] == password and row[2] == 'admin':
                    print("Login admin berhasil!")
                    menu_admin()
                    return
        print("Nama atau PIN salah.")
        if not lanjutkan_atau_keluar():
            return

def load_barang():
    try:
        with open(CSV_BARANG, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return [dict(row) for row in reader if row['kategori'] == 'Obat Pertanian']
    except FileNotFoundError:
        return []

def simpan_barang(barang_list):
    with open(CSV_BARANG, mode='w', newline='') as file:
        fieldnames = ['id', 'nama', 'stok', 'harga', 'kategori', 'masa_habis']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(barang_list)

def bubble_sort_id(barang_list):
    n = len(barang_list)
    for i in range(n):
        for j in range(n - i - 1):
            if int(barang_list[j]['id']) > int(barang_list[j + 1]['id']):
                barang_list[j], barang_list[j + 1] = barang_list[j + 1], barang_list[j]
    return barang_list

def cari_barang_by_id(barang_list, id_barang):
    for barang in barang_list:
        if barang['id'] == id_barang:
            return barang
    return None

def tampilkan_barang(barang_list):
    print("\n== Daftar Obat Pertanian ==")
    print("{:<5} {:<25} {:<10} {:<10} {:<15} {:<15}".format("ID", "Nama", "Stok", "Harga", "Kategori", "masa_habis"))
    print("-" * 90)
    for b in barang_list:
        print("{:<5} {:<25} {:<10} {:<10} {:<15} {:<15}".format(
            b['id'], b['nama'], b['stok'], b['harga'], b.get('kategori', '-'), b.get('masa_habis', '-')
        ))

def proses_pembayaran_knapsack(selected_items, total_bayar):
    """Proses pembayaran dan simpan transaksi"""
    print("\n== Proses Pembayaran ==")
    print("Daftar Obat:")
    for obat in selected_items:
        print(f"- {obat['nama']}: Rp{obat['harga']}")
    
    print(f"\nTotal Pembayaran: Rp{total_bayar}")
    
    while True:
        bayar = input("Masukkan nominal pembayaran: Rp")
        if bayar.isdigit():
            bayar = int(bayar)
            if bayar >= total_bayar:
                print(f"Pembayaran berhasil! Kembalian: Rp{bayar - total_bayar}")
                simpan_transaksi(len(selected_items), total_bayar)
                break
            else:
                print(f"Uang kurang! Kurang Rp{total_bayar - bayar}")
        else:
            print("Input harus angka!")

def rekomendasi_obat(barang_list, anggaran):
    if not barang_list:
        print("Tidak ada data obat pertanian.")
        return

    barang_list_valid = [b for b in barang_list if 'masa_habis' in b and 'harga' in b]
    if not barang_list_valid:
        print("Data tidak valid: pastikan ada 'masa_habis' dan 'harga'!")
        return

    barang_sorted = sorted(
        barang_list_valid,
        key=lambda b: int(b['masa_habis']),
        reverse=True
    )

    selected_items = []
    total_bayar = 0
    for obat in barang_sorted:
        harga_obat = int(obat['harga'])
        if total_bayar + harga_obat <= anggaran:
            selected_items.append(obat)
            total_bayar += harga_obat

    print("\n== Rekomendasi Obat ==")
    for idx, obat in enumerate(selected_items, 1):
        print(f"{idx}. {obat['nama']} (Masa: {obat['masa_habis']} hari, Harga: Rp{obat['harga']})")
    print(f"\nTotal Harga: Rp{total_bayar} (Dari anggaran Rp{anggaran})")

    checkout = input("\nLanjutkan checkout? (y/n): ").lower()
    if checkout == 'y':
        proses_pembayaran_knapsack(selected_items, total_bayar)

def edit_stok():
    barang_list = load_barang()
    id_barang = input("Masukkan ID barang: ")
    barang = cari_barang_by_id(barang_list, id_barang)
    if barang:
        print(f"Stok lama: {barang['stok']}")
        stok_baru = input("Masukkan stok baru: ")
        while not stok_baru.isdigit():  
            print("Stok harus berupa angka!")
            stok_baru = input("Stok: ")
        stok_baru = int(stok_baru)
        barang['stok'] = stok_baru
        simpan_barang(barang_list)
        print("Stok berhasil diperbarui.")
    else:
        print("Barang tidak ditemukan.")

def tambah_barang():
    barang_list = load_barang()
    id_baru = str(int(barang_list[-1]['id']) + 1 if barang_list else 1)
    nama = input("Nama barang: ")
    stok = input("Stok: ")
    while not stok.isdigit():  
        print("Stok harus berupa angka!")
        stok = input("Stok: ")
    stok = int(stok)
    harga = input("Harga: ")
    while not harga.isdigit():  
        print("Harga harus berupa angka!")
        harga = input("Harga: ")
    harga = int(harga)
    kategori = "Obat Pertanian"
    masa_habis = input("Masa habis obat: ")
    barang_list.append({
        'id': id_baru, 'nama': nama, 'stok': stok, 'harga': harga, 'kategori': kategori, 'masa_habis': masa_habis
    })
    simpan_barang(barang_list)
    print("Barang berhasil ditambahkan.")

def hapus_barang():
    barang_list = load_barang()
    id_barang = input("Masukkan ID barang yang akan dihapus: ")
    barang = cari_barang_by_id(barang_list, id_barang)
    if barang:
        barang_list.remove(barang)
        simpan_barang(barang_list)
        print("Barang berhasil dihapus.")
    else:
        print("Barang tidak ditemukan.")

def tambah_keranjang():
    barang_list = load_barang()
    tampilkan_barang(barang_list)
    id_barang = input("Masukkan ID barang yang ingin dibeli: ")
    barang = cari_barang_by_id(barang_list, id_barang)
    if not barang:
        print("Barang tidak ditemukan.")
        return

    jumlah = input("Masukkan jumlah pembelian: ")
    if not jumlah.isdigit() or int(jumlah) <= 0 or jumlah == "":
        print("Jumlah tidak valid.")
        return
    jumlah = int(jumlah)
    stok = int(barang['stok'])

    if jumlah > stok:
        print("Stok tidak cukup.")
        return

    for item in keranjang:
        if item['id'] == id_barang:
            item['jumlah'] += jumlah
            print(f"Jumlah {barang['nama']} di keranjang ditambah menjadi {item['jumlah']}.")
            return

    keranjang.append({
        'id': id_barang,
        'nama': barang['nama'],
        'harga': int(barang['harga']),
        'jumlah': jumlah
    })
    print(f"{jumlah} {barang['nama']} berhasil ditambahkan ke keranjang.")

def tampilkan_keranjang():
    if not keranjang:
        print("Keranjang Anda kosong.")
        return

    print("\n== Keranjang Anda ==")
    print("{:<5} {:<25} {:<10} {:<10}".format("ID", "Nama", "Jumlah", "Harga"))
    total_harga = 0
    for item in keranjang:
        subtotal = item['harga'] * item['jumlah']
        total_harga += subtotal
        print("{:<5} {:<25} {:<10} Rp{:<10}".format(item['id'], item['nama'], item['jumlah'], subtotal))
    print(f"Total Harga: Rp{total_harga}")
    while True:
        pilihan = input("Apakah Anda ingin checkout? (ya/tidak): ").strip().lower()
        if pilihan == 'ya':
            checkout(user_login_name)
            break
        elif pilihan == 'tidak':
            break
        else:
            print("Masukkan 'ya' atau 'tidak'.")

def checkout(username):
    global keranjang
    if not keranjang:
        print("Keranjang kosong, tidak dapat melakukan checkout.")
        return

    barang_list = load_barang()
    total_bayar = 0

    for item in keranjang:
        barang = cari_barang_by_id(barang_list, item['id'])
        if not barang:
            print(f"Barang {item['nama']} tidak ditemukan, batal checkout.")
            return
        stok_barang = int(barang['stok'])
        if item['jumlah'] > stok_barang:
            print(f"Stok untuk {item['nama']} tidak cukup, batal checkout.")
            return
        total_bayar += item['jumlah'] * int(barang['harga'])

    print(f"Total yang harus dibayar: Rp{total_bayar}")

    while True:
        bayar = input("Masukkan jumlah pembayaran: Rp")
        if not bayar.isdigit():
            print("Masukkan angka yang valid.")
            continue
        bayar = int(bayar)
        if bayar < total_bayar:
            print("Pembayaran kurang.")
        else:
            kembalian = bayar - total_bayar
            print(f"Pembayaran diterima. Kembalian: Rp{kembalian}")

            for item in keranjang:
                barang = cari_barang_by_id(barang_list, item['id'])
                barang['stok'] = str(int(barang['stok']) - item['jumlah'])
            simpan_barang(barang_list)

            simpan_transaksi(username, len(keranjang), total_bayar)

            keranjang = []
            break

def simpan_transaksi(username, jumlah_item, total_bayar):
    init_transaksi_file()
    transaksi_id = 1
    with open(CSV_TRANSAKSI, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)
        if rows:
            last_id = int(rows[-1][0])
            transaksi_id = last_id + 1

    tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_TRANSAKSI, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([transaksi_id, tanggal, username, total_bayar])
    print("Transaksi berhasil disimpan.")

def riwayat_transaksi():
    init_transaksi_file()
    if not user_login_name:
        print("Anda belum login.")
        return

    with open(CSV_TRANSAKSI, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        transaksi_user = [row for row in reader if row[2] == user_login_name]

    if not transaksi_user:
        print("Belum ada riwayat transaksi.")
        return

    print(f"\n== Riwayat Transaksi untuk {user_login_name} ==")
    print("{:<5} {:<20} {:<10}".format("ID", "Tanggal", "Total Bayar"))
    for tr in transaksi_user:
        print("{:<5} {:<20} Rp{:<10}".format(tr[0], tr[1], tr[3]))

def menu_pengguna():
    while True:
        print("\n=== Menu Pengguna ===")
        print("1. Tampilkan Barang")
        print("2. Belanja")
        print("3. Tampilkan Keranjang")
        print("4. Rekomendasi Obat")
        print("5. Riwayat Transaksi")
        print("6. Logout")
        pilihan = input("Pilih menu: ")

        barang_list = load_barang()

        if pilihan == '1':
            tampilkan_barang(barang_list)
        elif pilihan == '2':
            tambah_keranjang()
        elif pilihan == '3':
            tampilkan_keranjang()
        elif pilihan == '4':
            anggaran = int(input(f'Masukkan anggaran anda:'))
            rekomendasi_obat(barang_list, anggaran)
        elif pilihan == '5':
            riwayat_transaksi()
        elif pilihan == '6':
            print("Logout berhasil.")
            break
        else:
            print("Pilihan salah.")

def menu_admin():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Tampilkan Barang")
        print("2. Tambah Barang")
        print("3. Edit Stok")
        print("4. Hapus Barang")
        print("5. Logout")
        pilihan = input("Pilih menu: ")

        barang_list = load_barang()

        if pilihan == '1':
            tampilkan_barang(barang_list)
        elif pilihan == '2':
            tambah_barang()
        elif pilihan == '3':
            edit_stok()
        elif pilihan == '4':
            hapus_barang()
        elif pilihan == '5':
            print("Logout berhasil.")
            break
        else:
            print("Pilihan salah.")

def menu_utama():
    init_user_file()
    init_barang_file()
    init_transaksi_file()
    while True:
        print("\n=== Selamat Datang di Toko Obat Pertanian ===")
        print("1. Login Admin")
        print("2. Login User")
        print("3. Registrasi User")
        print("4. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            admin_login()
        elif pilihan == '2':
            user_login()
        elif pilihan == '3':
            registrasi()
        elif pilihan == '4':
            print("Terima kasih, sampai jumpa!")
            break
        else:
            print("Pilihan salah.")

menu_utama()
