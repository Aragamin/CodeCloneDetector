import ast
import difflib
import os

def get_ast_from_file(file_path, encoding="utf-8"):
    """Получает AST из файла."""
    with open(file_path, "r", encoding=encoding) as file:
        code = file.read()
    return ast.parse(code)

def compare_ast(ast1, ast2):
    """Сравнивает два AST и возвращает коэффициент схожести."""
    ast1_str = ast.dump(ast1)
    ast2_str = ast.dump(ast2)

    matcher = difflib.SequenceMatcher(None, ast1_str, ast2_str)
    similarity_ratio = matcher.ratio()

    return similarity_ratio

def calculate_plagiarism_percentage(target_filename, origin_filename):
    """Вычисляет процент заимствования между двумя файлами."""
    target_ast = get_ast_from_file(target_filename)
    origin_ast = get_ast_from_file(origin_filename)
    similarity_ratio = compare_ast(origin_ast, target_ast)
    return similarity_ratio * 100

if __name__ == "__main__":
    # Частное тестирование алгоритма
    test_examples_dir = os.path.join(os.path.dirname(__file__), '..', 'test_examples')
    file1_path = os.path.join(test_examples_dir, "original_program.py")
    file2_path = os.path.join(test_examples_dir, "C_copy_type2_renamed_variables_50.py")

    plagiarism_percentage = calculate_plagiarism_percentage(file1_path, file2_path)
    print("Процент заимствований между файлами:", plagiarism_percentage, "%")
