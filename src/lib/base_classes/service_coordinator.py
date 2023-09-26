from typing import Coroutine, Any, NoReturn
from datetime import datetime
from asyncio import sleep, create_task, CancelledError

from lib.base_classes.routine import Routine
from lib.logger import Logger


class ServiceCoordinator:
    """
    Base class for service coordinators.

    This class provides a basic structure for service coordinators that manage asynchronous routines.

    Attributes:
        task: An asyncio.Task object representing the running routine task.

    Methods:
        __init__: Constructor for initializing the service coordinator. Must be implemented in child classes.

        run_service: Starts the routine by creating and running a task.
        cancel_routine: Cancels the running routine task.

        __routine: Placeholder method for implementing the actual routine logic in child classes.


        stop_service: Cancels the running service task.

        add_routine: Adds a routine to the coordinator's list of managed routines.

        remove_routine: Removes a routine from the coordinator's list of managed routines.
    """

    def __init__(self) -> None:
        """
        Constructor for initializing the service coordinator.

        This method should be implemented in child classes to set up any necessary resources.
        """
        pass

    #
    #
    #

    async def run_service(self):
        """
        Starts the service by creating and running a task.

        If the task encounters a CancelledError, it is handled gracefully.
        """
        task = create_task(self._routine())
        self._task = task

        try:
            await task

        except CancelledError:
            return

        except Exception as e:
            log = Logger(name=self.__class__.__name__)
            log.error(e)
            return

    #
    #
    #

    async def _routine(self) -> Coroutine[Any, Any, NoReturn]:
        """
        Implements the routine logic for managing Coingecko data.

        This method runs asynchronous routines that retrieve and process data, coordinating various tasks.

        It calculates sleep times based on routine intervals to manage the frequency of data retrieval.
        """
        while True:
            start_time = datetime.now()
            for routine in self.routines.values():
                routine.run()
            end_time = datetime.now()

            elapsed_time_seconds = (end_time - start_time).total_seconds()

            sleep_time = max(self._routine_interval_sec - elapsed_time_seconds, 0)

            await sleep(sleep_time)

    #
    #
    #

    def stop_service(self) -> None:
        """
        Cancels the running service task.

        If a task is running, it will be canceled.
        """
        if self._task:
            self._task.cancel()

    #
    #
    #

    def add_routine(self, routine: Routine) -> None:
        """
        Adds a routine to the coordinator's list of managed routines.

        Args:
            routine: An instance of a routine class.
        """
        self.routines[routine.__class__.__name__] = routine

    #
    #
    #

    def remove_routine(self, routine: Routine) -> None:
        """
        Removes a routine from the coordinator's list of managed routines.

        Args:
            routine: An instance of a routine class.
        """
        del self.routines[routine.__class__.__name__]
