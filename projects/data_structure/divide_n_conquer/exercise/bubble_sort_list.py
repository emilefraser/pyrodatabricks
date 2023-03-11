from tests import *
from jovian.pythondsa import evaluate_test_cases


def bubble_sort(nums):
    # Create a copy of the list, to avoid changing it
    nums = list(nums)
    # 4. Repeat the process n-1 times
    for _ in range(len(nums) - 1):
        # 1. Iterate over the array (except last element)
        for i in range(len(nums) - 1):
            # 2. Compare the number with
            if nums[i] > nums[i + 1]:
                # 3. Swap the two elements
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
    # Return the sorted list
    return nums


if __name__ == "__main__":
    x, y = 2, 3
    x, y = y, x
    print(f"x value is {x} and y value is {y}")

    # Let's test it with an example.
    nums0, output0 = random_test0['input']['nums'], random_test0['output']

    print('\nInput:', nums0)
    print('\nExpected output:', output0)
    result0 = bubble_sort(nums0)
    print('\nActual output:', result0)
    print('\nMatch:', result0 == output0)
    print("Result Status: ", result0 == output0)

    # Tests with Jovian "evaluate_test_cases"
    results = evaluate_test_cases(bubble_sort, random_tests)

