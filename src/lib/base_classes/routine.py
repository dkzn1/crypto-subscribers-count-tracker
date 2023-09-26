from typing import Optional, Any, Callable, Union
from abc import ABC, abstractmethod
import time
from functools import wraps
from datetime import datetime

from lib.logger import Logger


class Routine(ABC):
    """
    Base class for creating and managing routines within a service.

    Attributes:
        routines: Reference to the routines manager.
        service: Reference to the service associated with the routine.
        _routine_intervals_hours (List[Union[int, float]]): List of routine
        run/idle intervals in hours.
        refetch_timeout_sec (int): Timeout duration for refetching routines.
        update_timestamp (int): Timestamp of the last routine update.

    Methods:
        - run(): Run the routine. Implementation is in child classes.
        - start(): Add routine to the list of active routine instances.
        - stop(): Remove routine from the list of active routine instances.
        - refetch(): Refetch utility method for failed fetch attempts.
        - check_idle_status(): Check if the routine has been idle for a specified interval.
        - check_run_interval(): Decorator to control routine execution based on intervals.

    Usage:
        To create a custom routine, subclass `Routine` and implement the `run()` method.
    """

    def __init__(self, service) -> None:
        """
        Initialize a Routine

        Args:
            routines: Reference to the routines manager.
            service: Reference to the service associated with the routine.
            intervals (List[Union[int, float]]): List of routine intervals in hours.
        """
        self._service = service

        self._db = service.db
        self._config = service.config

        self._log = Logger(name=self.__class__.__name__)

        if hasattr(service, 'formatter'):
            self._formatter = service.formatter
        if hasattr(service, 'cleaner'):
            self._cleaner = service.cleaner
        if hasattr(service, 'finder'):
            self._finder = service.finder
        if hasattr(service, 'validator'):
            self._validator = service.validator
        if hasattr(service, 'processor'):
            self._processor = service.processor

        self._routine_intervals_hours = service.config.routine_intervals_hours
        self._refetch_timeout_sec = service.config.refetch_timeout_sec

        self._update_timestamp = None

        self._cookie = None

    #
    #
    #

    @abstractmethod
    def run(self) -> None:
        """
        Implement in child classes

        This method should be overridden in child classes to define the behavior of the routine.
        """
        pass

    #
    #
    #

    def restart(self) -> None:
        """
        Adds the routine to the list of active routine instances and initiates its execution.
        """
        self._service.add_routine(self)
        self.run()

    #
    #
    #

    def stop(self) -> None:
        """
        Removes the routine from the list of active routine instances, will not run in the next interval iteration.
        """
        self._service.remove_routine(self)

    #
    #
    #

    @staticmethod
    def _refetch(run: Callable, timeout_sec: int, attempts: int, return_call: bool = False) -> Optional[Any]:
        """
        Make specified fetch attempts for failed API responses. Multiply timeout time after each attempt.

        Args:
            run (Callable): The fetch function to retry.
            timeout_sec (int): Timeout duration in seconds.
            attempts (int): Number of retry attempts.
            return_call (bool): Whether to return the result of the fetch function.

        Returns:
            Optional[Any]: Result of the fetch call (if return_call is True).
        """
        if attempts == 0:
            return

        sleep_time = timeout_sec if attempts > 4 else timeout_sec * (5 - attempts)

        time.sleep(sleep_time)

        if return_call:
            return run(attempts - 1)

        run(attempts - 1)

    #
    #
    #

    @staticmethod
    def _check_idle_status(current_timestamp: int, update_timestamp: int, run_interval: Union[int, float]) -> Union[int, float]:
        """
        Check if Routine idle timeout has ended.

        Args:
            current_timestamp (int): Current timestamp.
            update_timestamp (int): Timestamp of the last routine update.
            run_interval (Union[int, float]): Routine interval in hours.

        Returns:
            Union[int, float]: Difference in hours between timestamps.
        """
        difference_in_hours = (current_timestamp - update_timestamp) / 3600
        return difference_in_hours < run_interval

    #
    #
    #

    @staticmethod
    def run_interval_decorator(interval_time) -> Callable:
        """
        Control Routine Execution Based on Intervals

        Args:
            interval_time: The index of the interval in the routine intervals list.

        Returns:
            Callable: A decorator function to control routine execution.
        """

        def decorator(func: Callable) -> Union[Callable, None]:
            @wraps(func)
            def wrapper(self, refetch_attempts: int = 5):
                run_interval = self._routine_intervals_hours[interval_time]
                current_timestamp = int(datetime.now().timestamp())

                if self._update_timestamp:
                    is_idle = self._check_idle_status(current_timestamp, self._update_timestamp, run_interval)

                    if is_idle:
                        return

                self._update_timestamp = current_timestamp
                return func(self, refetch_attempts)

            return wrapper

        return decorator
