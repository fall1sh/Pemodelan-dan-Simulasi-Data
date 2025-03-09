import numpy as np
import matplotlib.pyplot as plt

num_points = 10000

X = np.random.rand(num_points)
Y = np.random.rand(num_points)

distances = X**2 + Y**2

inside_circle = distances <= 1

pi_estimate = 4 * np.sum(inside_circle) / num_points

plt.figure(figsize=(6,6))
plt.scatter(X[inside_circle], Y[inside_circle], color='blue', s=1, label='Dalam Lingkaran')
plt.scatter(X[~inside_circle], Y[~inside_circle], color='red', s=1, label='Luar Lingkaran')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title(f'Simulasi Monte Carlo Estimasi Pi\nEstimasi Pi = {pi_estimate:.5f}')
plt.show()

print(f'Estimasi nilai π: {pi_estimate:.5f}')
