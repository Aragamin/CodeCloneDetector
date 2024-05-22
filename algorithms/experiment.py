import string
import time
import os
from matplotlib import pyplot as plt
from algorithms.ast_find import calculate_plagiarism_percentage
from algorithms.greedy_string_tiling import search_plagiarism
from algorithms.heckel import search_heckel

# Путь к директории с тестовыми примерами
test_examples_dir = os.path.join(os.path.dirname(__file__), '..', 'test_examples')

def load_test_example(example_name):
    example_path = os.path.join(test_examples_dir, example_name)
    with open(example_path, 'r', encoding='utf-8') as file:
        return file.read()

def calc_plagiarism_matrix(find_plagiarism, origin_filename, target_filenames, method_name, test_count=10):
    time_out = open(method_name + '_time.csv', 'w')
    percentage_out = open(method_name + '_percentage.csv', 'w')
    for target_filename in target_filenames:
        percentage = 0.0
        start_time = time.time()
        for _ in range(test_count):
            percentage = find_plagiarism(os.path.join(test_examples_dir, target_filename),
                                         os.path.join(test_examples_dir, origin_filename))
        result_time = (time.time() - start_time) / test_count * 1000
        time_out.write(str(result_time) + '\n')
        percentage_out.write(str(percentage) + '\n')
    time_out.close()
    percentage_out.close()

def merge_data(type):
    with open(f'{type}_results.csv', 'w') as outfile, \
            open(f'greedy_{type}.csv') as greedy, \
            open(f'heckel_{type}.csv') as heckel, \
            open(f'ast_{type}.csv') as ast:
        outfile.write('Тестовые данные,Строковый,Токенизация,AST,Среднее значение\n')
        greedy_string = greedy.readlines()
        heckel_string = heckel.readlines()
        ast_string = ast.readlines()
        for i in range(len(greedy_string)):
            avg_score = (float(greedy_string[i].strip()) + float(heckel_string[i].strip()) + float(ast_string[i].strip())) / 3
            outfile.write(
                f'{i + 1},{greedy_string[i].strip()},{heckel_string[i].strip()},{ast_string[i].strip()},{avg_score}\n')

def plot_results(variant, title, ylabel):
    with open(f'greedy_{variant}.csv') as greedy, \
            open(f'heckel_{variant}.csv') as heckel, \
            open(f'ast_{variant}.csv') as ast:
        greedy_nums = []
        heckel_nums = []
        ast_nums = []
        greedy_string = greedy.readlines()
        heckel_string = heckel.readlines()
        ast_string = ast.readlines()

        # Пропускаем первую строку с заголовками
        for i in range(len(greedy_string)):
            greedy_nums.append(float(greedy_string[i].strip()))
            heckel_nums.append(float(heckel_string[i].strip()))
            ast_nums.append(float(ast_string[i].strip()))

        alphabet = list(string.ascii_uppercase)
        # Создаем график и добавляем кривые
        plt.plot(alphabet[:len(greedy_nums)], greedy_nums, label='Строковый метод')
        plt.plot(alphabet[:len(heckel_nums)], heckel_nums, label='Токенизация', linestyle='--')
        plt.plot(alphabet[:len(ast_nums)], ast_nums, label='AST', linestyle='-.')

        plt.title(title)
        plt.xlabel('Тестовые данные')
        plt.ylabel(ylabel)
        plt.legend()
        plt.savefig(f'{variant}_plot.png')
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
