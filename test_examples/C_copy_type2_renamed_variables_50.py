# Пример программы для демонстрации алгоритмов обнаружения заимствований

def calc_factorial(k):
    """Вычисление факториала числа."""
    if k == 0:
        return 1
    else:
        return k * calc_factorial(k - 1)


def calc_fibonacci(k):
    """Вычисление n-го числа Фибоначчи."""
    if k <= 0:
        return 0
    elif k == 1:
        return 1
    else:
        return calc_fibonacci(k - 1) + calc_fibonacci(k - 2)


def prime_number(k):
    """Проверка, является ли число простым."""
    if k <= 1:
        return False
    for j in range(2, int(k ** 0.5) + 1):
        if k % j == 0:
            return False
    return True


def quick_sort(array):
    """Быстрая сортировка массива."""
    if len(array) <= 1:
        return array
    else:
        new_pivot = array[len(array) // 2]
        left = [x for x in array if x < new_pivot]
        middle = [x for x in array if x == new_pivot]
        right = [x for x in array if x > new_pivot]
        return quick_sort(left) + middle + quick_sort(right)


def binary_search(array, target):
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
    return -1


def main():
    """Основная функция."""
    number = 5
    print(f"Факториал {number} = {calc_factorial(number)}")
    print(f"Число Фибоначчи {number} = {calc_fibonacci(number)}")
    print(f"Число {number} простое? {prime_number(number)}")

    arr = [3, 6, 8, 10, 1, 2, 1]
    print(f"Исходный массив: {arr}")
    sorted_arr = quick_sort(arr)
    print(f"Отсортированный массив: {sorted_arr}")

    target = 10
    index = binary_search(sorted_arr, target)
    if index != -1:
        print(f"Элемент {target} найден на позиции {index} в отсортированном массиве.")
    else:
        print(f"Элемент {target} не найден в массиве.")


if __name__ == "__main__":
    main()
