from lib.interfaces.data_processor_interface import IDataProcessor


class DataValidator(IDataProcessor):
    """
    Base class for processing data that falls under validation category.

    This class provides a foundation for data processors and defines a common utility methods for validating data in different services.

    Methods:
        __init__: Initializes the DataValidator class. To be implemented in subclasses.
    """

    def __init__(self) -> None:
        """
        Initialize the DataValidator.

        Implement in subclasses.
        """
        pass
