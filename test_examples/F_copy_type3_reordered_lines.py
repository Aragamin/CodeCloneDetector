# Пример программы для демонстрации алгоритмов обнаружения заимствований

def factorial(n):
    """Вычисление факториала числа."""
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def fibonacci(n):
    """Вычисление n-го числа Фибоначчи."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def is_prime(n):
    """Проверка, является ли число простым."""
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def quicksort(arr):
    """Быстрая сортировка массива."""
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quicksort(left) + middle + quicksort(right)


def binary_search(arr, target):
    """Бинарный поиск в отсортированном массиве."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def main():
    """Основная функция."""
    arr = [3, 6, 8, 10, 1, 2, 1]
    print(f"Исходный массив: {arr}")
    sorted_arr = quicksort(arr)
    print(f"Отсортированный массив: {sorted_arr}")

    target = 10
    num = 5
    print(f"Факториал {num} = {factorial(num)}")
    print(f"Число Фибоначчи {num} = {fibonacci(num)}")
    print(f"Число {num} простое? {is_prime(num)}")

    index = binary_search(sorted_arr, target)
    if index != -1:
        print(f"Элемент {target} найден на позиции {index} в отсортированном массиве.")
    else:
        print(f"Элемент {target} не найден в массиве.")


if __name__ == "__main__":
    main()
