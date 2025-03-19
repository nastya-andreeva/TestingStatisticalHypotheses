from scipy import stats
import numpy as np

file_path = "Москва_2021.txt"
with open(file_path, 'r') as file:
    data = file.read().splitlines()
data = list(map(int, data))

n = 62

n_selection = 36
lst_selection = []

for _ in range(n_selection):
    selection = list(np.random.choice(data, size=n, replace=True))
    lst_selection += [selection]


sample_1 = lst_selection[5]
sample_2 = lst_selection[16]

s1_squared = np.var(sample_1, ddof=1)
s2_squared = np.var(sample_2, ddof=1)

# Вычисление F-критерия
F = s1_squared / s2_squared if s1_squared > s2_squared else s2_squared / s1_squared

# Уровень значимости
alpha = 0.05

# Степени свободы
n1 = len(sample_1)
n2 = len(sample_2)
dof1 = n1 - 1
dof2 = n2 - 1
# Критическое значение F-критерия (для односторонней проверки)
F_critical = 1.53
F_critical_leftd = stats.f.ppf(1 - alpha, dof1, dof2)
# Вывод результатов
print(f"Дисперсия выборки 1: {s1_squared}")
print(f"Дисперсия выборки 2: {s2_squared}")
print(f"Значение F-критерия: {F}")
print(f"Критическое значение F-критерия: {F_critical}")

# Проверка гипотезы
if F > F_critical:
    print("Нулевая гипотеза отвергается")
else:
    print("Нулевая гипотеза принимается")
print()

# Уровень значимости
alpha = 0.05

# Степени свободы
dof1 = n1 - 1
dof2 = n2 - 1

# Критические значения для двусторонней проверки
F_critical_left = stats.f.ppf(alpha / 2, dof1, dof2)  # Левая граница
F_critical_right = stats.f.ppf(1 - alpha / 2, dof1, dof2)  # Правая граница

# Вывод результатов
print(f"Дисперсия выборки 1: {s1_squared}")
print(f"Дисперсия выборки 2: {s2_squared}")
print(f"Значение F-критерия: {F}")
print(f"Левая критическая точка: {F_critical_left}")
print(f"Правая критическая точка: {F_critical_right}")

# Проверка гипотезы
if F < F_critical_left or F > F_critical_right:
    print("Нулевая гипотеза отвергается")
else:
    print("Нулевая гипотеза принимается")