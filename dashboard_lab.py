import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# KONFIGURASI DATABASE (BACKEND)
DB_FILE = 'laboratorium.db'

def init_db():
    """Fungsi ini membuat tabel dan isi data awal jika database belum ada"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Tabel Anggota
    c.execute('''CREATE TABLE IF NOT EXISTS Anggota (
        id_anggota INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_anggota TEXT,
        status_anggota TEXT DEFAULT 'Aktif'
    )''')
    
    # Tabel Alat
    c.execute('''CREATE TABLE IF NOT EXISTS Alat (
        id_alat INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_alat TEXT,
        jenis TEXT,
        harga_satuan INTEGER
    )''')

    # Tabel Stok
    c.execute('''CREATE TABLE IF NOT EXISTS Stok (
        id_stok INTEGER PRIMARY KEY AUTOINCREMENT,
        id_alat INTEGER,
        status_stok TEXT,
        FOREIGN KEY(id_alat) REFERENCES Alat(id_alat)
    )''')

    # Tabel Pinjaman
    c.execute('''CREATE TABLE IF NOT EXISTS Pinjaman (
        id_pinjaman INTEGER PRIMARY KEY AUTOINCREMENT,
        id_anggota INTEGER,
        tgl_pinjam DATE,
        tgl_tempo DATE,
        tgl_kembali DATE,
        status_pinjam TEXT,
        FOREIGN KEY(id_anggota) REFERENCES Anggota(id_anggota)
    )''')

    # Tabel Detail Pinjaman (Relasi Stok dan Pinjaman)
    c.execute('''CREATE TABLE IF NOT EXISTS Detail_pinjaman (
        id_detail INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pinjaman INTEGER,
        id_stok INTEGER,
        kondisi_kembali TEXT,
        FOREIGN KEY(id_pinjaman) REFERENCES Pinjaman(id_pinjaman),
        FOREIGN KEY(id_stok) REFERENCES Stok(id_stok)
    )''')

    # MENGISI DATA AWAL (SEEDING) 
    # Kita cek dulu, kalau kosong baru diisi biar tidak dobel
    c.execute("SELECT count(*) FROM Anggota")
    if c.fetchone()[0] == 0:
        # Isi Anggota (Sesuai gambar)
        anggota_data = [
            ('Taswir Hastuti', 'Aktif'), 
            ('Novi Kusmawati', 'Aktif'), 
            ('Genta Pranowo', 'Aktif'), 
            ('Raden Halim', 'Aktif'),
            ('Jamalia Najmudin', 'Aktif'),
            ('Tiara Suryono', 'Ditangguhkan'),
            ('Fitria Lazuardi', 'Aktif'),
            ('Wardi Mangunsong', 'Aktif'),
            ('Hartana Puspasari', 'Aktif'),
            ('Ajiman Sihombing', 'Aktif')
        ]
        c.executemany("INSERT INTO Anggota (nama_anggota, status_anggota) VALUES (?,?)", anggota_data)

        # Isi Alat
        alat_data = [
            ('Gelas Beaker 250ml', 'Gelas', 150000),
            ('Erlenmeyer Flask', 'Gelas', 180000),
            ('Labu Ukur 100ml', 'Gelas', 220000),
            ('Buret 50ml', 'Gelas', 350000),
            ('Pipet Volume 10ml', 'Gelas', 75000),
    ]
        c.executemany("INSERT INTO Alat (nama_alat, jenis, harga_satuan) VALUES (?,?,?)", alat_data)

        # Isi Stok (Misal kita punya 3 Gelas Beaker, 2 Erlenmeyer)
        # ID Alat 1 = Gelas Beaker, ID Alat 2 = Erlenmeyer
        stok_data = [
            (1, 'Tersedia'),
            (1, 'Tersedia'),
            (1, 'Dipinjam'),
            (1, 'Tersedia'),
            (1, 'Tersedia'),
            (2, 'Tersedia'),
            (2, 'Tersedia'),
            (2, 'Tersedia'),
            (3, 'Dipinjam'),
            (3, 'Dipinjam'),
            (3, 'Tersedia'),
            (4, 'Tersedia'),
            (5, 'Tersedia'),
            (5, 'Tersedia'),
            (5, 'Tersedia')
        ]
        c.executemany("INSERT INTO Stok (id_alat, status_stok) VALUES (?,?)", stok_data)
        
        # Buat 1 data peminjaman dummy
        pinjam_data = [
            (10, '2025-01-04', '2025-01-12', '2025-01-08', 'Dikembalikan'),
            (7, '2025-01-08', '2025-01-19', '2025-01-29', 'Dikembalikan'),
            (2, '2025-01-15', '2025-01-25', '2025-01-24', 'Dikembalikan'),
            (6, '2025-01-19', '2025-01-26', '2025-01-30', 'Dikembalikan'),
            (5, '2025-01-23', '2025-01-31', '2025-01-30', 'Dikembalikan'),
            (9, '2025-01-28', '2025-02-11', None, 'Terlambat'),
            (2, '2025-01-31', '2025-02-07', '2025-02-11', 'Dikembalikan'),
            (1, '2025-02-01', '2025-02-10', '2025-02-17', 'Dikembalikan'),
            (6, '2025-02-02', '2025-02-09', None, 'Terlambat'),
            (3, '2025-02-20', '2025-02-28', '2025-03-03', 'Dikembalikan'),
            (8, '2025-02-24', '2025-03-05', '2025-03-10', 'Dikembalikan'),
            (3, '2025-02-26', '2025-03-10', '2025-03-06', 'Dikembalikan'),
            (1, '2025-02-27', '2025-03-06', '2025-03-12', 'Dikembalikan'),
            (6, '2025-03-10', '2025-03-17', None, 'Terlambat'),
            (5, '2025-04-03', '2025-04-16', '2025-04-19', 'Dikembalikan'),
            (1, '2025-04-04', '2025-04-14', '2025-04-11', 'Dikembalikan'),
            (4, '2025-04-23', '2025-05-07', '2025-05-14', 'Dikembalikan'),
            (8, '2025-04-24', '2025-05-01', '2025-05-10', 'Dikembalikan'),
            (5, '2025-04-29', '2025-05-10', '2025-05-11', 'Dikembalikan'),
            (2, '2025-04-30', '2025-05-10', '2025-05-14', 'Dikembalikan')
        ]
        c.executemany("INSERT INTO Pinjaman (id_anggota, tgl_pinjam, tgl_tempo, tgl_kembali, status_pinjam) VALUES (?, ?, ?, ?, ?)", pinjam_data)

        detail_pinjaman_data = [
            (1, 2, 'Aman'),
            (1, 4, 'Aman'),
            (2, 5, 'Aman'),
            (3, 4, 'Aman'),
            (3, 6, 'Rusak'),
            (4, 1, 'Aman'),
            (5, 8, 'Aman'),
            (5, 6, 'Aman'),
            (6, 3, None),
            (7, 5, 'Aman'),
            (8, 6, 'Aman'),
            (9, 9, None),
            (10, 3, 'Aman'),
            (11, 9, 'Aman'),
            (11, 14, 'Aman'),
            (12, 15, 'Aman'),
            (12, 7, 'Aman'),
            (13, 1, 'Aman'),
            (13, 8, 'Aman'),
            (13, 11, 'Aman'),
            (13, 13, 'Aman'),
            (14, 10, None),
            (17, 12, 'Aman'),
            (17, 2, 'Aman'),
            (18, 13, 'Aman'),
            (18, 12, 'Aman'),
            (20, 11, 'Aman'),
            (20, 14, 'Aman'),
            (20, 10, 'Aman'),
        ]
        c.executemany("INSERT INTO Detail_pinjaman (id_pinjaman, id_stok, 'kondisi_kembali') VALUES (?, ?, ?)", detail_pinjaman_data)

        conn.commit()

    conn.close()

# Jalankan inisialisasi database sekali di awal
init_db()

# FUNGSI BANTUAN 
def get_connection():
    return sqlite3.connect(DB_FILE)

# TAMPILAN APLIKASI (FRONTEND)
st.set_page_config(page_title="Peminjaman Alat Lab", layout="wide")
st.title("Sistem Peminjaman Alat Laboratorium")

# Sidebar Menu
menu = st.sidebar.radio("Navigasi", ["Dashboard", "Peminjaman Baru (Input)", "Data Pinjaman (Read)", "Pengembalian (Update)"])

# HALAMAN 1: DASHBOARD (LAPORAN)
if menu == "Dashboard":
    st.header("Dashboard Laporan")
    conn = get_connection()
    
    # Metrik Utama
    col1, col2, col3 = st.columns(3)
    total_alat = pd.read_sql("SELECT count(*) FROM Stok", conn).iloc[0,0]
    total_pinjam = pd.read_sql("SELECT count(*) FROM Pinjaman WHERE status_pinjam='Dipinjam' or status_pinjam='Terlambat'", conn).iloc[0,0]
    total_anggota = pd.read_sql("SELECT count(*) FROM Anggota", conn).iloc[0,0]
    
    col1.metric("Total Aset Stok", total_alat)
    col2.metric("Sedang Dipinjam", total_pinjam)
    col3.metric("Jumlah Anggota", total_anggota)
    
    st.divider()
    
    # Grafik 1: Stok Berdasarkan Jenis Alat
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Stok per Alat")
        query_chart = """
        SELECT a.nama_alat, count(s.id_stok) as jumlah 
        FROM Stok s JOIN Alat a ON s.id_alat = a.id_alat 
        GROUP BY a.nama_alat
        """
        df_chart = pd.read_sql(query_chart, conn)
        st.bar_chart(df_chart.set_index('nama_alat'))

    with col_chart2:
        st.subheader("Status Stok")
        query_status = "SELECT status_stok, count(*) as jumlah FROM Stok GROUP BY status_stok"
        df_status = pd.read_sql(query_status, conn)
        st.dataframe(df_status, hide_index=True, use_container_width=True)

# HALAMAN 2: PEMINJAMAN BARU (INPUT - CREATE)
elif menu == "Peminjaman Baru (Input)":
    st.header("Form Peminjaman Alat")
    conn = get_connection()
    
    # Ambil data untuk dropdown (Dropdown Anggota & Alat)
    df_anggota = pd.read_sql("SELECT id_anggota, nama_anggota FROM Anggota WHERE status_anggota='Aktif'", conn)
    # Hanya ambil stok yang 'Tersedia'
    query_stok = """
    SELECT s.id_stok, a.nama_alat, s.id_alat 
    FROM Stok s JOIN Alat a ON s.id_alat = a.id_alat 
    WHERE s.status_stok = 'Tersedia'
    """
    df_stok = pd.read_sql(query_stok, conn)
    
    with st.form("form_pinjam"):
        # Selectbox Anggota
        anggota_pilihan = st.selectbox(
            "Pilih Anggota", 
            df_anggota['id_anggota'].tolist(), 
            format_func=lambda x: df_anggota[df_anggota['id_anggota'] == x]['nama_anggota'].values[0]
        )
        
        # Selectbox Alat (Stok Tersedia)
        stok_pilihan = st.selectbox(
            "Pilih Alat (Hanya yang Tersedia)", 
            df_stok['id_stok'].tolist(),
            format_func=lambda x: f"ID: {x} - " + df_stok[df_stok['id_stok'] == x]['nama_alat'].values[0]
        )
        
        tgl = st.date_input("Tanggal Pinjam", date.today())

        tgl_tempo = st.date_input("Jatuh Tempo", date.today() + pd.Timedelta(days=7))
        
        submit = st.form_submit_button("Simpan Peminjaman")
        
        if submit:
            c = conn.cursor()
            # Insert ke Tabel Pinjaman
            c.execute("INSERT INTO Pinjaman (id_anggota, tgl_pinjam, tgl_tempo, status_pinjam) VALUES (?, ?, ?, 'Dipinjam')", (anggota_pilihan, tgl, tgl_tempo))
            id_pinjam_baru = c.lastrowid
            
            # Insert ke Tabel Detail_pinjaman
            c.execute("INSERT INTO Detail_pinjaman (id_pinjaman, id_stok) VALUES (?, ?)", (id_pinjam_baru, stok_pilihan))
            
            # Update Status Stok jadi 'Dipinjam'
            c.execute("UPDATE Stok SET status_stok = 'Dipinjam' WHERE id_stok = ?", (stok_pilihan,))
            
            conn.commit()
            st.success("Peminjaman berhasil disimpan!")

# HALAMAN 3: LIHAT DATA (READ)
elif menu == "Data Pinjaman (Read)":
    st.header("Data Riwayat Peminjaman")
    conn = get_connection()
    
    # Query JOIN Antar Tabel (Menghubungkan Pinjaman -> Anggota -> Detail -> Stok -> Alat)
    # Ini memenuhi tujuan "Menunjukkan bagaimana database digunakan"
    query_lengkap = """
    SELECT 
        p.id_pinjaman,
        ang.nama_anggota,
        a.nama_alat,
        p.tgl_pinjam,
        p.tgl_tempo,
        p.tgl_kembali,
        p.status_pinjam
    FROM Pinjaman p
    JOIN Anggota ang ON p.id_anggota = ang.id_anggota
    JOIN Detail_pinjaman dp ON p.id_pinjaman = dp.id_pinjaman
    JOIN Stok s ON dp.id_stok = s.id_stok
    JOIN Alat a ON s.id_alat = a.id_alat
    ORDER BY p.id_pinjaman ASC
    """
    
    df_view = pd.read_sql(query_lengkap, conn)
    st.dataframe(df_view, use_container_width=True)

# HALAMAN 4 PENGEMBALIAN (UPDATE) 
elif menu == "Pengembalian (Update)":
    st.header("Update Status Pengembalian")
    conn = get_connection()
    
    # Cari pinjaman yang masih 'Dipinjam'
    df_aktif = pd.read_sql("""
        SELECT p.id_pinjaman, ag.nama_anggota, al.nama_alat 
        FROM Pinjaman p 
        JOIN Anggota ag ON p.id_anggota=ag.id_anggota
        JOIN Detail_pinjaman dp ON p.id_pinjaman=dp.id_pinjaman
        JOIN Stok s ON dp.id_stok=s.id_stok
        JOIN Alat al ON s.id_alat=al.id_alat
        WHERE p.status_pinjam='Dipinjam'
    """, conn)
    
    pilih_id = st.selectbox("Pilih ID Pinjaman", df_aktif['id_pinjaman'])
    kondisi = st.radio("Bagaimana Kondisi Barang Saat Kembali?", ["Aman", "Rusak"])
    
    if st.button("Proses Pengembalian"):
        c = conn.cursor()
        tgl_sekarang = date.today()
        
        # Update Tabel Pinjaman
        c.execute("UPDATE Pinjaman SET status_pinjam = 'Dikembalikan', tgl_kembali = ? WHERE id_pinjaman = ?", (tgl_sekarang, pilih_id,))

        # Update Kondisi di Detail_pinjaman
        c.execute("UPDATE Detail_pinjaman SET kondisi_kembali=? WHERE id_pinjaman=?", (kondisi, pilih_id,))
        
        # Cari ID Stok yang terkait untuk dikembalikan statusnya
        c.execute("SELECT id_stok FROM Detail_pinjaman WHERE id_pinjaman = ?", (pilih_id,))
        id_stok = c.fetchone()[0]
        
        # Update Tabel Stok jadi 'Tersedia' kembali
        c.execute("UPDATE Stok SET status_stok = 'Tersedia' WHERE id_stok = ?", (id_stok,))
        
        conn.commit()
        st.success(f"Pinjaman ID {pilih_id} berhasil dikembalikan. Stok kembali tersedia.")