def quick_sort(arr):
    if len(arr) <= 1:
        return arr  # Base case: an array of 0 or 1 elements is already sorted
    else:
        pivot = arr[len(arr) // 2]  # Choose a pivot element
        left = [x for x in arr if x < pivot]  # Elements less than pivot
        middle = [x for x in arr if x == pivot]  # Elements equal to pivot
        right = [x for x in arr if x > pivot]  # Elements greater than pivot
        return (
            quick_sort(left) + middle + quick_sort(right)
        )  # Recursively sort and combine


# Example usage
arr = [10, 7, 8, 9, 1, 5]
sorted_arr = quick_sort(arr)
print("Sorted array:", sorted_arr)
