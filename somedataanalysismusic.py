import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import statistics


def calculate_average(column, instrument, category, dataset):
    total = 0
    count = 0

    for row in dataset[1:]:
        if len(row) > column and (category == '' or row[2] == category) and (instrument == '' or row[4] == instrument) and isinstance(row[column], int):
            total += row[column]
            count += 1

    if count > 0:
        return total / count
    else:
        return None


def display_statistics(dataset):
    average_age = calculate_average(0, '', 'performer', dataset)
    average_income = calculate_average(1, '', '', dataset)
    composer_count = sum([1 for row in dataset[1:] if row[2] == 'composer'])
    average_educator_experience = calculate_average(3, '', 'educator', dataset)
    average_income_with_band, average_income_without_band = compare_band_incomes(dataset)

    window = tk.Tk()
    window.title("Statistics")

    tk.Label(window, text="Average Age of Performers:").grid(row=0, column=0, sticky="W")
    tk.Label(window, text=average_age).grid(row=0, column=1)

    tk.Label(window, text="Average Income:").grid(row=1, column=0, sticky="W")
    tk.Label(window, text=average_income).grid(row=1, column=1)

    tk.Label(window, text="Number of Composers:").grid(row=2, column=0, sticky="W")
    tk.Label(window, text=composer_count).grid(row=2, column=1)

    tk.Label(window, text="Average Experience of Educators:").grid(row=3, column=0, sticky="W")
    tk.Label(window, text=average_educator_experience).grid(row=3, column=1)

    tk.Label(window, text="Average Income for those with a Band:").grid(row=4, column=0, sticky="W")
    tk.Label(window, text=average_income_with_band).grid(row=4, column=1)

    tk.Label(window, text="Average Income for those without a Band:").grid(row=5, column=0, sticky="W")
    tk.Label(window, text=average_income_without_band).grid(row=5, column=1)

    compare_button = ttk.Button(window, text="Compare Band Incomes", command=lambda: compare_band_incomes(dataset))
    compare_button.grid(row=6, columnspan=2)

    window.mainloop()

def compare_band_incomes(dataset):
    incomes_with_band = []
    incomes_without_band = []

    for row in dataset[1:]:
        if row[5] == 1 and isinstance(row[1], int):
            incomes_with_band.append(row[1])
        elif row[5] == 0 and isinstance(row[1], int):
            incomes_without_band.append(row[1])

    band_incomes_window = tk.Toplevel()
    band_incomes_window.title("Band Incomes")

    mean_with_band = statistics.mean(incomes_with_band) if incomes_with_band else None
    std_dev_with_band = statistics.stdev(incomes_with_band) if incomes_with_band else None

    mean_without_band = statistics.mean(incomes_without_band) if incomes_without_band else None
    std_dev_without_band = statistics.stdev(incomes_without_band) if incomes_without_band else None

    tk.Label(band_incomes_window, text="With Band:").grid(row=0, column=0, sticky="W")
    tk.Label(band_incomes_window, text="Mean:").grid(row=1, column=0, sticky="E")
    tk.Label(band_incomes_window, text=mean_with_band).grid(row=1, column=1)
    tk.Label(band_incomes_window, text="Standard Deviation:").grid(row=2, column=0, sticky="E")
    tk.Label(band_incomes_window, text=std_dev_with_band).grid(row=2, column=1)

    tk.Label(band_incomes_window, text="Without Band:").grid(row=0, column=2, sticky="W")
    tk.Label(band_incomes_window, text="Mean:").grid(row=1, column=2, sticky="E")
    tk.Label(band_incomes_window, text=mean_without_band).grid(row=1, column=3)
    tk.Label(band_incomes_window, text="Standard Deviation:").grid(row=2, column=2, sticky="E")
    tk.Label(band_incomes_window, text=std_dev_without_band).grid(row=2, column=3)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.hist(incomes_with_band, bins=10, color='blue', alpha=0.7)
    plt.xlabel("Income")
    plt.ylabel("Number of Musicians")
    plt.title("Incomes with Band")

    plt.subplot(1, 2, 2)
    plt.hist(incomes_without_band, bins=10, color='green', alpha=0.7)
    plt.xlabel("Income")
    plt.ylabel("Number of Musicians")
    plt.title("Incomes without Band")

    plt.tight_layout()
    plt.show()

def find_correlations(category1, instrument1, category2, instrument2, dataset):
    data1 = []
    data2 = []

    for row in dataset[1:]:
        if (category1 == '' or row[2] == category1) and (instrument1 == '' or row[4] == instrument1) and isinstance(row[1], int):
            data1.append(row[1])
        if (category2 == '' or row[2] == category2) and (instrument2 == '' or row[4] == instrument2) and isinstance(row[1], int):
            data2.append(row[1])

    correlation = calculate_correlation(data1, data2)
    return correlation

def calculate_correlation(data1, data2):
    if len(data1) != len(data2):
        return None

    n = len(data1)
    sum_x = sum(data1)
    sum_y = sum(data2)
    sum_xy = sum([data1[i] * data2[i] for i in range(n)])
    sum_x_sq = sum([x ** 2 for x in data1])
    sum_y_sq = sum([y ** 2 for y in data2])

    numerator = (n * sum_xy) - (sum_x * sum_y)
    denominator = ((n * sum_x_sq - (sum_x ** 2)) ** 0.5) * ((n * sum_y_sq - (sum_y ** 2)) ** 0.5)

    correlation = numerator / denominator
    return correlation


dataset = [['age', 'income', 'title', 'experience', 'instrument', 'band'], 
[40, 40840, 'performer', 13, 'guitar', 1], [54, 21689, 'composer', 11, 'voice', 1], [37, 43153, 'composer', 28, 'piano', 0], [47, 58113, 'composer', 31, 'violin', 0], [52, 24518, 'producer', 13, 'guitar', 1], [52, 43574, 'composer', 27, 'drums', 1], [58, 27637, 'performer', 9, 'violin', 1], [57, 25707, 'performer', 8, 'piano', 1], [37, 26169, 'composer', 8, 'piano', 0], [28, 30852, 'educator', 9, 'guitar', 1], [65, 48403, 'composer', 22, 'guitar', 1], [51, 40874, 'educator', 15, 'guitar', 0], [49, 29925, 'performer', 9, 'piano', 1], [37, 20350, 'manager', 9, 'voice', 1], [38, 25049, 'performer', 17, 'drums', 1], [41, 33209, 'producer', 29, 'voice', 1], [37, 35711, 'performer', 14, 'piano', 0], [40, 61691, 'performer', 28, 'saxophone', 1], [43, 24854, 'performer', 6, 'voice', 1], [57, 24583, 'performer', 31, 'drums', 0], [39, 45258, 'performer', 24, 'violin', 1], [39, 36205, 'performer', 15, 'guitar', 1], [29, 33473, 'performer', 13, 'piano', 1], [47, 24387, 'performer', 13, 'guitar', 0], [50, 51984, 'performer', 23, 'guitar', 1], [33, 51034, 'producer', 30, 'voice', 0], [44, 25734, 'educator', 15, 'guitar', 1], [37, 33425, 'manager', 10, 'voice', 1], [41, 33206, 'producer', 16, 'drums', 1], [48, 41256, 'performer', 26, 'voice', 0], [38, 36601, 'educator', 25, 'voice', 0], [39, 49320, 'performer', 23, 'piano', 1], [43, 33309, 'performer', 12, 'voice', 1], [37, 18990, 'educator', 4, 'guitar', 1], [53, 24624, 'performer', 1, 'drums', 1], [56, 70057, 'composer', 31, 'piano', 0], [46, 40902, 'performer', 7, 'drums', 1], [33, 33338, 'performer', 8, 'guitar', 1], [35, 20356, 'manager', 6, 'piano', 1], [32, 29609, 'producer', 11, 'voice', 1], [55, 30095, 'educator', 23, 'drums', 1], [44, 35895, 'composer', 11, 'piano', 1], [55, 29730, 'performer', 9, 'drums', 1], [44, 33757, 'composer', 15, 'piano', 1], [32, 40882, 'performer', 15, 'voice', 0], [39, 32086, 'educator', 9, 'drums', 1], [34, 41498, 'composer', 14, 'guitar', 1], [47, 45242, 'educator', 16, 'voice', 1], [41, 20724, 'performer', 5, 'piano', 1], [22, 39822, 'composer', 17, 'piano', 1], [31, 45467, 'performer', 12, 'voice', 1], [55, 29886, 'performer', 10, 'drums', 1], [34, 35558, 'composer', 11, 'voice', 0], [49, 27715, 'educator', 7, 'guitar', 1], [46, 36945, 'performer', 17, 'guitar', 1], [45, 30362, 'educator', 18, 'guitar', 1], [59, 36526, 'educator', 28, 'voice', 0], [59, 42186, 'composer', 17, 'voice', 1], [52, 60303, 'performer', 42, 'piano', 0], [34, 37642, 'producer', 12, 'voice', 1], [32, 36687, 'producer', 27, 'violin', 1], [39, 48350, 'performer', 40, 'guitar', 1], [39, 27173, 'performer', 12, 'voice', 1], [54, 31991, 'performer', 11, 'voice', 1], [34, 22114, 'performer', 9, 'piano', 1], [66, 25016, 'composer', 22, 'guitar', 1], [53, 22514, 'performer', 3, 'voice', 1], [23, 21079, 'educator', 25, 'drums', 0], [28, 21473, 'performer', 17, 'guitar', 1], [43, 33086, 'educator', 29, 'drums', 0], [51, 21535, 'performer', 9, 'voice', 1], [35, 31174, 'producer', 12, 'drums', 1], [66, 53876, 'performer', 26, 'voice', 0], [40, 30367, 'composer', 27, 'voice', 0], [45, 34015, 'performer', 29, 'voice', 0], [50, 16583, 'educator', 5, 'drums', 1], [36, 37421, 'educator', 10, 'drums', 1], [26, 18467, 'performer', 3, 'voice', 1], [41, 33011, 'performer', 28, 'drums', 0], [28, 34084, 'composer', 15, 'saxophone', 1], [43, 39797, 'manager', 19, 'voice', 1], [48, 63969, 'educator', 33, 'piano', 0], [37, 43700, 'performer', 14, 'voice', 1], [35, 37162, 'educator', 17, 'voice', 1], [31, 25220, 'performer', 16, 'drums', 1], [37, 31216, 'producer', 30, 'guitar', 1], [49, 29417, 'educator', 17, 'piano', 1], [58, 51682, 'performer', 25, 'guitar', 0], [38, 30383, 'performer', 13, 'guitar', 0], [38, 45996, 'producer', 16, 'guitar', 1], [29, 29576, 'performer', 13, 'guitar', 1], [35, 63889, 'manager', 36, 'guitar', 0],
 [50, 54892, 'performer', 39, 'piano', 0], [30, 71131, 'performer', 45, 'drums', 0],
 [31, 42709, 'performer', 19, 'drums', 0], [44, 34082, 'educator', 19, 'drums', 1],
 [32, 40700, 'performer', 34, 'voice', 1], [40, 61084, 'performer', 38, 'voice', 0],

 [53, 22003, 'performer', 15, 'drums', 1], [56, 35558, 'composer', 30, 'piano', 0]]


display_statistics(dataset)

correlation_performer_income = find_correlations('performer', 'guitar', 'composer', 'piano', dataset)
print("\nCorrelation between Performer's Income (Playing Guitar) and Composer's Income (Playing Piano):", correlation_performer_income)

correlation_educator_experience = find_correlations('educator', '', 'performer', 'guitar', dataset)
print("Correlation between Educator's Income and Performer's Income (Playing Guitar):", correlation_educator_experience)
