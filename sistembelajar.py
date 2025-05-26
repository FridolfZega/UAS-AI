import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import os

# Inisialisasi variabel fuzzy
focus = ctrl.Antecedent(np.arange(0, 11, 1), 'focus')
fatigue = ctrl.Antecedent(np.arange(0, 11, 1), 'fatigue')
workload = ctrl.Antecedent(np.arange(0, 11, 1), 'workload')
duration = ctrl.Consequent(np.arange(0, 91, 1), 'duration')
timing = ctrl.Consequent(np.arange(0, 3, 1), 'timing')  # 0=Besok, 1=Nanti, 2=Sekarang

# Membership functions
focus['low'] = fuzz.trimf(focus.universe, [0, 0, 5])
focus['medium'] = fuzz.trimf(focus.universe, [3, 5, 7])
focus['high'] = fuzz.trimf(focus.universe, [5, 10, 10])

fatigue['very_tired'] = fuzz.trimf(fatigue.universe, [7, 10, 10])
fatigue['tired'] = fuzz.trimf(fatigue.universe, [3, 5, 7])
fatigue['fresh'] = fuzz.trimf(fatigue.universe, [0, 0, 5])

workload['light'] = fuzz.trimf(workload.universe, [0, 0, 5])
workload['medium'] = fuzz.trimf(workload.universe, [3, 5, 7])
workload['heavy'] = fuzz.trimf(workload.universe, [5, 10, 10])

duration['short'] = fuzz.trimf(duration.universe, [0, 0, 30])
duration['medium'] = fuzz.trimf(duration.universe, [20, 45, 60])
duration['long'] = fuzz.trimf(duration.universe, [60, 90, 90])

timing['besok'] = fuzz.trimf(timing.universe, [0, 0, 1])
timing['nanti'] = fuzz.trimf(timing.universe, [0, 1, 2])
timing['sekarang'] = fuzz.trimf(timing.universe, [1, 2, 2])

# Aturan fuzzy + fallback
rules = [
    ctrl.Rule(focus['high'] & fatigue['fresh'] & workload['heavy'], (duration['long'], timing['sekarang'])),
    ctrl.Rule(focus['medium'] & fatigue['tired'] & workload['medium'], (duration['medium'], timing['nanti'])),
    ctrl.Rule(focus['low'] & fatigue['very_tired'] & workload['light'], (duration['short'], timing['besok'])),
    ctrl.Rule(focus['medium'] & fatigue['fresh'] & workload['light'], (duration['medium'], timing['sekarang'])),
    ctrl.Rule(focus['high'] & fatigue['tired'] & workload['medium'], (duration['medium'], timing['nanti'])),
    ctrl.Rule(focus['medium'] | fatigue['tired'] | workload['medium'], (duration['medium'], timing['nanti']))  # fallback
]

study_ctrl = ctrl.ControlSystem(rules)

# Mapping input
def map_focus(answer): return {'1': 2, '2': 4, '3': 6, '4': 9}[answer]
def map_fatigue(answer): return {'1': 9, '2': 6, '3': 4, '4': 1}[answer]
def map_workload(answer): return {'1': 1, '2': 4, '3': 6, '4': 9}[answer]

# Validasi input
def safe_input(prompt, options):
    while True:
        print(prompt)
        for key, val in options.items():
            print(f"  {key}. {val}")
        inp = input("Jawaban (1-4): ")
        if inp in options:
            return inp
        else:
            print("⚠️ Masukkan hanya angka 1–4.\n")

# Opsi jawaban
focus_opts = {'1': "Sangat sulit fokus", '2': "Sulit fokus", '3': "Fokus sedang", '4': "Mudah fokus"}
fatigue_opts = {'1': "Sangat lelah dan mengantuk", '2': "Cukup lelah", '3': "Tidak terlalu lelah", '4': "Segar dan siap belajar"}
workload_opts = {'1': "Tidak ada tugas", '2': "Sedikit tugas", '3': "Tugas sedang", '4': "Sangat banyak tugas"}

# Looping sistem
while True:
    # Clear layar (opsional, hanya Windows)
    os.system('cls' if os.name == 'nt' else 'clear')

    print("=== Sistem Rekomendasi Waktu Belajar (Fuzzy Logic) ===\n")
    f_input = safe_input("1. Seberapa fokus Anda saat ini?", focus_opts)
    fa_input = safe_input("\n2. Bagaimana kondisi fisik Anda?", fatigue_opts)
    w_input = safe_input("\n3. Seberapa berat beban tugas Anda hari ini?", workload_opts)

    # Proses fuzzy (reset setiap kali)
    study_sim = ctrl.ControlSystemSimulation(study_ctrl)
    study_sim.input['focus'] = map_focus(f_input)
    study_sim.input['fatigue'] = map_fatigue(fa_input)
    study_sim.input['workload'] = map_workload(w_input)

    try:
        study_sim.compute()
        dur = round(study_sim.output['duration'])
        t = round(study_sim.output['timing'])
        t_label = {0: "Besok", 1: "Nanti", 2: "Sekarang"}.get(t, "-")

        # Interpretasi kategori durasi
        if dur <= 30:
            dur_label = "≤ 30 menit"
        elif dur <= 60:
            dur_label = "30 – 60 menit"
        elif dur <= 90:
            dur_label = "60 – 90 menit"
        else:
            dur_label = "> 90 menit"

        print("\n=== Rekomendasi Sistem ===")
        print(f"- Durasi Belajar Disarankan : {dur_label}")
        print(f"- Waktu Belajar Terbaik     : {t_label}")
    except Exception as e:
        print("\n❌ Sistem gagal menghitung rekomendasi.")
        print(f"Detail: {e}")

    # Tanya user apakah ingin ulang
    ulang = input("\nIngin mengulang program? (y/n): ").lower()
    if ulang != 'y':
        print("\nTerima kasih telah menggunakan sistem ini!")
        break
