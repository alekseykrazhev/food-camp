
import string


def get_field_to_sort(field_name: str, arr):
    """
    get field to sort by
    """
    return arr[field_name]


def selection_sort(arr: list, field_name: string) -> list:
    """
    Selection sort algorithm for list of dictionaries
    """
    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            if get_field_to_sort(field_name, arr[j]) < get_field_to_sort(field_name, arr[min_index]):
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr
    