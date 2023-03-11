from jovian.pythondsa import evaluate_test_cases
import datetime
from tests import large_tests, tests


def find_cards(cards, query, mid):
    # find middle number
    mid_number = cards[mid]
    print("mid: ", mid, ", mid_number: ", mid_number)
    if mid_number == query:
        if mid-1 >= 0 and cards[mid-1] == query:
            # We do return (left, right, found) words as a string
            return "left"
        else:
            return "found"
    elif mid_number < query:
        return "left"
    else:
        return "right"


def locate_card(cards, query):
    low, high = 0, len(cards)
    while low <= high:
        print("low: ", low, ", high: ", high)
        mid = (low + high) // 2
        result = find_cards(cards, query, mid)
        if result == "found":
            return mid
        elif result == "left":
            high = mid - 1
        elif result == "right":
            low = mid + 1
    return -1


if __name__ == "__main__":
    # Test Cases lists are provided here below and print each test status and amount of time it needs to completion

    count = 1
    for test in tests:
        start_time = datetime.datetime.now()
        print("Test Case Number : ", count)
        print("Execution started ", start_time)
        output = test["output"]
        test_result = locate_card(**test["input"])
        print("Expected Output : \n", output)
        print("Actual Output : \n", test_result)
        if test_result == output:
            print("Test Case Status: Passed")
        else:
            print("Test Case Status: Failed")
        end_time = datetime.datetime.now()
        time_diff = end_time - start_time
        print(f"Execution Time {time_diff} \n\n")
        count += 1

    # Below Code for to test with large Test Case set to check the time and space complexity

    # start_time = datetime.datetime.now()
    # print("Test Case Number : ", 1)
    # print("Execution started ", start_time)
    # output = large_tests["output"]
    # test_result = locate_card(**large_tests["input"])
    # print("Expected Output : \n", output)
    # print("Actual Output : \n", test_result)
    # if test_result == output:
    #     print("Test Case Status: Passed")
    # else:
    #     print("Test Case Status: Failed")
    # end_time = datetime.datetime.now()
    # time_diff = end_time - start_time
    # print(f"Execution Time {time_diff} \n\n")

    # If you want to Test with Jovian "evaluate_test_cases" function, do uncomment below single line f code,
    # you will see test results output on terminal

    # evaluate_test_cases(locate_card, tests)
