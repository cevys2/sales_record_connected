# File: app_ui.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from sistem_bisnis import SistemManajemen

class App(tk.Tk):
    def __init__(self, sistem: SistemManajemen):
        super().__init__()
        self.sistem = sistem
        self.title("Sistem Manajemen Sederhana")
        self.geometry("800x600")

        # Style
        style = ttk.Style(self)
        style.theme_use("clam")

        # --- MEMBUAT MENU BAR ---
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Menu File
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Data Master dari Excel...", command=self.import_semua_data)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.quit)

        # Notebook (untuk tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Membuat Frames untuk setiap tab
        self.frame_penjualan = ttk.Frame(self.notebook, padding="10")
        self.frame_inventaris = ttk.Frame(self.notebook, padding="10")
        self.frame_salesman = ttk.Frame(self.notebook, padding="10")
        self.frame_lokasi = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.frame_penjualan, text="Catat Penjualan")
        self.notebook.add(self.frame_inventaris, text="Inventaris")
        self.notebook.add(self.frame_salesman, text="Salesman")
        self.notebook.add(self.frame_lokasi, text="Lokasi")

        # Memanggil fungsi untuk mengisi konten setiap tab
        self.create_widgets_penjualan()
        self.create_widgets_inventaris()
        # Anda bisa menambahkan fungsi untuk salesman dan lokasi dengan pola yang sama
        
        # Inisialisasi data di tabel
        self.refresh_tabel_inventaris()

    # --- TAB PENJUALAN ---
    def create_widgets_penjualan(self):
        frame = self.frame_penjualan
        
        # Form Penjualan
        form_frame = ttk.LabelFrame(frame, text="Form Input Penjualan")
        form_frame.pack(fill="x", padx=10, pady=10)

        # Barang
        ttk.Label(form_frame, text="Pilih Barang:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_barang = ttk.Combobox(form_frame, state="readonly", values=self.get_nama_barang_list())
        self.combo_barang.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Jumlah
        ttk.Label(form_frame, text="Jumlah:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_jumlah = ttk.Entry(form_frame)
        self.entry_jumlah.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Salesman
        ttk.Label(form_frame, text="Pilih Salesman:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.combo_salesman = ttk.Combobox(form_frame, state="readonly", values=self.get_nama_salesman_list())
        self.combo_salesman.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Lokasi
        ttk.Label(form_frame, text="Pilih Lokasi:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.combo_lokasi = ttk.Combobox(form_frame, state="readonly", values=self.get_nama_lokasi_list())
        self.combo_lokasi.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        form_frame.grid_columnconfigure(1, weight=1)

        # Tombol
        btn_catat = ttk.Button(frame, text="Catat Transaksi", command=self.catat_penjualan)
        btn_catat.pack(pady=10)

        # Laporan Penjualan
        report_frame = ttk.LabelFrame(frame, text="Laporan Penjualan Terakhir")
        report_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.text_laporan = tk.Text(report_frame, height=15, width=80, state="disabled")
        self.text_laporan.pack(padx=5, pady=5, fill="both", expand=True)

    def catat_penjualan(self):
        try:
            barang_terpilih = self.combo_barang.get().split("]")[0][1:]
            salesman_terpilih = self.combo_salesman.get().split("]")[0][1:]
            lokasi_terpilih = self.combo_lokasi.get().split("]")[0][1:]
            jumlah = self.entry_jumlah.get()

            if not all([barang_terpilih, salesman_terpilih, lokasi_terpilih, jumlah]):
                messagebox.showwarning("Input Tidak Lengkap", "Harap isi semua kolom.")
                return

            sukses, pesan = self.sistem.catat_penjualan(barang_terpilih, jumlah, salesman_terpilih, lokasi_terpilih)

            if sukses:
                messagebox.showinfo("Sukses", pesan)
                self.entry_jumlah.delete(0, tk.END)
                self.refresh_all()
            else:
                messagebox.showerror("Gagal", pesan)
        except IndexError:
            messagebox.showerror("Error", "Pilihan tidak valid. Pastikan semua dropdown dipilih.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    # --- TAB INVENTARIS ---
    def create_widgets_inventaris(self):
        frame = self.frame_inventaris

        # Form Tambah Barang
        form_frame = ttk.LabelFrame(frame, text="Form Tambah Barang")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="ID Barang:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id_barang = ttk.Entry(form_frame)
        self.entry_id_barang.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Nama Barang:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nama_barang = ttk.Entry(form_frame)
        self.entry_nama_barang.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Stok:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_stok = ttk.Entry(form_frame)
        self.entry_stok.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Harga:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_harga = ttk.Entry(form_frame)
        self.entry_harga.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)

        btn_tambah = ttk.Button(form_frame, text="Tambah Barang", command=self.tambah_barang)
        btn_tambah.grid(row=2, column=0, columnspan=4, pady=10,)

       

        # Tabel Inventaris
        tabel_frame = ttk.Frame(frame)
        tabel_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("ID Barang", "Nama Barang", "Stok", "Harga")
        self.tabel_inventaris = ttk.Treeview(tabel_frame, columns=cols, show="headings")
        for col in cols:
            self.tabel_inventaris.heading(col, text=col)
        self.tabel_inventaris.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabel_frame, orient="vertical", command=self.tabel_inventaris.yview)
        self.tabel_inventaris.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def import_semua_data(self):
        """Membuka dialog file dan mengimpor semua data dari 3 sheet."""
        file_path = filedialog.askopenfilename(
            title="Pilih File Excel Data Master",
            filetypes=(("Excel Files", "*.xlsx"), ("All files", "*.*"))
        )
        if not file_path:
            return
        
        # Panggil ketiga fungsi import
        hasil_inventaris = self.sistem.import_inventaris_from_excel(file_path)
        hasil_salesman = self.sistem.import_salesman_from_excel(file_path)
        hasil_lokasi = self.sistem.import_lokasi_from_excel(file_path)

        # Gabungkan semua pesan untuk ditampilkan
        pesan_akhir = (
            f"{hasil_inventaris[1]}\n"
            f"{hasil_salesman[1]}\n"
            f"{hasil_lokasi[1]}"
        )

        messagebox.showinfo("Hasil Impor", pesan_akhir)
        self.refresh_all() # Wajib untuk update seluruh UI


    def tambah_barang(self):
        id_b = self.entry_id_barang.get()
        nama = self.entry_nama_barang.get()
        stok = self.entry_stok.get()
        harga = self.entry_harga.get()

        if not all([id_b, nama, stok, harga]):
            messagebox.showwarning("Input Tidak Lengkap", "Harap isi semua kolom untuk menambah barang.")
            return

        sukses, pesan = self.sistem.tambah_barang(id_b, nama, stok, harga)
        if sukses:
            messagebox.showinfo("Sukses", pesan)
            # Kosongkan form
            self.entry_id_barang.delete(0, tk.END)
            self.entry_nama_barang.delete(0, tk.END)
            self.entry_stok.delete(0, tk.END)
            self.entry_harga.delete(0, tk.END)
            self.refresh_all()
        else:
            messagebox.showerror("Gagal", pesan)

    # --- FUNGSI BANTUAN & REFRESH ---
    def refresh_tabel_inventaris(self):
        # Hapus data lama
        for item in self.tabel_inventaris.get_children():
            self.tabel_inventaris.delete(item)
        # Masukkan data baru
        for barang in self.sistem.get_list_inventaris():
            self.tabel_inventaris.insert("", tk.END, values=(barang.id_barang, barang.nama_barang, barang.stok, f"Rp {barang.harga:,.2f}"))

    def refresh_combobox(self):
        self.combo_barang['values'] = self.get_nama_barang_list()
        self.combo_salesman['values'] = self.get_nama_salesman_list()
        self.combo_lokasi['values'] = self.get_nama_lokasi_list()

    def refresh_laporan_penjualan(self):
        self.text_laporan.config(state="normal")
        self.text_laporan.delete(1.0, tk.END)
        if not self.sistem.penjualan:
            self.text_laporan.insert(tk.END, "Belum ada transaksi.")
        else:
            # Tampilkan 5 transaksi terakhir
            for trx in reversed(self.sistem.penjualan[-5:]):
                self.text_laporan.insert(tk.END, trx.get_details() + "-"*20 + "\n")
        self.text_laporan.config(state="disabled")

    def refresh_all(self):
        """Panggil semua fungsi refresh."""
        self.refresh_tabel_inventaris()
        self.refresh_combobox()
        self.refresh_laporan_penjualan()
        
    def get_nama_barang_list(self):
        return [f"[{b.id_barang}] {b.nama_barang}" for b in self.sistem.get_list_inventaris()]
    
    def get_nama_salesman_list(self):
        return [f"[{s.id_salesman}] {s.nama_salesman}" for s in self.sistem.get_list_salesman()]

    def get_nama_lokasi_list(self):
        return [f"[{l.id_lokasi}] {l.nama_lokasi}" for l in self.sistem.get_list_lokasi()]

if __name__ == "__main__":
    sistem_manajemen = SistemManajemen()
    app = App(sistem_manajemen)
    app.mainloop()