import math
from scipy import stats
import numpy as np


file_path = "Москва_2021.txt"
with open(file_path, 'r') as file:
    data = file.read().splitlines()
data = list(map(int, data))

# Параметры
gamma = 0.95
delta = 3
n_samples = 36
std_dev = 12.038146371631095
t = 1.96


def mean(data):
    return sum(data) / len(data)


def variance(data):
    m = mean(data)
    return sum((x - m) ** 2 for x in data) / (len(data))


def stddev(data):
   return math.sqrt(variance(data))


s_size = 62

# Генерация выборок и расчет выборочных средних
n_selection = 36
lst_selection = []
lst_mean = []

for _ in range(n_selection):
    selection = list(np.random.choice(data, size=s_size, replace=True))
    lst_selection += [selection]
    lst_mean += [mean(selection)]


# Построение интервального ряда распределения
min_val = math.floor(min(lst_mean))  # Округление вниз
max_val = math.ceil(max(lst_mean))   # Округление вверх
bins = list(range(int(min_val), int(max_val)+1))
print(len(bins))
print(bins)

# Вычисление частот и относительных частот
hist = [0] * (len(bins) - 1)
for mean_value in lst_mean:
    for i in range(1, len(bins)):
        if bins[i-1] <= mean_value < bins[i]:
            hist[i-1] += 1
            break
print('Частоты: ', hist)
relative_frequencies = [h / len(lst_mean) for h in hist]
print('Относительные частоты: ', relative_frequencies)

n = 36
max_value = max(bins)
min_value = min(bins)

print("Интервал \t Частота \t Относительная частота")
for i in range(len(bins) - 1):
    print(f"{bins[i]} - {bins[i+1]:<10} {hist[i]:<10} {relative_frequencies[i]:<20}")

interval_means = [(bins[i] + bins[i + 1]) / 2 for i in range(len(bins) - 1)]
print("Середины интервалов:", interval_means)

mean_value = sum([(hist[i] * interval_means[i]) for i in range(len(interval_means))]) / n
print("Среднее:", mean_value)

mean_sq = sum([(hist[i] * math.pow(interval_means[i], 2)) for i in range(len(interval_means))]) / n
print("Квадрат среднего:", mean_sq)

variance_value = mean_sq - mean_value**2
print("Дисперсия:", variance_value)

std_dev = math.sqrt(variance_value)
print("СКО:", std_dev)

# Нормированных границ интервалов (z_i) с учетом бесконечности
z_values = [(-math.inf if i == 0 else (bins[i] - mean_value) / std_dev) for i in range(len(interval_means))]
z_values.append(math.inf)  # Добавляем плюс бесконечность для последнего интервала

laplace_values = [stats.norm.cdf(z) - 0.5 for z in z_values]

# Вычисление вероятностей попадания X в интервалы (p_i)
probabilities = [laplace_values[i+1] - laplace_values[i] for i in range(len(laplace_values)-1)]

# Вычисление теоретических частот (n'_i)
theoretical_frequencies = [p * n for p in probabilities]

print()
# Вывод нормированных границ, значений функции Лапласа и вероятностей для каждого интервала
for i in range(len(bins) - 1):
    print(f"({bins[i]}, {bins[i+1]})   z_i = ({z_values[i]:<7.3f}, {z_values[i+1]:<7.3f})   "
          f"Φ(z_i) = {laplace_values[i]:<7.4f}   Φ(z_{i+1}) = {laplace_values[i+1]:<7.4f}   "
          f"p_i = {probabilities[i]:<7.4f}")

print()
print(f"{'Интервал':<10} {'Фактическая частота':<20} {'Теоретическая частота':<20}")
for i in range(len(bins) - 1):
    print(f"({bins[i]}, {bins[i+1]}) \t  {hist[i]:<20} {theoretical_frequencies[i]:<20.4f}")

# Вычисление хи-квадрат по новой формуле
chi_square = sum(((hist[i] - theoretical_frequencies[i]) ** 2 ) / theoretical_frequencies[i] for i in range(len(theoretical_frequencies)))

# Вывод результата
print(f"Значение хи-квадрат (набл): {chi_square:.4f}")
critical_value = stats.chi2.ppf(1 - 0.05, df=len(bins) - 4)
print("Критическое значение χ2: " + str(critical_value))

if chi_square < critical_value:
    print("Принимаем гипотезу")
elif chi_square > critical_value:
    print("Отвергаем гипотезу")