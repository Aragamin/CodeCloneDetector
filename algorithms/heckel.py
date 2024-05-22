from abc import ABC, abstractmethod
import re
from operator import attrgetter


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


class PythonTokenizer(ABC):
    INT_TYPES = "|".join(["unsigned long long int", "unsigned long long", "unsigned long int", "unsigned long",
                          "unsigned int", "unsigned short int", "unsigned short", "unsigned", "signed long long int",
                          "signed long long", "signed long int", "signed long", "signed short int", "signed short",
                          "signed int", "signed", "long long int", "long long", "long int", "long", "short int",
                          "short", "int"])
    CHAR_TYPES = "|".join(["signed char", "unsigned char", "char"])
    FLOAT_TYPES = "|".join(["long double", "double", "float"])
    BORDER = "$"
    NOT_TOKEN = "."  # Используется при токенизации, не является конечным токеном
    SUBSTITUTE = "1"  # Используется для замены строковых и символьных констант в тексте программы
    TOKENS = {
        "int": "N",  # - Number - целое число
        "double": "D",  # - Double - дробное число
        "char": "B",  # - Byte - однобайтовый тип (char)
        "ptr": "P",  # - Pointer - указатель
        "call": "C",  # - Call - вызов функции
        "assign": "A",  # - Assign - присваивание
        "func": "F",  # - Function - определение функции
        "cast": "T",  # - Type - приведение типов
        "math": "M",  # - Math - математические операторы + инкремент и декремент
        "return": "R",  # - Return - возврат значения из функции
        "if": "I",  # - If - условные конструкции
        "cycle": "S",  # - Series - циклы
        "compare": "E",  # - сравнения
        "logic": "L",  # - Logic - логические операции
        "shift": "U",  # - Upheaval - побитовые операции сдвига
        "control": "G",  # - Governance - управляющие конструкции
        "struct": "V",  # - Var - структуры
    }

    def tokenize(self, src):
        src_with_replace_import = self.replace_import(src)
        src_with_replace_comments = self.replace_comments(src_with_replace_import)
        tokens = self._process(src_with_replace_comments)
        return tokens

    @staticmethod
    def replace_comments(src):
        comment_tokens = PythonTokenizer.search_tokens(src, r'//[^\n]*(\n|$)', "control", re.MULTILINE)
        src = PythonTokenizer.replace_tokens_in_src(src, comment_tokens, " ")
        comment_tokens = PythonTokenizer.search_tokens(src, r'/\*.*?\*/', "control", re.DOTALL)
        src = PythonTokenizer.replace_tokens_in_src(src, comment_tokens, " ")
        return src

    @staticmethod
    def replace_import(src):
        import_tokens = PythonTokenizer.search_tokens(src, r'#\s*include\s*[<"][^<>"]+[>"]', "control", re.DOTALL)
        src = PythonTokenizer.replace_tokens_in_src(src, import_tokens, " ")
        return src

    @staticmethod
    def replace_strings(src):
        strings_tokens = PythonTokenizer.search_tokens(src, r'"[^\n"]+"', "control")
        strings_tokens += PythonTokenizer.search_tokens(src, r"'[^\n']+'", "control")
        src = PythonTokenizer.replace_tokens_in_src(src, strings_tokens, PythonTokenizer.SUBSTITUTE)
        return src

    @staticmethod
    def replace_macros(src):
        macros_tokens = PythonTokenizer.search_tokens(src, r"#\s*define\s*[^\n]*", "control")
        src = PythonTokenizer.replace_tokens_in_src(src, macros_tokens, " ")
        return src

    def _process(self, src):
        tokens = []

        # Замена символьных и строковых констант, например, чтобы ';' - не вносило ошибки в токенизацию
        src = PythonTokenizer.replace_strings(src)

        # Замена директив #define
        src = PythonTokenizer.replace_macros(src)

        # Токенизация тернарного оператора
        ternary_tokens, src = PythonTokenizer.get_tokens_ternary_operator(src)
        tokens += ternary_tokens

        # Токенизация указателей на функцию
        regex_for_func_ptr = r'\w+(\s*\*\s*)*\s*\((\s*\*\s*)+[\w+\[\]]+\s*\)\s*\([^=;]*\)\s*(?=[;=])'
        function_pointer_tokens = PythonTokenizer.search_tokens(src, regex_for_func_ptr, "ptr")
        src = PythonTokenizer.replace_tokens_in_src(src, function_pointer_tokens)
        tokens += function_pointer_tokens

        # Токенизация определения функции, возвращающей указатель на функцию
        regex_for_func_def = r'[\w*\[\]\s]+\s+\([\w*\[\]\s]+\([\w*\[\]\s]+\)\)\s*\([\w*\[\]\s]+\)\s*(?={)'
        function_tokens = PythonTokenizer.search_tokens(src, regex_for_func_def, "func")
        src = PythonTokenizer.replace_tokens_in_src(src, function_tokens)
        tokens += function_tokens

        # Получение токенов не расставленных фигурных скобок после for, while, do, if, else
        tokens += PythonTokenizer.get_tokens_missing_curly_braces(src)

        # Токенизация циклов
        cycle_tokens = PythonTokenizer.search_tokens(src, r'\b(for|while)\b\s*\([^{]+?\)\s*(?=[{\w*])', "cycle")
        src = PythonTokenizer.replace_tokens_in_src(src, cycle_tokens)
        tokens += cycle_tokens
        tokens += PythonTokenizer.search_tokens(src, r'\bdo\b', "cycle")
        while_from_do_tokens = PythonTokenizer.search_tokens(src, r'while\s*\([^;{]+\)\s*;', "cycle")
        src = PythonTokenizer.replace_tokens_in_src(src, while_from_do_tokens)

        # Удаление закрывающей } в switch
        #   Специальный символ $ используется в дальнейшем при токенизации как окончание switch
        src = PythonTokenizer.replace_close_brace_in_switch(src, "$")

        # Удаление break из switch
        for match in re.finditer(r'(\bcase|\bdefault)[^:]*:.*?(\bbreak\s*;\s*}?)', src, flags=re.ASCII + re.DOTALL):
            src = src[:match.start(2)] + PythonTokenizer.NOT_TOKEN * (match.end(2) - match.start(2) - 1) + src[
                                                                                                           match.end(
                                                                                                               2) - 1:]

        # Удаление ключевого слова switch, чтобы оно не было токенизировано как определение функции
        for match in re.finditer(r'\bswitch[^{]*{', src, flags=re.ASCII):
            src = src[:match.start()] + ';' * (match.end() - match.start()) + src[match.end():]

        # Токенизация switch
        for match in re.finditer(r'(\b((case|default)\b[^:]*?:)\s*[{\w])([^}$]*?(?=(}|\$|\bcase\b|\bdefault\b)))', src,
                                 flags=re.ASCII):  # $ используется
            token = Token(PythonTokenizer.TOKENS["if"], match.start(1), match.end(1))
            if src[token.end - 1] != "{":
                tokens.append(Token("{", token.end - 2, token.end - 2))
            tokens.append(token)
            src = src[:match.start(2)] + ';' * (match.end(2) - match.start(2)) + src[match.end(2):]
            if src[match.start(5)] != "}":
                tokens.append(Token("}", match.start(5) - 1, match.start(5) - 1))

        # Токенизация условных конструкций
        if_else_tokens = PythonTokenizer.search_tokens(src, r'\b(if|else\s*if)\s*\([^{;]+?\)\s*(?=[{\w*.])|\belse\b',
                                                       "if")
        src = PythonTokenizer.replace_tokens_in_src(src, if_else_tokens)
        tokens += if_else_tokens

        # Токенизация определения функции
        function_tokens = PythonTokenizer.search_tokens(src, r'\w+((\s*\*\s*)+|\s+)\w+\s*\([^{;]*\)\s*(?={)', "func")
        src = PythonTokenizer.replace_tokens_in_src(src, function_tokens)
        tokens += function_tokens

        # Токенизация вызова функции
        call_tokens = []
        for match in re.finditer(r'[^-+*/%|$<>^\s]\s*\b(\w+\s*\([^;{]*?\)\s*)(?=;)', src, flags=re.ASCII):
            call_tokens.append(Token(PythonTokenizer.TOKENS["call"], match.start(1), match.end(1) + 1))
        src = PythonTokenizer.replace_tokens_in_src(src, call_tokens, is_full_replace=False)
        tokens += call_tokens

        # Токенизация приведения типа
        type_cast_tokens = PythonTokenizer.search_tokens(src,
                                                         r'\(\s*\w+(\s*\*?\s*)*\)\s*(?=[\w\(' + PythonTokenizer.NOT_TOKEN + r'])',
                                                         "cast")
        src = PythonTokenizer.replace_tokens_in_src(src, type_cast_tokens)
        tokens += type_cast_tokens

        # Токенизация указателя на структуру
        struct_pointers_tokens = PythonTokenizer.search_tokens(src, r'(struct|union)\s*\w+(\s*\*+\s*)+\w+', "ptr")
        src = PythonTokenizer.replace_tokens_in_src(src, struct_pointers_tokens)
        tokens += struct_pointers_tokens

        # Токенизация структур
        tokens += PythonTokenizer.search_tokens(src, r'(struct|union)(\s+\w+)?\s*(?={)', "struct")
        regex_for_struct_var = r'(struct|union)\s+\w+\s+\w+[\[\]\d]*(\s*,\s*\w+[\[\]\d]*\s*)*\s*(?=[;=])'
        tokens += PythonTokenizer.search_tokens(src, regex_for_struct_var, "struct")

        # Токенизация возврата из функции
        tokens += PythonTokenizer.search_tokens(src, r'\breturn\b[^;]*;', "return")
        src = re.sub(r'\breturn\b', PythonTokenizer.NOT_TOKEN * 6, src)

        # Токенизация основных типов данных
        regex_for_ptr = r'({int_types}|{char_types}|{float_types}|void)(\s*\*+\s*)+(\s*const\s+)?\w+[\[\]\d:]*(\s*,(\s*\*+\s*)+(\s*const\s+)?\w+[\[\]\d]*\s*)*\s*(?=[;=])' \
            .format(
            int_types=PythonTokenizer.INT_TYPES,
            char_types=PythonTokenizer.CHAR_TYPES,
            float_types=PythonTokenizer.FLOAT_TYPES
        )
        pointers = PythonTokenizer.search_tokens(src, regex_for_ptr, "ptr")
        src = PythonTokenizer.replace_tokens_in_src(src, pointers)
        tokens += pointers
        regex_for_char = r'({char_types})\s+\w+[\[\]\d:]*(\s*,\s*\w+[\[\]\d]*\s*)*\s*(?=[;=])' \
            .format(char_types=PythonTokenizer.CHAR_TYPES)
        tokens += PythonTokenizer.search_tokens(src, regex_for_char, "char")
        regex_for_float = r'({float_types})\s+\w+[\[\]\d:]*(\s*,\s*\w+[\[\]\d]*\s*)*\s*(?=[;=])' \
            .format(float_types=PythonTokenizer.FLOAT_TYPES)
        tokens += PythonTokenizer.search_tokens(src, regex_for_float, "double")
        regex_for_int = r'({int_types})\s+\w+[\[\]\d:]*(\s*,\s*\w+[\[\]\d]*\s*)*\s*(?=[;=])' \
            .format(int_types=PythonTokenizer.INT_TYPES)
        tokens += PythonTokenizer.search_tokens(src, regex_for_int, "int")

        # Токенизация управляющих конструкций
        tokens += PythonTokenizer.search_tokens(src, r'\bcontinue\s*;|\bbreak\s*;|\bgoto\s+\w+;', "control")

        # Токенизация сочетаний оператора присваивания
        #   Специальный символ @ используется для токенизации этих сочетаний в правильном порядке
        src = re.sub(r'(<<|>>|&|\^|\||\+|-|\*|/|%)=', r'@\1', src)

        # Токенизация математических выражений
        tokens += PythonTokenizer.search_tokens(src, r'\w+\+\+|\+\+\w+', "math")
        tokens += PythonTokenizer.search_tokens(src, r'\w+--|--\w+', "math")
        tokens += PythonTokenizer.search_tokens(src, r'(?<=[\w\d)])\s*\*', "math")
        tokens += PythonTokenizer.search_tokens(src, r'(?<=@)\*', "math")  # @ используется
        tokens += PythonTokenizer.search_tokens(src, r'(?<![@={}><|&\s+-.])\s*[+\-/%]\s*(?![>\s+-])',
                                                "math")  # @ используется
        tokens += PythonTokenizer.search_tokens(src, r'(?<=@)[+\-/%]\s*(?![>\s+-])', "math")  # @ используется

        # Токенизация логических операций
        tokens += PythonTokenizer.search_tokens(src, r'&&|\|\||!', "logic")

        # Токенизация побитовых операций
        tokens += PythonTokenizer.search_tokens(src, r'\w+\s*(<<|>>|&|\^|\|)\s*\w+', "shift")
        tokens += PythonTokenizer.search_tokens(src, r'(?<=@)(<<|>>|&|\^|\|)\s*\w+', "shift")  # @ используется
        tokens += PythonTokenizer.search_tokens(src, r'~', "shift")

        # Токенизация сравнений
        tokens += PythonTokenizer.search_tokens(src, r'==|((?<!-)>)|(?<!<)<[^<]|<=|>=|!=', "compare")

        # Токенизация присваивания
        assign_tokens = PythonTokenizer.search_tokens(src, r'[=@]\s*{[^;]*}\s*;', "assign")  # @ используется
        src = PythonTokenizer.replace_tokens_in_src(src, assign_tokens)
        tokens += assign_tokens
        tokens += PythonTokenizer.search_tokens(src, r'(?<!=)[=@][^=;]+;?', "assign")  # @ используется

        # Токенизация фигурных скобок
        for match in re.finditer(r'{', src, flags=re.ASCII):
            tokens.append(Token("{", match.start(), match.end()))
        for match in re.finditer(r'}', src, flags=re.ASCII):
            tokens.append(Token("}", match.start(), match.end()))

        return sorted(tokens, key=attrgetter('start', 'end'))

    @staticmethod
    def search_tokens(src, pattern, token_key, flags=re.ASCII):
        tokens = []
        for match in re.finditer(pattern, src, flags=flags):
            tokens.append(Token(PythonTokenizer.TOKENS[token_key], match.start(), match.end()))
        return tokens

    @staticmethod
    def replace_tokens_in_src(src, tokens, replace=".", is_full_replace=True):
        for token in tokens:
            if is_full_replace is True:
                src = src[:token.start] + replace * (token.end - token.start) + src[token.end:]
            else:
                src = src[:token.start] + replace * (token.end - token.start - 1) + src[token.end - 1:]
        return src

    @staticmethod
    def get_tokens_missing_curly_braces(src):
        tokens = []

        for match in re.finditer(r'\belse\s*([^;{]+;)\s*', src, flags=re.ASCII):
            tokens.append(Token("{", match.start(1) - 1, match.start(1) - 1))
            tokens.append(Token("}", match.end(1) - 1, match.end(1) - 1))

        for match in re.finditer(r'\bdo\b\s*([^{;]+;)', src, flags=re.ASCII):
            tokens.append(Token("{", match.start(1) - 1, match.start(1) - 1))
            tokens.append(Token("}", match.end(1) - 1, match.end(1) - 1))

        for match in re.finditer(r'\bfor\s*\((([^;]*;\s*){2}[^)]*)\)', src, flags=re.ASCII):
            src = src[:match.start(1)] + "." * (match.end(1) - match.start(1)) + src[match.end(1):]

        keywords = ["while", "if", "for"]
        for word in keywords:
            for match in re.finditer(r'(?=(\b' + word + r'\s*\([^;{]+?\)\s*([^;{]+;)\s*))', src, flags=re.ASCII):
                tokens.append(Token("{", match.start(2) - 1, match.start(2) - 1))
                i = match.end(1)
                if i + 4 < len(src) and word != "if":
                    if src[i] == 'e' and src[i + 1] == 'l' and src[i + 2] == 's' and src[i + 3] == 'e' \
                            and not str.isalpha(src[i + 4]):
                        while i < len(src) and src[i] != ';':
                            i += 1
                        tokens.append(Token("}", i, i))
                        continue
                tokens.append(Token("}", match.end(2) - 1, match.end(2) - 1))

        return tokens

    @staticmethod
    def replace_close_brace_in_switch(src, symbol):
        for match in re.finditer(r'\bswitch\b[^{]+{', src, flags=re.ASCII):
            i = match.end()
            count_close_brace = 1
            while i < len(src):
                if src[i] == '{':
                    count_close_brace += 1
                if src[i] == '}':
                    count_close_brace -= 1
                    if count_close_brace == 0:
                        src = src[:i] + symbol + src[i + 1:]
                        break
                i += 1
        return src

    @staticmethod
    def get_tokens_ternary_operator(src, replace='.'):
        tokens = []
        for match in re.finditer(
                r'(?<=[;}{()\w])\s*(=|\breturn\b)?([^;<>=]+(==|>=|<=|>|<)[^;<>=?]+)(\?[^:;]+)(:[^;]+;)', src,
                flags=re.ASCII):
            tokens.append(Token(PythonTokenizer.TOKENS["if"], match.start(4), match.start(4)))
            tokens.append(Token("{", match.start(4), match.start(4) + 1))
            tokens.append(Token("}", match.end(4) - 1, match.end(4) - 1))
            tokens.append(Token(PythonTokenizer.TOKENS["if"], match.start(5), match.start(5)))
            tokens.append(Token("{", match.start(5), match.start(5) + 1))
            tokens.append(Token("}", match.end(5) - 1, match.end(5) - 1))
            if match[1] == "=":
                tokens.append(Token(PythonTokenizer.TOKENS["assign"], match.start(4), match.start(4) + 2))
                tokens.append(Token(PythonTokenizer.TOKENS["assign"], match.start(5), match.start(5) + 2))
                src = src[:match.start(1)] + "." + src[match.start(1) + 1:]
            if match[1] == "return":
                tokens.append(Token(PythonTokenizer.TOKENS["return"], match.start(4), match.start(4) + 2))
                tokens.append(Token(PythonTokenizer.TOKENS["return"], match.start(5), match.start(5) + 2))
                src = src[:match.start(1)] + "." * (match.end(1) - match.start(1)) + src[match.end(1):]
            src = src[:match.start(5)] + ";" + src[match.start(5) + 1:]
            src = src[:match.start(2)] + replace * (match.end(2) - match.start(2)) + src[match.end(2):]
        return tokens, src

    @staticmethod
    def get_function_names(src):
        functions = set()
        for match in re.finditer(r'\w+(\s*\*\s*)*\s*\((\s*\*?\s*)*(\w+)\s*\([^{]*\)\s*\)\s*\([^{]*\)\s*{', src):
            functions |= {match[3]}
        for match in re.finditer(r'\w+((\s*\*\s*)+|\s+)(\w+)\s*\([^{]*\)\s*{', src):
            functions |= {match[3]}
        functions -= {"main"}
        return list(functions)


def search_heckel(target_filename, origin_filename, length_n_gramm=4):
    with open(origin_filename, encoding='utf-8') as origin_file, open(target_filename, encoding='utf-8') as target_file:
        tokenizer = PythonTokenizer()
        origin_tokens = Token.get_tokens_str_from_token_list(tokenizer.tokenize(origin_file.read()))
        target_tokens = Token.get_tokens_str_from_token_list(tokenizer.tokenize(target_file.read()))
    origin_n_gramms = split_into_n_gramms(origin_tokens, length_n_gramm)
    target_n_gramms = split_into_n_gramms(target_tokens, length_n_gramm)
    return round(len(origin_n_gramms & target_n_gramms) / len(origin_n_gramms | target_n_gramms) * 100)



def split_into_n_gramms(token_str, length_n_gramm):
    if length_n_gramm <= 0:
        return set()
    n_gramms = []
    for i in range(len(token_str) - length_n_gramm + 1):
        n_gramms.append(token_str[i:i + length_n_gramm])
    return set(n_gramms)


if __name__ == "__main__":
    file1_path = "../test_examples/original_program.py"
    file2_path = "../test_examples/F_copy_type3_reordered_lines.py"

    plagiarism_percentage = search_heckel(target_filename=file2_path, origin_filename=file1_path)
    print("Процент заимствований между файлами:", plagiarism_percentage, "%")


