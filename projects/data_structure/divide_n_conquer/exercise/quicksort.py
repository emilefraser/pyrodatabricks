from tests import *
from jovian.pythondsa import evaluate_test_cases


def quicksort(nums, start=0, end=None):
    # print('quicksort', nums, start, end)
    if end is None:
        nums = list(nums)
        end = len(nums) - 1

    if start < end:
        pivot = partition(nums, start, end)
        quicksort(nums, start, pivot -1)
        quicksort(nums, pivot +1, end)

    return nums


def partition(nums, start=0, end=None):
    # print('partition', nums, start, end)
    if end is None:
        end = len(nums) - 1

    # Initialize right and left pointers
    l, r = start, end - 1

    # Iterate while they're apart
    while r > l:
        # print('  ', nums, l, r)
        # Increment left pointer if number is less or equal to pivot
        if nums[l] <= nums[end]:
            l += 1

        # Decrement right pointer if number is greater than pivot
        elif nums[r] > nums[end]:
            r -= 1

        # Two out-of-place elements found, swap them
        else:
            nums[l], nums[r] = nums[r], nums[l]
    # print('  ', nums, l, r)
    # Place the pivot between the two parts
    if nums[l] > nums[end]:
        nums[l], nums[end] = nums[end], nums[l]
        return l
    else:
        return end


if __name__ == "__main__":
    # Do test with quicksort by doing partition
    l1 = [1, 5, 6, 2, 0, 11, 3]
    pivot_ = partition(l1)
    print("\nVariable l1 and pivot_ values, ", l1, pivot_)

    # We can now see quicksort in action:
    nums0, output0 = random_test0['input']['nums'], random_test0['output']
    print('\nInput:', nums0)
    print('\nExpected output:', output0)
    result0 = quicksort(nums0)
    print('\nActual output:', result0)
    print('\nMatch:', result0 == output0)

    # Let's test all the cases using the evaluate_test_cases function from jovian.
    print("\nRunning all test cases through Jovian test cases\n")
    results = evaluate_test_cases(quicksort, random_tests)
