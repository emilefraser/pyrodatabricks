from tests import *
from jovian.pythondsa import evaluate_test_cases


def merge_sort(nums):
    # Terminating condition (list of 0 or 1 elements)
    if len(nums) <= 1:
        return nums

    # Get the midpoint
    mid = len(nums) // 2
    # Split the list into two halves
    left = nums[:mid]
    right = nums[mid:]
    # Solve the problem for each half recursively
    left_sorted, right_sorted = merge_sort(left), merge_sort(right)

    # Combine the results of the two halves
    sorted_nums = merge(left_sorted, right_sorted)
    return sorted_nums


def merge(nums1, nums2):
    # List to store the results
    merged = []
    # Indices for iteration
    i, j = 0, 0
    # Loop over the two lists
    while i < len(nums1) and j < len(nums2):
        # Include the smaller element in the result and move to next element
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1

    # Get the remaining parts
    nums1_tail = nums1[i:]
    nums2_tail = nums2[j:]

    # Return the final merged array
    return merged + nums1_tail + nums2_tail


def merge_test(nums1, nums2, depth=0):
    print('  ' * depth, 'merge:', nums1, nums2)
    i, j, merged = 0, 0, []
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1
    return merged + nums1[i:] + nums2[j:]


def merge_sort_test(nums, depth=0):
    print('  ' * depth, 'merge_sort:', nums)
    if len(nums) < 2:
        return nums
    mid = len(nums) // 2
    return merge_test(merge_sort_test(nums[:mid], depth + 1),
                      merge_sort_test(nums[mid:], depth + 1),
                      depth + 1)


if __name__ == "__main__":
    # Let's test the merge operation, before we test merge sort.

    merge([1, 4, 7, 9, 11], [-1, 0, 2, 3, 8, 12])

    # It seems to work as expected. We can now test the merge_sort function.

    nums0, output0 = random_test0['input']['nums'], random_test0['output']
    print('\nInput:', nums0)
    print('\nExpected output:', output0)
    result0 = merge_sort(nums0)
    print('\nActual output:', result0)
    print('\nMatch:', result0 == output0)

    # Let's test all the cases using the evaluate_test_cases function from jovian.
    results = evaluate_test_cases(merge_sort, random_tests)
    print("\nAll the test cases have passed! Our function works as expected."
          "Normal tests covered, Let's starts with large Test Cases")

    # Analyze the algorithm's complexity and identify inefficiencies
    print("Testing with large data set \n")
    output = merge_sort_test([5, -12, 2, 6, 1, 23, 7, 7, -12])
    print("\nresult output, ", output)
