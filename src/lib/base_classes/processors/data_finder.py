from lib.interfaces.data_processor_interface import IDataProcessor


class DataFinder(IDataProcessor):
    """
    Base class for processing data that falls under finding category of processing, i.e. extracting data etc.

    This class provides a foundation for data processors and defines a common utility methods for finding data in different services.

    Methods:
        __init__: Initializes the DataFinder class. To be implemented in subclasses.
    """

    def __init__(self) -> None:
        """
        Initialize the DataFinder.

        Implement in subclasses.
        """
        pass
