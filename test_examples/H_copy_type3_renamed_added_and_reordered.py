# Пример программы для демонстрации алгоритмов обнаружения заимствований

def calc_factorial(k):
    """Вычисление факториала числа."""
    if k == 0:
        return 1
    else:
        print(f"Вычисление факториала для {k}")  # Добавленная строка 1
        return k * calc_factorial(k - 1)


def calc_fibonacci(k):
    """Вычисление n-го числа Фибоначчи."""
    if k <= 0:
        return 0
    elif k == 1:
        return 1
    else:
        print(f"Вычисление числа Фибоначчи для {k}")  # Добавленная строка 2
        return calc_fibonacci(k - 1) + calc_fibonacci(k - 2)


def prime_number(k):
    """Проверка, является ли число простым."""
    if k <= 1:
        return False
    for j in range(2, int(k ** 0.5) + 1):
        if k % j == 0:
            return False
        print(f"Проверка числа {k} на простоту")  # Добавленная строка 3
    return True


def quick_sort(array):
    """Быстрая сортировка массива."""
    if len(array) <= 1:
        return array
    else:
        new_pivot = array[len(array) // 2]
        new_left = [value for value in array if value < new_pivot]
        new_middle = [value for value in array if value == new_pivot]
        new_right = [value for value in array if value > new_pivot]
        print(f"Сортировка: {array}")  # Добавленная строка 4
        return quick_sort(new_left) + new_middle + quick_sort(new_right)


def search_binary(array, target_value):
    """Бинарный поиск в отсортированном массиве."""
    new_left, new_right = 0, len(array) - 1
    while new_left <= new_right:
        new_mid = (new_left + new_right) // 2
        if array[new_mid] == target_value:
            return new_mid
        elif array[new_mid] < target_value:
            new_left = new_mid + 1
        else:
            new_right = new_mid - 1
    print(f"Поиск элемента {target_value}")  # Добавленная строка 5
    return -1


def main():
    """Основная функция."""
    array = [3, 6, 8, 10, 1, 2, 1]
    print(f"Исходный массив: {array}")
    sorted_arr = quick_sort(array)
    print(f"Отсортированный массив: {sorted_arr}")

    target_value = 10
    number = 5
    print(f"Факториал {number} = {calc_factorial(number)}")
    print(f"Число Фибоначчи {number} = {calc_fibonacci(number)}")
    print(f"Число {number} простое? {prime_number(number)}")

    index_position = search_binary(sorted_arr, target_value)
    if index_position != -1:
        print(f"Элемент {target_value} найден на позиции {index_position} в отсортированном массиве.")
    else:
        print(f"Элемент {target_value} не найден в массиве.")


if __name__ == "__main__":
    main()
