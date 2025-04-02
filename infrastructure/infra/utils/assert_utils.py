from typing import Callable, List, Any

class CustomAssert:
    @staticmethod
    def assert_multiple(assertions: List[Callable[[], None]], message=None):
        errors = []
        for assertion in assertions:
            try:
                assertion()
            except AssertionError as e:
                errors.append(str(e))

        if errors:
            if message is None:
                message = "Multiple assertions failed:\n" + "\n".join(errors)
            raise AssertionError(message)

    @staticmethod
    def assert_true(condition, message=None):
        if not condition:
            if message is None:
                message = "Expected condition to be True, but it was False"
            raise AssertionError(message)

    @staticmethod
    def assert_false(condition, message=None):
        if condition:
            if message is None:
                message = "Expected condition to be False, but it was True"
            raise AssertionError(message)

    @staticmethod
    def assert_equal(expected, actual, message=None):
        if expected != actual:
            if message is None:
                message = f"Expected {expected}, but got {actual}"
            raise AssertionError(message)

    @staticmethod
    def assert_not_equal(expected, actual, message=None):
        if expected == actual:
            if message is None:
                message = f"Expected {expected} and {actual} to be different"
            raise AssertionError(message)

    @staticmethod
    def assert_in(expected, container, message=None):
        if expected not in container:
            if message is None:
                message = f"Expected {expected} to be in {container}"
            raise AssertionError(message)

    @staticmethod
    def assert_not_in(expected, container, message=None):
        if expected in container:
            if message is None:
                message = f"Expected {expected} not to be in {container}"
            raise AssertionError(message)

    @staticmethod
    def assert_greater(first, second, message=None):
        if not first > second:
            if message is None:
                message = f"Expected {first} to be greater than {second}"
            raise AssertionError(message)

    @staticmethod
    def assert_greater_equal(first, second, message=None):
        if not first >= second:
            if message is None:
                message = "Expected {first} to be greater than or equal to {second}"
            raise AssertionError(message)

    @staticmethod
    def assert_less(first, second, message=None):
        if not first < second:
            if message is None:
                message = "Expected {first} to be less than {second}"
            raise AssertionError(message)

    @staticmethod
    def assert_less_equal(first, second, message=None):
        if not first <= second:
            if message is None:
                message = "Expected {first} to be less than or equal to {second}"
            raise AssertionError(message)