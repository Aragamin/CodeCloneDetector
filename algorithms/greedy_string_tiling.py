import os

def load_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return None

def is_marked_match(marked_string_dict, begin, length):
    return any(begin + i in marked_string_dict for i in range(length))

def search_plagiarism(target_file, origin_file, min_match_len=4):
    target_lines = load_file_content(target_file)
    origin_lines = load_file_content(origin_file)

    if target_lines is None or origin_lines is None:
        return None

    tiles = []
    matches = []
    max_match = min_match_len + 1
    source_marked = {}
    search_marked = {}
    while max_match > min_match_len:
        max_match = min_match_len
        for p in range(len(target_lines)):
            for t in range(len(origin_lines)):
                j = 0
                while p + j < len(target_lines) and t + j < len(origin_lines) and \
                        target_lines[p + j] == origin_lines[t + j] and p + j not in source_marked and \
                        t + j not in search_marked:
                    j += 1
                if j == max_match:
                    matches.append({"p": p, "t": t, "j": j})
                if j > max_match:
                    matches = [{"p": p, "t": t, "j": j}]
                    max_match = j
        for match in matches:
            if not is_marked_match(source_marked, match["p"], match["j"]) and \
                    not is_marked_match(search_marked, match["t"], match["j"]):
                for k in range(match["j"]):
                    source_marked[match["p"] + k] = True
                    search_marked[match["t"] + k] = True
                tiles.append(target_lines[match["p"]:match["p"] + match["j"]])
    # Вычисляем процент совпадения
    total_len = sum(len(line) for line in target_lines)
    plagiarism_len = sum(len("".join(tile)) for tile in tiles)
    plagiarism_percent = (plagiarism_len / total_len) * 100 if total_len > 0 else 0

    return plagiarism_percent

if __name__ == "__main__":
    test_examples_dir = os.path.join(os.path.dirname(__file__), '..', 'test_examples')
    file1_path = os.path.join(test_examples_dir, "original_program.py")
    file2_path = os.path.join(test_examples_dir, "F_copy_type3_reordered_lines.py")

    plagiarism_percent = search_plagiarism(target_file=file2_path, origin_file=file1_path, min_match_len=6)  # Увеличено значение min_match_len
    if plagiarism_percent is not None:
        print(f"Процент плагиата: {plagiarism_percent}%")
    else:
        print("Не удалось вычислить процент плагиата из-за ошибки при загрузке файлов.")

