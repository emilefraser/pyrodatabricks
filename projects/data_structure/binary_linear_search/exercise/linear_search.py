import datetime
from jovian.pythondsa import evaluate_test_cases
from tests import tests, large_tests

# Problem Statement
'''Swap cards and find matching numbers within a bunch of cards'''
# Solved with Linear Search


def locate_cards(cards, query):
    # Create a variable position with the value 0
    position = 0
    # Set up loop for repetition
    while position < len(cards):
        # Catch if element at the current position match the query
        if cards[position] == query:
            return position
        position += 1
    return -1


if __name__ == "__main__":
    # Test Cases lists are provided here below and print each test status and amount of time it needs to completion

    count = 1
    for test in tests:
        start_time = datetime.datetime.now()
        print("Test Case Number : ", count)
        print("Execution started ", start_time)
        output = test["output"]
        result = locate_cards(**test["input"])
        print("Expected Output : \n", output)
        print("Actual Output : \n", result)
        if result == output:
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
    # result = locate_cards(**large_tests["input"])
    # print("Expected Output : \n", output)
    # print("Actual Output : \n", result)
    # if result == output:
    #     print("Test Case Status: Passed")
    # else:
    #     print("Test Case Status: Failed")
    # end_time = datetime.datetime.now()
    # time_diff = end_time - start_time
    # print(f"Execution Time {time_diff} \n\n")

    # If you want to Test with Jovian "evaluate_test_cases" function, you will see test results output on terminal

    # evaluate_test_cases(locate_cards, tests)
