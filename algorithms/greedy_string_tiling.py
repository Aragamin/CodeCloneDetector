import os

def load_file_content(file_path):
    """Загружает содержимое файла и возвращает его построчно."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return None

def is_marked_match(marked_dict, start, length):
    """Проверяет, является ли данная строка уже частью найденного совпадения."""
    return any(start + i in marked_dict for i in range(length))

def mark_positions(marked_dict, start, length):
    """Помечает строки как совпадающие."""
    for i in range(length):
        marked_dict[start + i] = True

def search_greedy_string_tiling(target_file, origin_file, min_match_length=4):
    """Основная функция для поиска заимствований методом Greedy String Tiling."""
    target_lines = load_file_content(target_file)
    origin_lines = load_file_content(origin_file)

    if target_lines is None or origin_lines is None:
        return None

    tiles = []
    target_marked = {}
    origin_marked = {}
    total_matched_length = 0
    max_match = min_match_length + 1

    while max_match > min_match_length:
        max_match = min_match_length
        matches = []

        for i in range(len(target_lines)):
            for j in range(len(origin_lines)):
                k = 0
                while i + k < len(target_lines) and j + k < len(origin_lines) and \
                        target_lines[i + k].strip() == origin_lines[j + k].strip() and \
                        not is_marked_match(target_marked, i + k, 1) and \
                        not is_marked_match(origin_marked, j + k, 1):
                    k += 1
                if k > max_match:
                    matches = [(i, j, k)]
                    max_match = k
                elif k == max_match:
                    matches.append((i, j, k))

        for match in matches:
            i, j, k = match
            if not is_marked_match(target_marked, i, k) and not is_marked_match(origin_marked, j, k):
                mark_positions(target_marked, i, k)
                mark_positions(origin_marked, j, k)
                tiles.append((i, j, k))
                total_matched_length += sum(len(target_lines[i + n].strip()) for n in range(k))

    # Вычисляем процент совпадения
    total_length = sum(len(line.strip()) for line in target_lines)
    plagiarism_percent = (total_matched_length / total_length) * 100 if total_length > 0 else 0

    return plagiarism_percent

def run_greedy_string_tiling():
    # Получение абсолютного пути к текущему файлу
    current_dir = os.path.dirname(__file__)
    print(f"Текущая директория: {current_dir}")

    # Путь к директории с тестовыми примерами
    test_examples_dir = os.path.join(current_dir, '..', 'test_examples')
    print(f"Путь к директории с тестовыми примерами: {test_examples_dir}")

    # Словарь для хранения результатов
    results = {}

    # Путь к файлам тестовых примеров
    files_to_check = [
        "A_copy_type1_complete.py",
        "B_copy_type2_renamed_variables_33.py",
        "C_copy_type2_renamed_variables_50.py",
        "D_copy_type2_renamed_variables_100.py",
        "E_copy_type3_added_lines.py",
        "F_copy_type3_reordered_lines.py",
        "G_copy_type3_added_and_reordered.py",
        "H_copy_type3_renamed_added_and_reordered.py"
    ]

    origin_file = os.path.join(test_examples_dir, "original_program.py")

    for file_name in files_to_check:
        file_path = os.path.join(test_examples_dir, file_name)
        plagiarism_percent = search_greedy_string_tiling(target_file=file_path, origin_file=origin_file, min_match_length=6)
        if plagiarism_percent is not None:
            results[file_name] = plagiarism_percent
        else:
            results[file_name] = "Ошибка при загрузке файлов."

    # Печать результатов в отсортированном порядке
    for file_name in sorted(results.keys()):
        print(f"Процент плагиата {file_name}: {results[file_name]}%")

if __name__ == "__main__":
    run_greedy_string_tiling()
