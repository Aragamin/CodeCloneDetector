import os
import string
import time
from matplotlib import pyplot as plt
from ast_find import calculate_plagiarism_percentage
from greedy_string_tiling import search_greedy_string_tiling
from heckel import search_heckel
import numpy as np

# Путь к директории с тестовыми примерами
test_examples_dir = os.path.join(os.path.dirname(__file__), '..', 'test_examples')

# Путь к директории для результатов
results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(results_dir, exist_ok=True)

def load_test_example(example_name):
    """Загружает тестовый пример из файла."""
    example_path = os.path.join(test_examples_dir, example_name)
    with open(example_path, 'r', encoding='utf-8') as file:
        return file.read()

def calc_plagiarism_matrix(find_plagiarism, origin_filename, target_filenames, method_name, test_count=10):
    """
    Вычисляет матрицу плагиата для заданного метода.
    Сохраняет время выполнения и процент совпадений в соответствующие файлы.
    """
    time_out_path = os.path.join(results_dir, method_name + '_time.csv')
    percentage_out_path = os.path.join(results_dir, method_name + '_percentage.csv')
    with open(time_out_path, 'w') as time_out, open(percentage_out_path, 'w') as percentage_out:
        for target_filename in target_filenames:
            total_percentage = 0.0
            total_time = 0.0
            for _ in range(test_count):
                start_time = time.time()
                # Для метода GST используется дополнительный аргумент min_match_length
                if method_name == 'greedy':
                    percentage = find_plagiarism(os.path.join(test_examples_dir, target_filename),
                                                 os.path.join(test_examples_dir, origin_filename),
                                                 min_match_length=6)
                else:
                    percentage = find_plagiarism(os.path.join(test_examples_dir, target_filename),
                                                 os.path.join(test_examples_dir, origin_filename))
                total_time += (time.time() - start_time)
                total_percentage += percentage
            avg_percentage = total_percentage / test_count
            avg_time = (total_time / test_count) * 1000
            percentage_out.write(f"{avg_percentage}\n")
            time_out.write(f"{avg_time}\n")

def merge_data(type):
    """
    Объединяет данные из трех методов в один файл.
    Считает среднее значение для каждого тестового примера.
    """
    results_file = os.path.join(results_dir, f'{type}_results.csv')
    greedy_file = os.path.join(results_dir, f'greedy_{type}.csv')
    heckel_file = os.path.join(results_dir, f'heckel_{type}.csv')
    ast_file = os.path.join(results_dir, f'ast_{type}.csv')

    with open(results_file, 'w') as outfile, \
            open(greedy_file) as greedy, \
            open(heckel_file) as heckel, \
            open(ast_file) as ast:
        outfile.write('Тестовые данные,Строковый,Токенизация,AST,Среднее значение\n')
        greedy_data = [float(line.strip()) for line in greedy]
        heckel_data = [float(line.strip()) for line in heckel]
        ast_data = [float(line.strip()) for line in ast]
        for i in range(len(greedy_data)):
            avg_score = (greedy_data[i] + heckel_data[i] + ast_data[i]) / 3
            outfile.write(
                f'{string.ascii_uppercase[i]},{greedy_data[i]},{heckel_data[i]},{ast_data[i]},{avg_score}\n')

def plot_results0(variant, title, ylabel):
    """
    Строит графики результатов для времени выполнения и процента совпадений.
    """
    greedy_file = os.path.join(results_dir, f'greedy_{variant}.csv')
    heckel_file = os.path.join(results_dir, f'heckel_{variant}.csv')
    ast_file = os.path.join(results_dir, f'ast_{variant}.csv')

    with open(greedy_file) as greedy, \
            open(heckel_file) as heckel, \
            open(ast_file) as ast:
        greedy_nums = []
        heckel_nums = []
        ast_nums = []
        greedy_lines = greedy.readlines()
        heckel_lines = heckel.readlines()
        ast_lines = ast.readlines()

        for line in greedy_lines:
            greedy_nums.append(float(line.strip()))
        for line in heckel_lines:
            heckel_nums.append(float(line.strip()))
        for line in ast_lines:
            ast_nums.append(float(line.strip()))

        alphabet = list(string.ascii_uppercase)
        plt.plot(alphabet[:len(greedy_nums)], greedy_nums, label='Строковый метод', marker='o')
        plt.plot(alphabet[:len(heckel_nums)], heckel_nums, label='Токенизация', linestyle='--', marker='s')
        plt.plot(alphabet[:len(ast_nums)], ast_nums, label='AST', linestyle='-.', marker='^')

        for i, (g, h, a) in enumerate(zip(greedy_nums, heckel_nums, ast_nums)):
            plt.text(i, g, f'{g:.1f}', ha='center', va='bottom', fontsize=10, color='blue')
            plt.text(i, h, f'{h:.1f}', ha='center', va='bottom', fontsize=10, color='orange')
            plt.text(i, a, f'{a:.1f}', ha='center', va='bottom', fontsize=10, color='green')

        plt.title(title)
        plt.xlabel('Тестовые данные')
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        plot_path = os.path.join(results_dir, f'{variant}_plot.png')
        plt.savefig(plot_path)
        plt.show()

def plot_results(variant, title, ylabel):
    """
    Строит графики результатов для времени выполнения и процента совпадений.
    """
    greedy_file = os.path.join(results_dir, f'greedy_{variant}.csv')
    heckel_file = os.path.join(results_dir, f'heckel_{variant}.csv')
    ast_file = os.path.join(results_dir, f'ast_{variant}.csv')

    with open(greedy_file) as greedy, \
            open(heckel_file) as heckel, \
            open(ast_file) as ast:
        greedy_nums = []
        heckel_nums = []
        ast_nums = []
        greedy_lines = greedy.readlines()
        heckel_lines = heckel.readlines()
        ast_lines = ast.readlines()

        for line in greedy_lines:
            greedy_nums.append(float(line.strip()))
        for line in heckel_lines:
            heckel_nums.append(float(line.strip()))
        for line in ast_lines:
            ast_nums.append(float(line.strip()))

        alphabet = list(string.ascii_uppercase)
        x = np.arange(len(greedy_nums))  # индекс для x координаты
        bar_width = 0.25

        plt.figure(figsize=(10, 6))
        plt.bar(x - bar_width, greedy_nums, width=bar_width, label='Строковый метод', color='blue')
        plt.bar(x, heckel_nums, width=bar_width, label='Токенизация', color='orange')
        plt.bar(x + bar_width, ast_nums, width=bar_width, label='AST', color='green')

        for i, (g, h, a) in enumerate(zip(greedy_nums, heckel_nums, ast_nums)):
            plt.text(i - bar_width, g, f'{g:.1f}', ha='center', va='bottom', fontsize=10, bbox=dict(facecolor='white', alpha=0.7))
            plt.text(i, h, f'{h:.1f}', ha='center', va='bottom', fontsize=10, bbox=dict(facecolor='white', alpha=0.7))
            plt.text(i + bar_width, a, f'{a:.1f}', ha='center', va='bottom', fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

        plt.title(title, fontsize=16)
        plt.xlabel('Тестовые данные', fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        plt.xticks(x, alphabet[:len(greedy_nums)], fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)

        # Настройка положения легенды
        if variant == 'time':
            plt.legend(fontsize=12, loc='upper left', bbox_to_anchor=(0, 1), borderaxespad=0., frameon=True, edgecolor='black')
        elif variant == 'percentage':
            plt.legend(fontsize=12, loc='lower left', bbox_to_anchor=(0, 0), borderaxespad=0., frameon=True, edgecolor='black')

        plt.tight_layout()
        plot_path = os.path.join(results_dir, f'{variant}_plot.png')
        plt.savefig(plot_path, dpi=300)
        plt.show()




def main():
    """
    Основная функция, выполняющая тестирование и построение графиков.
    """
    target_filenames = [
        'A_copy_type1_complete.py',
        'B_copy_type2_renamed_variables_33.py',
        'C_copy_type2_renamed_variables_50.py',
        'D_copy_type2_renamed_variables_100.py',
        'E_copy_type3_added_lines.py',
        'F_copy_type3_reordered_lines.py',
        'G_copy_type3_added_and_reordered.py',
        'H_copy_type3_renamed_added_and_reordered.py'
    ]

    calc_plagiarism_matrix(
        find_plagiarism=calculate_plagiarism_percentage, origin_filename='original_program.py',
        target_filenames=target_filenames, method_name='ast',
    )
    calc_plagiarism_matrix(
        find_plagiarism=search_greedy_string_tiling, origin_filename='original_program.py',
        target_filenames=target_filenames, method_name='greedy',
    )
    calc_plagiarism_matrix(
        find_plagiarism=search_heckel, origin_filename='original_program.py',
        target_filenames=target_filenames, method_name='heckel',
    )

    merge_data('time')
    merge_data('percentage')

    plot_results('time', 'Сравнение времени выполнения', 'Время выполнения, мс')
    plot_results('percentage', 'Сравнение процентного заимствования', 'Процент заимствования, %')

    # Вывод средних значений по времени и проценту заимствований
    print_average_results()

def print_average_results():
    """
    Выводит средние значения по времени выполнения и проценту заимствований для каждого метода.
    """
    time_files = {
        'Строковый метод': 'greedy_time.csv',
        'Токенизация': 'heckel_time.csv',
        'AST': 'ast_time.csv'
    }
    percentage_files = {
        'Строковый метод': 'greedy_percentage.csv',
        'Токенизация': 'heckel_percentage.csv',
        'AST': 'ast_percentage.csv'
    }

    for method, filename in time_files.items():
        with open(os.path.join(results_dir, filename)) as file:
            times = [float(line.strip()) for line in file]
            avg_time = sum(times) / len(times)
            print(f"Среднее время выполнения для {method}: {avg_time:.2f} мс")

    for method, filename in percentage_files.items():
        with open(os.path.join(results_dir, filename)) as file:
            percentages = [float(line.strip()) for line in file]
            avg_percentage = sum(percentages) / len(percentages)
            print(f"Средний процент заимствований для {method}: {avg_percentage:.2f} %")

if __name__ == '__main__':
    main()
