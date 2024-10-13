import math
from scipy import stats

file_path = "Москва_2021.txt"
with open(file_path, 'r') as file:
    data = file.read().splitlines()
data = list(map(int, data))

# Построение интервальных рядов и расчет характеристик
min_value = 14
max_value = 73

gap = math.ceil((max_value - min_value) / 7)
print('Шаг:', gap)
bins = list(range(min_value, max_value + gap, gap))
print('Границы интервалов:', bins)

a = 0.05

hist = [0] * (len(bins) - 1)
for x in data:
    for i in range(1, len(bins)):
        if bins[i-1] <= x < bins[i]:
            hist[i-1] += 1
            break
print('Частоты:', hist)

relative_frequencies = [h / len(data) for h in hist]
print('Относительные частоты: ', relative_frequencies)

print("Интервал\t Частота\t Относительная частота\t")
for i in range(len(bins) - 1):
    print(f"{bins[i]} - {bins[i+1]:} \t {hist[i]:} \t\t {relative_frequencies[i]}")

gap_means = [(bins[i] + bins[i + 1]) / 2 for i in range(len(bins) - 1)]
print("Середины интервалов:", gap_means)

mean_value = sum([(hist[i] * gap_means[i]) for i in range(len(gap_means))]) / len(data)
print("Среднее:", mean_value)

mean_sq = sum([(hist[i] * gap_means[i] ** 2) for i in range(len(gap_means))]) / len(data)
print("Квадрат среднего:", mean_sq)

variance = mean_sq - mean_value ** 2
print("Дисперсия:", variance)

std_dev = math.sqrt(variance)
print("СКО:", std_dev)

# Нормированных границы интервалов (z_i) с учетом бесконечности
z_values = [(-math.inf if i == 0 else (bins[i] - mean_value) / std_dev) for i in range(len(gap_means))]
z_values.append(math.inf)  # Добавляем + бесконечность для последнего интервала
print(z_values)

# Значения функции Лапласа для нормированных границ
laplace_values = [stats.norm.cdf(z) - 0.5 for z in z_values]

# Вычисление вероятностей попадания X в интервалы (p_i)
probabilities = [laplace_values[i+1] - laplace_values[i] for i in range(len(laplace_values)-1)]

# Вычисление теоретических частот (n'_i)
theoretical_frequencies = [p * len(data) for p in probabilities] # умножения вероятностей на общее количество данных.
print(theoretical_frequencies)

# Вывод нормированных границ, значений функции Лапласа и вероятностей для каждого интервала
print()
for i in range(len(bins) - 1):
    print(f"({bins[i]}, {bins[i+1]})   z_i = ({z_values[i]:<7.3f}, {z_values[i+1]:<7.3f})   "
          f"Φ(z_i) = {laplace_values[i]:<7.4f}   Φ(z_{i+1}) = {laplace_values[i+1]:<7.4f}   "
          f"p_i = {probabilities[i]:<7.4f}")

print()
print(f"{'Интервал':<10} {'Фактическая частота':<20} {'Теоретическая частота':<20}")
for i in range(len(bins) - 1):
    print(f"({bins[i]}, {bins[i+1]})   {hist[i]:<20} {theoretical_frequencies[i]:<20.4f}")

chi_square = sum((hist[i] ** 2) / theoretical_frequencies[i] for i in range(len(theoretical_frequencies))) - sum(hist)

print(f"Значение хи-квадрат (набл): {chi_square:.4f}")
critical_value = stats.chi2.ppf(1 - 0.05, df=len(bins) - 4)
print("Критическое значение χ2: " + str(critical_value))

if chi_square < critical_value:
    print("Принимаем гипотезу")
elif chi_square > critical_value:
    print("Отвергаем гипотезу")