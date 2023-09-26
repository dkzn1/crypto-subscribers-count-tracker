from lib.interfaces.data_processor_interface import IDataProcessor


class DataProcessor(IDataProcessor):
    """
    Base class for processing data that falls under computation category and also general processing logic.

    This class provides a foundation for data processors and defines a common utility methods for processing data in different services.

    Methods:
        __init__: Initializes the DataProcessor class. To be implemented in subclasses.
    """

    def __init__(self) -> None:
        """
        Initialize the DataProcessor.

        Implement in subclasses.
        """
        pass
