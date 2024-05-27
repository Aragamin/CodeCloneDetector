import ast
import os


class ASTComparator(ast.NodeVisitor):
    def __init__(self, tree1, tree2):
        self.tree1 = tree1
        self.tree2 = tree2
        self.mismatches = 0
        self.total = 0

    def compare(self):
        self.visit(self.tree1, self.tree2)
        return self.mismatches == 0

    def visit(self, node1, node2=None):
        self.total += 1
        if node2 is None:
            node2 = self.tree2
        if type(node1) != type(node2):
            self.mismatches += 1
        else:
            for field in node1._fields:
                value1 = getattr(node1, field)
                value2 = getattr(node2, field)
                if isinstance(value1, list) and isinstance(value2, list):
                    for item1, item2 in zip(value1, value2):
                        self.visit(item1, item2)
                elif isinstance(value1, ast.AST) and isinstance(value2, ast.AST):
                    self.visit(value1, value2)
                elif isinstance(value1, (str, int, float)) and isinstance(value2, (str, int, float)):
                    continue
                else:
                    if value1 != value2:
                        self.mismatches += 1


def get_ast_from_file(file_path, encoding="utf-8"):
    """Получает AST из файла."""
    with open(file_path, "r", encoding=encoding) as file:
        code = file.read()
    return ast.parse(code)


def calculate_plagiarism_percentage(target_filename, origin_filename):
    """Вычисляет процент заимствования между двумя файлами."""
    target_ast = get_ast_from_file(target_filename)
    origin_ast = get_ast_from_file(origin_filename)

    comparator = ASTComparator(target_ast, origin_ast)
    is_similar = comparator.compare()
    similarity_ratio = 1 - comparator.mismatches / comparator.total
    return similarity_ratio * 100


if __name__ == "__main__":
    # Частное тестирование алгоритма
    test_examples_dir = os.path.join(os.path.dirname(__file__), '..', 'test_examples')
    file1_path = os.path.join(test_examples_dir, "original_program.py")
    file2_path = os.path.join(test_examples_dir, "C_copy_type2_renamed_variables_50.py")

    plagiarism_percentage = calculate_plagiarism_percentage(file1_path, file2_path)
    print("Процент заимствований между файлами:", plagiarism_percentage, "%")
