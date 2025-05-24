import os
import random
import threading
import time
import requests

# Warna ANSI
colors = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]
RESET = "\033[0m"
HIJAU = "\033[92m"
KUNING = "\033[93m"
BIRU = "\033[94m"

# Banner
banner_lines = [
    " __        __   _                            _   _                 ",
    " \\ \\      / /__| | ___ ___  _ __ ___   ___  | \\ | | _____      __ ",
    "  \\ \\ /\\ / / _ \\ |/ __/ _ \\| '_ ` _ \\ / _ \\ |  \\| |/ _ \\ \\ /\\ / / ",
    "   \\ V  V /  __/ | (_| (_) | | | | | |  __/ | |\\  |  __/\\ V  V /  ",
    "    \\_/\\_/ \\___|_|\\___\\___/|_| |_| |_|\\___| |_| \\_|\\___| \\_/\\_/   "
]

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def tampilkan_banner():
    clear_screen()
    for line in banner_lines:
        warna = random.choice(colors)
        print(f"{warna}{line}{RESET}")
    print(f"\n{KUNING}  Tools WhatsApp Number Generator & Checker {RESET}")
    print(f"{BIRU}  Made by Fatillah Developer{RESET}\n")

def generate_numbers(base, digit_3_range=range(0, 10), suffix_range=range(1, 100)):
    hasil = []
    for d3 in digit_3_range:
        for i in suffix_range:
            nomor = list(base)
            nomor[-3] = str(d3)
            nomor[-2:] = list(str(i).zfill(2))
            hasil.append("".join(nomor))
    return hasil

def check_number_active(nomor, aktif_list, lock):
    url = f"https://wa.me/{nomor}"
    try:
        res = requests.get(url, timeout=5)
        if "Use WhatsApp" in res.text or "Chat on WhatsApp" in res.text:
            print(f"{HIJAU}Active: {nomor}{RESET}")
            with lock:
                aktif_list.append(nomor)
    except:
        pass  # skip error/invalid

def dump_numbers(base_nomor, kode_negara, total_angka3=3, filename="hasil"):
    if len(base_nomor) < 3:
        print("Nomor minimal 3 digit.")
        return

    base = list(kode_negara + base_nomor)
    aktif = []
    lock = threading.Lock()

    print(f"{KUNING}Mulai proses generate dan check...{RESET}\n")
    threads = []

    for d3 in range(1, total_angka3 + 1):
        for i in range(1, 100):
            nomor = list(base)
            nomor[-3] = str(d3)
            nomor[-2:] = list(str(i).zfill(2))
            nomor_final = "".join(nomor)

            t = threading.Thread(target=check_number_active, args=(nomor_final, aktif, lock))
            t.start()
            threads.append(t)

            time.sleep(0.01)  # delay kecil biar stabil

    for t in threads:
        t.join()

    if aktif:
        random.shuffle(aktif)
        with open(f"{filename}.txt", "w") as f:
            for nomor in aktif:
                f.write(nomor + "\n")
        print(f"\n{HIJAU}Selesai! {len(aktif)} nomor aktif disimpan di {filename}.txt{RESET}")
    else:
        print(f"\n{KUNING}Tidak ada nomor aktif ditemukan.{RESET}")

def menu():
    while True:
        tampilkan_banner()
        print(f"""{BIRU}
[1] Dump & Check WhatsApp Numbers
[0] Exit
{RESET}""")
        pilih = input("Pilih menu: ").strip()
        if pilih == "1":
            print(f"{KUNING}Contoh kode negara: +972 (Israel), +91 (India), +1 (USA){RESET}")
            kode = input("Masukkan kode negara: ").strip()
            dasar = input("Masukkan nomor dasar (tanpa kode negara): ").strip()
            ganti_digit3 = input("Ganti angka ke-3 dari belakang sampai (default 3): ").strip()
            jumlah_ganti = int(ganti_digit3) if ganti_digit3.isdigit() else 3
            nama_file = input("Nama file output: ").strip()
            dump_numbers(dasar, kode, total_angka3=jumlah_ganti, filename=nama_file)
            input(f"\n{BIRU}Tekan Enter untuk kembali ke menu...{RESET}")
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter...")

if __name__ == "__main__":
    menu()
