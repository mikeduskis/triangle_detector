from datetime import datetime, timedelta
import os
from subprocess import PIPE, Popen, STDOUT
from threading import Thread

PYTHON = os.environ['PYTHON'] if 'PYTHON' in os.environ else 'python'


class Server:
    """
    Mechanism for starting and stopping the service programmatically.
    This isn't needed under ordinary operating conditions but can be
    useful for testing.
    """

    def _next_output_line(self):
        line = None

        def grab_it():
            nonlocal line
            line = next(self._stdout_lines)
        expiration = datetime.now() + timedelta(seconds=2)
        Thread(target=grab_it, daemon=True).start()
        while datetime.now() < expiration:
            if line is not None:
                return line
        raise TimeoutError('Timed out waiting for output')

    def _wait_for_start(self):
        expiration = datetime.now() + timedelta(seconds=3)
        while datetime.now() < expiration:
            if 'Running' in self._next_output_line():
                return
        raise TimeoutError('Timed out while waiting for the service to start')

    def start(self, *, port):
        self._process = Popen(
            args=[PYTHON, '-m', 'triangle_detector', str(port)],
            stdout=PIPE, stderr=STDOUT, universal_newlines=True)
        self._stdout_lines = iter(self._process.stdout.readline, '')
        self._wait_for_start()
        if self._process.returncode is not None:
            raise Exception(
                'Service failed to start\n%s' % self._process.stdin.read())

    def stop(self):
        self._process.terminate()
