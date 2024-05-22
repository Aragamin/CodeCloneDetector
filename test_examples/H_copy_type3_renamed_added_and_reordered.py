# Пример программы для демонстрации алгоритмов обнаружения заимствований

def compute_factorial(x):
    """Вычисление факториала числа."""
    if x == 0:
        return 1
    else:
        print(f"Вычисление факториала для {x}")  # Добавленная строка 1
        return x * compute_factorial(x - 1)


def compute_fibonacci(x):
    """Вычисление n-го числа Фибоначчи."""
    if x <= 0:
        return 0
    elif x == 1:
        return 1
    else:
        print(f"Вычисление числа Фибоначчи для {x}")  # Добавленная строка 2
        return compute_fibonacci(x - 1) + compute_fibonacci(x - 2)


def is_prime_number(x):
    """Проверка, является ли число простым."""
    if x <= 1:
        return False
    for i in range(2, int(x ** 0.5) + 1):
        if x % i == 0:
            return False
    print(f"Проверка числа {x} на простоту")  # Добавленная строка 3
    return True


def quick_sort(array):
    """Быстрая сортировка массива."""
    if len(array) <= 1:
        return array
    else:
        pivot = array[len(array) // 2]
        left = [y for y in array if y < pivot]
        middle = [y for y in array if y == pivot]
        right = [y for y in array if y > pivot]
        print(f"Сортировка: {array}")  # Добавленная строка 4
        return quick_sort(left) + middle + quick_sort(right)


def binary_search_algorithm(array, target):
    """Бинарный поиск в отсортированном массиве."""
    left, right = 0, len(array) - 1
    while left <= right:
        mid = (left + right) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    print(f"Поиск элемента {target}")  # Добавленная строка 5
    return -1


def main():
    """Основная функция."""
    array = [3, 6, 8, 10, 1, 2, 1]
    sorted_array = quick_sort(array)
    print(f"Исходный массив: {array}")
    print(f"Отсортированный массив: {sorted_array}")

    search_target = 10
    search_index = binary_search_algorithm(sorted_array, search_target)
    if search_index != -1:
        print(f"Элемент {search_target} найден на позиции {search_index} в отсортированном массиве.")
    else:
        print(f"Элемент {search_target} не найден в массиве.")

    number = 5
    print(f"Факториал {number} = {compute_factorial(number)}")
    print(f"Число Фибоначчи {number} = {compute_fibonacci(number)}")
    print(f"Число {number} простое? {is_prime_number(number)}")


if __name__ == "__main__":
    main()
