# Пример программы для демонстрации алгоритмов обнаружения заимствований

def compute_fact(n):
    """Вычисление факториала числа."""
    if n == 0:
        return 1
    else:
        return n * compute_fact(n - 1)


def compute_fib(n):
    """Вычисление n-го числа Фибоначчи."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return compute_fib(n - 1) + compute_fib(n - 2)


def is_num_prime(num):
    """Проверка, является ли число простым."""
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def quick_sorting(array):
    """Быстрая сортировка массива."""
    if len(array) <= 1:
        return array
    else:
        pivot = array[len(array) // 2]
        left = [x for x in array if x < pivot]
        middle = [x for x in array if x == pivot]
        right = [x for x in array if x > pivot]
        return quick_sorting(left) + middle + quick_sorting(right)


def binary_search_func(array, target):
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
    num = 5
    print(f"Факториал {num} = {compute_fact(num)}")
    print(f"Число Фибоначчи {num} = {compute_fib(num)}")
    print(f"Число {num} простое? {is_num_prime(num)}")

    arr = [3, 6, 8, 10, 1, 2, 1]
    print(f"Исходный массив: {arr}")
    sorted_arr = quick_sorting(arr)
    print(f"Отсортированный массив: {sorted_arr}")

    target = 10
    index = binary_search_func(sorted_arr, target)
    if index != -1:
        print(f"Элемент {target} найден на позиции {index} в отсортированном массиве.")
    else:
        print(f"Элемент {target} не найден в массиве.")


if __name__ == "__main__":
    main()
