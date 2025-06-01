import numpy as np

def trapmf(x, a, b, c, d):
    return np.maximum(0, np.minimum(np.minimum((x-a)/(b-a+1e-6), 1), (d-x)/(d-c+1e-6)))

def trimf(x, a, b, c):
    return np.maximum(0, np.minimum((x-a)/(b-a+1e-6), (c-x)/(c-b+1e-6)))

def interpretasi_durasi(durasi):
    if durasi <= 30:
        return "≤ 30 menit"
    elif 30 < durasi <= 60:
        return "30 – 60 menit"
    elif 60 < durasi <= 90:
        return "60 – 90 menit"
    else:
        return "> 90 menit"

def fuzzy_rekomendasi(fokus, kelelahan, beban):
    # Perbaikan agar nilai 10 tidak menghasilkan μ = 0
    fokus_low = trapmf(fokus, 0, 0, 2, 4)
    fokus_med = trimf(fokus, 3, 5, 7)
    fokus_high = trapmf(fokus, 6, 7.5, 9.5, 10.5)

    kelelahan_vtired = trapmf(kelelahan, 0, 0, 2, 4)
    kelelahan_tired = trimf(kelelahan, 3, 5, 7)
    kelelahan_fresh = trapmf(kelelahan, 6, 7.5, 9.5, 10.5)

    beban_light = trapmf(beban, 0, 0, 2, 4)
    beban_med = trimf(beban, 3, 5, 7)
    beban_heavy = trapmf(beban, 6, 7.5, 9.5, 10.5)

    # Inferensi aturan fuzzy
    r1 = min(fokus_high, kelelahan_fresh, beban_heavy)  # Long
    r2 = min(fokus_med, kelelahan_tired, beban_med)     # Medium
    r3 = min(fokus_low, kelelahan_vtired, beban_light)  # Short
    r4 = max(fokus_med, kelelahan_tired, beban_med)     # Fallback Medium

    durasi = (
        r1 * 100 +  # Long
        r2 * 45 +
        r3 * 15 +
        r4 * 45
    ) / (r1 + r2 + r3 + r4 + 1e-6)

    if r1 == max(r1, r2, r3, r4):
        waktu = "Sekarang"
    elif r2 == max(r1, r2, r3, r4) or r4 == max(r1, r2, r3, r4):
        waktu = "Nanti"
    else:
        waktu = "Besok"

    return durasi, waktu

# PROGRAM UTAMA
while True:
    print("\n=== SISTEM REKOMENDASI WAKTU BELAJAR BERBASIS FUZZY LOGIC ===")

    # Input Fokus
    print("\n1. Bagaimana tingkat fokus Anda saat ini?")
    print("   a. Sangat sulit fokus")
    print("   b. Sulit fokus")
    print("   c. Fokus sedang")
    print("   d. Mudah fokus")
    jawaban_fokus = input("Jawaban Anda (a/b/c/d): ").lower()
    fokus = {'a': 2, 'b': 4, 'c': 6, 'd': 10}.get(jawaban_fokus)

    # Input Kelelahan
    print("\n2. Bagaimana tingkat kelelahan Anda saat ini?")
    print("   a. Sangat lelah dan mengantuk")
    print("   b. Cukup lelah")
    print("   c. Tidak terlalu lelah")
    print("   d. Segar dan siap belajar")
    jawaban_kelelahan = input("Jawaban Anda (a/b/c/d): ").lower()
    kelelahan = {'a': 2, 'b': 6, 'c': 8, 'd': 10}.get(jawaban_kelelahan)

    # Input Beban Tugas
    print("\n3. Bagaimana beban tugas Anda hari ini?")
    print("   a. Tidak ada tugas")
    print("   b. Sedikit tugas")
    print("   c. Tugas sedang")
    print("   d. Sangat banyak tugas")
    jawaban_beban = input("Jawaban Anda (a/b/c/d): ").lower()
    beban = {'a': 1, 'b': 3, 'c': 6, 'd': 10}.get(jawaban_beban)

    if None in (fokus, kelelahan, beban):
        print("\n❌ Input tidak valid. Silakan ulangi dengan a/b/c/d.")
        continue

    # Proses fuzzy
    durasi_crisp, waktu_output = fuzzy_rekomendasi(fokus, kelelahan, beban)

    # Output
    print("\n=== HASIL REKOMENDASI ===")
    print(f"Durasi Belajar       : {interpretasi_durasi(durasi_crisp)}")
    print(f"Waktu Belajar Terbaik: {waktu_output}")

    # Ulangi?
    ulang = input("\nIngin mengulang sistem? (y/n): ").lower()
    if ulang != 'y':
        print("\nTerima kasih telah menggunakan sistem ini!")
        break
