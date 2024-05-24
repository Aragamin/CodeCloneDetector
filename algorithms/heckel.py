from abc import ABC, abstractmethod
import re
from operator import attrgetter

# Класс, представляющий токен
class Token:
    def __init__(self, symbol, start, end):
        self.__symbol = symbol
        self.__start = start
        self.__end = end

    @property
    def symbol(self):
        return self.__symbol

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @staticmethod
    def get_tokens_str_from_token_list(token_list):
        token_str = ""
        for token in sorted(token_list, key=lambda tok: tok.start):
            token_str += token.symbol
        return token_str

    @staticmethod
    def find_border_tokens_str_in_token_list(token_list, token_str):
        for i in range(len(token_list)):
            j = 0
            while j < len(token_str) and i + j < len(token_list) and token_list[i + j].symbol == token_str[j]:
                j += 1
            if j == len(token_str):
                return token_list[i].start, token_list[i + j - 1].end
            i += 1
        return None

# Абстрактный класс для токенизации Python кода
class PythonTokenizer(ABC):
    BORDER = "$"
    NOT_TOKEN = "."  # Используется при токенизации, не является конечным токеном
    SUBSTITUTE = "1"  # Используется для замены строковых и символьных констант в тексте программы
    TOKENS = {
        "call": "C",  # - Call - вызов функции
        "assign": "A",  # - Assign - присваивание
        "func": "F",  # - Function - определение функции
        "math": "M",  # - Math - математические операторы + инкремент и декремент
        "return": "R",  # - Return - возврат значения из функции
        "if": "I",  # - If - условные конструкции
        "cycle": "S",  # - Series - циклы
        "compare": "E",  # - сравнения
        "logic": "L",  # - Logic - логические операции
        "control": "G",  # - Governance - управляющие конструкции
        "decorator": "D",  # - Decorator - декораторы функций
        "import": "I",  # - Import - импорт модулей
        "docstring": "DS"  # - Docstring - строка документации
    }

    # Метод токенизации исходного кода
    def tokenize(self, src):
        src_with_replace_import = self.replace_import(src)
        src_with_replace_comments = self.replace_comments(src_with_replace_import)
        src_with_replace_docstrings = self.replace_docstrings(src_with_replace_comments)
        tokens = self._process(src_with_replace_docstrings)
        return tokens

    # Замена комментариев
    @staticmethod
    def replace_comments(src):
        comment_tokens = PythonTokenizer.search_tokens(src, r'#.*', "control")
        src = PythonTokenizer.replace_tokens_in_src(src, comment_tokens, " ")
        return src

    # Замена импортов
    @staticmethod
    def replace_import(src):
        import_tokens = PythonTokenizer.search_tokens(src, r'^\s*import\s+[\w.]+', "import", re.MULTILINE)
        import_tokens += PythonTokenizer.search_tokens(src, r'^\s*from\s+[\w.]+\s+import\s+[\w., ]+', "import", re.MULTILINE)
        src = PythonTokenizer.replace_tokens_in_src(src, import_tokens, " ")
        return src

    # Замена строк документации
    @staticmethod
    def replace_docstrings(src):
        docstring_tokens = PythonTokenizer.search_tokens(src, r'""".*?"""', "docstring", re.DOTALL)
        docstring_tokens += PythonTokenizer.search_tokens(src, r"'''.*?'''", "docstring", re.DOTALL)
        src = PythonTokenizer.replace_tokens_in_src(src, docstring_tokens, PythonTokenizer.SUBSTITUTE)
        return src

    # Обработка исходного кода для токенизации
    def _process(self, src):
        tokens = []

        # Замена символьных и строковых констант
        src = PythonTokenizer.replace_strings(src)

        # Токенизация декораторов
        decorator_tokens = PythonTokenizer.search_tokens(src, r'^\s*@\w+', "decorator", re.MULTILINE)
        src = PythonTokenizer.replace_tokens_in_src(src, decorator_tokens, " ")
        tokens += decorator_tokens

        # Токенизация циклов
        cycle_tokens = PythonTokenizer.search_tokens(src, r'\b(for|while)\b\s*\(.*?\)\s*:', "cycle")
        src = PythonTokenizer.replace_tokens_in_src(src, cycle_tokens)
        tokens += cycle_tokens
        tokens += PythonTokenizer.search_tokens(src, r'\bfor\b', "cycle")
        while_from_do_tokens = PythonTokenizer.search_tokens(src, r'while\s*\(.*?\)\s*:', "cycle")
        src = PythonTokenizer.replace_tokens_in_src(src, while_from_do_tokens)

        # Токенизация условных конструкций
        if_else_tokens = PythonTokenizer.search_tokens(src, r'\b(if|elif)\s*\(.*?\)\s*:', "if")
        src = PythonTokenizer.replace_tokens_in_src(src, if_else_tokens)
        tokens += if_else_tokens
        tokens += PythonTokenizer.search_tokens(src, r'\belse\b\s*:', "if")

        # Токенизация определения функции
        function_tokens = PythonTokenizer.search_tokens(src, r'def\s+\w+\s*\(.*?\)\s*:', "func")
        src = PythonTokenizer.replace_tokens_in_src(src, function_tokens)
        tokens += function_tokens

        # Токенизация вызова функции
        call_tokens = []
        for match in re.finditer(r'(\w+)\s*\(.*?\)', src, flags=re.ASCII):
            call_tokens.append(Token(PythonTokenizer.TOKENS["call"], match.start(1), match.end(1) + 1))
        src = PythonTokenizer.replace_tokens_in_src(src, call_tokens, is_full_replace=False)
        tokens += call_tokens

        # Токенизация логических операций
        tokens += PythonTokenizer.search_tokens(src, r'and|or|not', "logic")

        # Токенизация сравнений
        tokens += PythonTokenizer.search_tokens(src, r'==|!=|<=|>=|<|>', "compare")

        # Токенизация присваивания
        assign_tokens = PythonTokenizer.search_tokens(src, r'=', "assign")
        src = PythonTokenizer.replace_tokens_in_src(src, assign_tokens)
        tokens += assign_tokens

        # Токенизация математических выражений
        tokens += PythonTokenizer.search_tokens(src, r'\+\+|--|\+|-|\*|/|%', "math")

        # Токенизация управляющих конструкций
        tokens += PythonTokenizer.search_tokens(src, r'\bcontinue\b|\bbreak\b|\bpass\b|\breturn\b', "control")

        return sorted(tokens, key=attrgetter('start', 'end'))

    # Поиск токенов
    @staticmethod
    def search_tokens(src, pattern, token_key, flags=re.ASCII):
        tokens = []
        for match in re.finditer(pattern, src, flags=flags):
            tokens.append(Token(PythonTokenizer.TOKENS[token_key], match.start(), match.end()))
        return tokens

    # Замена токенов в исходном коде
    @staticmethod
    def replace_tokens_in_src(src, tokens, replace=".", is_full_replace=True):
        for token in tokens:
            if is_full_replace is True:
                src = src[:token.start] + replace * (token.end - token.start) + src[token.end:]
            else:
                src = src[:token.start] + replace * (token.end - token.start - 1) + src[token.end - 1:]
        return src

    # Замена строковых констант
    @staticmethod
    def replace_strings(src):
        strings_tokens = PythonTokenizer.search_tokens(src, r'"[^"\n]*"', "control")
        strings_tokens += PythonTokenizer.search_tokens(src, r"'[^'\n]*'", "control")
        src = PythonTokenizer.replace_tokens_in_src(src, strings_tokens, PythonTokenizer.SUBSTITUTE)
        return src

# Функция для поиска заимствований методом Хеккеля
def search_heckel(target_filename, origin_filename, length_n_gramm=4):
    with open(origin_filename, encoding='utf-8') as origin_file, open(target_filename, encoding='utf-8') as target_file:
        tokenizer = PythonTokenizer()
        origin_tokens = Token.get_tokens_str_from_token_list(tokenizer.tokenize(origin_file.read()))
        target_tokens = Token.get_tokens_str_from_token_list(tokenizer.tokenize(target_file.read()))
    origin_n_gramms = split_into_n_gramms(origin_tokens, length_n_gramm)
    target_n_gramms = split_into_n_gramms(target_tokens, length_n_gramm)
    return round(len(origin_n_gramms & target_n_gramms) / len(origin_n_gramms | target_n_gramms) * 100)

# Функция для разбиения строки токенов на n-граммы
def split_into_n_gramms(token_str, length_n_gramm):
    if length_n_gramm <= 0:
        return set()
    n_gramms = []
    for i in range(len(token_str) - length_n_gramm + 1):
        n_gramms.append(token_str[i:i + length_n_gramm])
    return set(n_gramms)

# Тестирование функции
if __name__ == "__main__":
    file1_path = "../test_examples/original_program.py"
    file2_path = "../test_examples/F_copy_type3_reordered_lines.py"

    plagiarism_percentage = search_heckel(target_filename=file2_path, origin_filename=file1_path)
    print("Процент заимствований между файлами:", plagiarism_percentage, "%")

