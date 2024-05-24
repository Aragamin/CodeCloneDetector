import os
import string
import time
from matplotlib import pyplot as plt
from algorithms.ast_find import calculate_plagiarism_percentage
from algorithms.greedy_string_tiling import search_plagiarism
from algorithms.heckel import search_heckel

# Путь к директории с тестовыми примерами
test_examples_dir = os.path.join(os.path.dirname(__file__), '..', 'test_examples')

# Путь к директории для результатов
results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(results_dir, exist_ok=True)

def load_test_example(example_name):
    example_path = os.path.join(test_examples_dir, example_name)
    with open(example_path, 'r', encoding='utf-8') as file:
        return file.read()

def calc_plagiarism_matrix(find_plagiarism, origin_filename, target_filenames, method_name, test_count=10):
    time_out_path = os.path.join(results_dir, method_name + '_time.csv')
    percentage_out_path = os.path.join(results_dir, method_name + '_percentage.csv')
    with open(time_out_path, 'w') as time_out, open(percentage_out_path, 'w') as percentage_out:
        for target_filename in target_filenames:
            total_percentage = 0.0
            total_time = 0.0
            for _ in range(test_count):
                start_time = time.time()
                percentage = find_plagiarism(os.path.join(test_examples_dir, target_filename),
                                             os.path.join(test_examples_dir, origin_filename))
                total_time += (time.time() - start_time)
                total_percentage += percentage
            avg_percentage = total_percentage / test_count
            avg_time = (total_time / test_count) * 1000
            percentage_out.write(f"{avg_percentage}\n")
            time_out.write(f"{avg_time}\n")

def merge_data(type):
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

def plot_results(variant, title, ylabel):
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
            plt.text(i, g, f'{g:.1f}', ha='center', va='bottom', fontsize=8, color='blue')
            plt.text(i, h, f'{h:.1f}', ha='center', va='bottom', fontsize=8, color='orange')
            plt.text(i, a, f'{a:.1f}', ha='center', va='bottom', fontsize=8, color='green')

        plt.title(title)
        plt.xlabel('Тестовые данные')
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        plot_path = os.path.join(results_dir, f'{variant}_plot.png')
        plt.savefig(plot_path)
        plt.show()

def main():
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
        find_plagiarism=search_plagiarism, origin_filename='original_program.py',
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

if __name__ == '__main__':
    main()
