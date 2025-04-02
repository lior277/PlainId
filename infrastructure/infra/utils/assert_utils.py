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
    def assert_equal(expected, actual, message=None):
        if expected != actual:
            if message is None:
                message = f"Expected {expected}, but got {actual}"
            raise AssertionError(message)



