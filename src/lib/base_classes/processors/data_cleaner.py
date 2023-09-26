from lib.interfaces.data_processor_interface import IDataProcessor


class DataCleaner(IDataProcessor):
    """
    Base class for processing data that falls under cleaning categoryr like filtering or removing redundant data.

    This class provides a foundation for data cleaning operations and defines a common utility methods for cleaning data in different services.

    Methods:
        __init__: Initializes the DataCleaner class. To be implemented in subclasses.
    """

    def __init__(self) -> None:
        """
        Initialize the DataCleaner.

        Implement in subclasses.
        """
        pass
