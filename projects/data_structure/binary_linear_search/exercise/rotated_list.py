from tests import rotated_test, rotated_single_test, rotated_large_tests
from jovian.pythondsa import evaluate_test_cases, evaluate_test_case
import datetime

# Problem Statement
''' You are given list of numbers, obtained by rotating a sorted list an unknown number of times.
Write a function to determine the minimum number of times the original sorted list was rotated to obtain the given list.
Your function should have the worst-case complexity of O(log N), where N is the length of the list.
You can assume that all the numbers in the list are unique.'''


def count_rotations_linear(nums):
    position = 1    # What is the initial value of position

    while position < len(nums):         # When should the loop run
        # Success Criteria: Check whether the number at the current position is less than predecessor
        if position > 0 and nums[position] < nums[position-1]:
            return position
        # Move to the next position
        position += 1
    return 0


def count_rotations_binary(nums):
    low = 0
    high = len(nums)-1

    while low <= high:
        mid = (low + high) // 2
        mid_number = nums[mid]
        # Uncomment the next line for logging the values and fixing errors.
        # print("lo:", lo, ", hi:", hi, ", mid:", mid, ", mid_number:", mid_number)

        if mid > 0 and mid_number < nums[mid-1]:
            # The middle position is the answer
            return mid
        elif mid_number < high:
            # Answer lies in the left half
            high = mid - 1
        else:
            # Answer lies in the right half
            low = mid + 1

    return 0


if __name__ == "__main__":
    # Test Cases lists are provided here below and print each test status and amount of time it needs to completion
    """Here it tests locally"""
    # for rotation in [count_rotations_binary, count_rotations_linear]:
    #     print(f"Test cases Running for {'Binary' if rotation == count_rotations_binary else 'Linear'} \n")
    #     count = 1
    #     for test in rotated_test:
    #         start_time = datetime.datetime.now()
    #         print("Test Case Number : ", count)
    #         # print("Execution started ", start_time)
    #         output = test["output"]
    #         test_result = count_rotations_binary(**test["input"])
    #         print("Expected Output : \n", output)
    #         print("Actual Output : \n", test_result)
    #         if test_result == output:
    #             print("Test Case Status: Passed")
    #         else:
    #             print("Test Case Status: Failed")
    #         end_time = datetime.datetime.now()
    #         time_diff = end_time - start_time
    #         print(f"Execution Time {time_diff} \n")
    #         count += 1
    #     print(f"Test cases completed for {'Binary' if rotation == count_rotations_binary else 'Linear'} \n\n")

    # Here is below code for Jovian "evaluate_test_case" and "evaluate_test_cases" Test Cases

    print("\nSingle Test Case Running...\n")
    print("\nRotated list through Linear Search\n")
    evaluate_test_case(count_rotations_linear, rotated_single_test)
    print("Rotated list through Binary Search\n")
    evaluate_test_case(count_rotations_binary, rotated_single_test)
    print("\n\nMultiple Test Cases Running...")
    print("\nRotated list through Linear Search\n")
    evaluate_test_cases(count_rotations_linear, rotated_test)
    print("\nRotated list through Binary Search\n")
    evaluate_test_cases(count_rotations_binary, rotated_test)

    # Below Code for to test with large Test Case set to check the time and space complexity

    # for rotation in [count_rotations_binary, count_rotations_linear]:
    #     print(f"Test cases Running for {'Binary' if rotation == count_rotations_binary else 'Linear'} \n")
    #     start_time = datetime.datetime.now()
    #     print("Test Case Number : ", 1)
    #     print("Execution started ", start_time)
    #     output = rotated_large_tests["output"]
    #     test_result = rotation(**rotated_large_tests["input"])
    #     print("Expected Output : \n", output)
    #     print("Actual Output : \n", test_result)
    #     if test_result == output:
    #         print("Test Case Status: Passed")
    #     else:
    #         print("Test Case Status: Failed")
    #     end_time = datetime.datetime.now()
    #     time_diff = end_time - start_time
    #     print(f"Execution Time {time_diff} \n\n")
    # print(f"Test cases completed for {'Binary' if rotation == count_rotations_binary else 'Linear'} \n\n")

