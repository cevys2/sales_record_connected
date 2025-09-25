# File: sistem_bisnis.py
# (Versi yang sudah dimodifikasi untuk UI)
import pandas as pd

class Inventaris:
    def __init__(self, id_barang, nama_barang, stok, harga):
        self.id_barang = id_barang
        self.nama_barang = nama_barang
        self.stok = int(stok)
        self.harga = float(harga)

    def __repr__(self):
        return f"ID: {self.id_barang}, Nama: {self.nama_barang}, Stok: {self.stok}, Harga: {self.harga}"

    def tambah_stok(self, jumlah):
        if jumlah > 0:
            self.stok += jumlah
        else:
            print("Error: Jumlah harus positif.")

    def kurangi_stok(self, jumlah):
        if 0 < jumlah <= self.stok:
            self.stok -= jumlah
            return True
        else:
            return False

class Lokasi:
    def __init__(self, id_lokasi, nama_lokasi, alamat):
        self.id_lokasi = id_lokasi
        self.nama_lokasi = nama_lokasi
        self.alamat = alamat

    def __repr__(self):
        return f"[{self.id_lokasi}] {self.nama_lokasi}"

class Salesman:
    def __init__(self, id_salesman, nama_salesman):
        self.id_salesman = id_salesman
        self.nama_salesman = nama_salesman

    def __repr__(self):
        return f"[{self.id_salesman}] {self.nama_salesman}"

class Penjualan:
    def __init__(self, id_transaksi, barang, jumlah, salesman, lokasi):
        self.id_transaksi = id_transaksi
        self.barang = barang
        self.jumlah = jumlah
        self.salesman = salesman
        self.lokasi = lokasi
        self.total_harga = barang.harga * jumlah

    def get_details(self):
        return (
            f"ID Trx: {self.id_transaksi}\n"
            f"Barang: {self.barang.nama_barang} (x{self.jumlah})\n"
            f"Total: Rp {self.total_harga:,.2f}\n"
            f"Sales: {self.salesman.nama_salesman}\n"
            f"Lokasi: {self.lokasi.nama_lokasi}\n"
        )

class SistemManajemen:
    def __init__(self):
        self.inventaris = {}
        self.salesman = {}
        self.lokasi = {}
        self.penjualan = []
        self.id_transaksi_terakhir = 0
        self._inisialisasi_data_awal()

    def _inisialisasi_data_awal(self):
        """Menambahkan data dummy untuk demo."""
        self.tambah_barang("B001", "Laptop Pro", 50, 15000000)
        self.tambah_barang("B002", "Mouse Wireless", 200, 250000)
        self.tambah_salesman("S01", "Budi Santoso")
        self.tambah_salesman("S02", "Citra Lestari")
        self.tambah_lokasi("L01", "Gudang Jakarta", "Jl. Sudirman No. 1")
        self.tambah_lokasi("L02", "Toko Bandung", "Jl. Asia Afrika No. 10")

    def tambah_barang(self, id_barang, nama_barang, stok, harga):
        if id_barang in self.inventaris:
            return False, f"Error: ID Barang '{id_barang}' sudah ada."
        try:
            barang_baru = Inventaris(id_barang, nama_barang, int(stok), float(harga))
            self.inventaris[id_barang] = barang_baru
            return True, f"Barang '{nama_barang}' berhasil ditambahkan."
        except ValueError:
            return False, "Error: Stok harus angka dan Harga harus angka."

    def tambah_salesman(self, id_salesman, nama_salesman):
        if id_salesman in self.salesman:
            return False, f"Error: ID Salesman '{id_salesman}' sudah ada."
        salesman_baru = Salesman(id_salesman, nama_salesman)
        self.salesman[id_salesman] = salesman_baru
        return True, f"Salesman '{nama_salesman}' berhasil ditambahkan."

    def tambah_lokasi(self, id_lokasi, nama_lokasi, alamat):
        if id_lokasi in self.lokasi:
            return False, f"Error: ID Lokasi '{id_lokasi}' sudah ada."
        lokasi_baru = Lokasi(id_lokasi, nama_lokasi, alamat)
        self.lokasi[id_lokasi] = lokasi_baru
        return True, f"Lokasi '{nama_lokasi}' berhasil ditambahkan."

    def catat_penjualan(self, id_barang, jumlah, id_salesman, id_lokasi):
        barang = self.inventaris.get(id_barang)
        salesman = self.salesman.get(id_salesman)
        lokasi = self.lokasi.get(id_lokasi)

        if not all([barang, salesman, lokasi]):
            return False, "Error: Data Barang, Salesman, atau Lokasi tidak valid."
        
        try:
            jumlah_int = int(jumlah)
            if jumlah_int <= 0:
                return False, "Error: Jumlah harus lebih dari 0."
        except ValueError:
            return False, "Error: Jumlah harus berupa angka."

        if barang.kurangi_stok(jumlah_int):
            self.id_transaksi_terakhir += 1
            transaksi_baru = Penjualan(self.id_transaksi_terakhir, barang, jumlah_int, salesman, lokasi)
            self.penjualan.append(transaksi_baru)
            return True, f"Penjualan (ID: {self.id_transaksi_terakhir}) berhasil dicatat."
        else:
            return False, f"Error: Stok '{barang.nama_barang}' tidak mencukupi."
        
    def import_inventaris_from_excel(self, file_path):
        """Membaca sheet 'Inventaris' dari file Excel."""
        try:
            # Tambahkan parameter sheet_name
            df = pd.read_excel(file_path, sheet_name="Inventaris")
            required_cols = {'ID_Barang', 'Nama_Barang', 'Stok', 'Harga'}
            if not required_cols.issubset(df.columns):
                return False, "[Inventaris] Error: Kolom tidak sesuai."

            count = 0
            for index, row in df.iterrows():
                # Fungsi tambah_barang akan return (True/False, pesan)
                sukses, _ = self.tambah_barang(
                    id_barang=row['ID_Barang'],
                    nama_barang=row['Nama_Barang'],
                    stok=row['Stok'],
                    harga=row['Harga']
                )
                if sukses: count += 1
            return True, f"[Inventaris] {count} data berhasil diimpor."
        except Exception as e:
            return False, f"[Inventaris] Error: {e}"
        
    def import_salesman_from_excel(self, file_path):
        """Membaca sheet 'Salesman' dari file Excel."""
        try:
            df = pd.read_excel(file_path, sheet_name="Salesman")
            required_cols = {'ID_Salesman', 'Nama_Salesman'}
            if not required_cols.issubset(df.columns):
                return False, "[Salesman] Error: Kolom tidak sesuai."
            
            count = 0
            for index, row in df.iterrows():
                sukses, _ = self.tambah_salesman(
                    id_salesman=row['ID_Salesman'],
                    nama_salesman=row['Nama_Salesman']
                )
                if sukses: count += 1
            return True, f"[Salesman] {count} data berhasil diimpor."
        except Exception as e:
            return False, f"[Salesman] Error: {e}"
        
    def import_lokasi_from_excel(self, file_path):
        """Membaca sheet 'Lokasi' dari file Excel."""
        try:
            df = pd.read_excel(file_path, sheet_name="Lokasi")
            required_cols = {'ID_Lokasi', 'Nama_Lokasi', 'Alamat'}
            if not required_cols.issubset(df.columns):
                return False, "[Lokasi] Error: Kolom tidak sesuai."

            count = 0
            for index, row in df.iterrows():
                sukses, _ = self.tambah_lokasi(
                    id_lokasi=row['ID_Lokasi'],
                    nama_lokasi=row['Nama_Lokasi'],
                    alamat=row['Alamat']
                )
                if sukses: count += 1
            return True, f"[Lokasi] {count} data berhasil diimpor."
        except Exception as e:
            return False, f"[Lokasi] Error: {e}"


    def get_list_inventaris(self):
        return list(self.inventaris.values())

    def get_list_salesman(self):
        return list(self.salesman.values())

    def get_list_lokasi(self):
        return list(self.lokasi.values())