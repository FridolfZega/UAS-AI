import numpy as np
import matplotlib.pyplot as plt

# Fungsi trapezoid membership function
def trapmf(x, a, b, c, d):
    return np.maximum(0, np.minimum(np.minimum((x - a) / (b - a + 1e-6), 1), (d - x) / (d - c + 1e-6)))

# Fungsi triangle membership function
def trimf(x, a, b, c):
    return np.maximum(0, np.minimum((x - a) / (b - a + 1e-6), (c - x) / (c - b + 1e-6)))

# Range nilai kelelahan (0–10)
x = np.linspace(0, 10, 1000)

# Membership functions untuk kelelahan
kelelahan_vtired = trapmf(x, 0, 0, 2, 4)
kelelahan_tired = trimf(x, 3, 5, 7)
kelelahan_fresh = trapmf(x, 6, 7.5, 9.5, 10.5)

# Plotting grafik
plt.figure(figsize=(10, 5))
plt.plot(x, kelelahan_vtired, 'r-', label='Very Tired')
plt.plot(x, kelelahan_tired, 'k-', label='Tired')
plt.plot(x, kelelahan_fresh, 'g-', label='Fresh')
plt.title('Membership Function - Kelelahan')
plt.xlabel('Nilai')
plt.ylabel('Keanggotaan')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
