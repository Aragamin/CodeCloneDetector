# Пример программы для демонстрации алгоритмов обнаружения заимствований

def compute_fact(x):
    """Вычисление факториала числа."""
    if x == 0:
        return 1
    else:
        return x * compute_fact(x - 1)


def compute_fib(x):
    """Вычисление n-го числа Фибоначчи."""
    if x <= 0:
        return 0
    elif x == 1:
        return 1
    else:
        return compute_fib(x - 1) + compute_fib(x - 2)


def is_num_prime(x):
    """Проверка, является ли число простым."""
    if x <= 1:
        return False
    for i in range(2, int(x ** 0.5) + 1):
        if x % i == 0:
            return False
    return True


def quick_sorting(arr):
    """Быстрая сортировка массива."""
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sorting(left) + middle + quick_sorting(right)


def binary_search_func(arr, target):
    """Бинарный поиск в отсортированном массиве."""
    l, r = 0, len(arr) - 1
    while l <= r:
        mid = (l + r) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            l = mid + 1
        else:
            r = mid - 1
    return -1


def main():
    """Основная функция."""
    number = 5
    print(f"Факториал {number} = {compute_fact(number)}")
    print(f"Число Фибоначчи {number} = {compute_fib(number)}")
    print(f"Число {number} простое? {is_num_prime(number)}")

    array = [3, 6, 8, 10, 1, 2, 1]
    print(f"Исходный массив: {array}")
    sorted_array = quick_sorting(array)
    print(f"Отсортированный массив: {sorted_array}")

    tgt = 10
    idx = binary_search_func(sorted_array, tgt)
    if idx != -1:
        print(f"Элемент {tgt} найден на позиции {idx} в отсортированном массиве.")
    else:
        print(f"Элемент {tgt} не найден в массиве.")


if __name__ == "__main__":
    main()
