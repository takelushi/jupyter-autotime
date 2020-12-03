"""jupyter-autotime."""

import threading
import time

from IPython.core.magics.execution import _format_time
from IPython.display import clear_output, display, HTML

LAB = False


class Timer():
    """Timer."""

    __slots__ = ['start_time', 'start_time_str', 'output', 'running', 'worker']

    TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
    UPDATE_DURATION = 0.11

    def _get_now_str(self):
        """Get current time string.

        Returns:
            str: Current time string.
        """
        return time.strftime(self.TIME_FORMAT, time.localtime())

    def _get_formatted_delta(self):
        """Get formatted time delta.

        Returns:
            str: Formatted time delta.
        """
        return _format_time(time.monotonic() - self.start_time)

    def _update_output(self, text):
        """Update output.

        Args:
            text (str): Display text.
        """
        self.output.update(HTML(f'<pre>{text}</pre>'))

    def _run_loop(self):
        """Run counter."""
        self.running = True
        self.start_time_str = self._get_now_str()
        self.start_time = time.monotonic()
        while self.running:
            self._update_output('⌛ {} ({})'.format(self._get_formatted_delta(),
                                                   self.start_time_str))
            time.sleep(self.UPDATE_DURATION)

    def start(self):
        """Start timer."""
        print(LAB)
        self.output = display(display_id=True)
        if not LAB:
            self.output.display(HTML('<pre></pre>'))
        self.worker = threading.Thread(target=self._run_loop)
        self.worker.start()

    def stop(self):
        """Stop timer."""
        delta_str = self._get_formatted_delta()
        end_time_str = self._get_now_str()
        self.running = False

        while self.worker.is_alive():
            pass

        self._update_output('✔️ {} ({}/{})'.format(delta_str,
                                                   self.start_time_str,
                                                   end_time_str))

    def clear(self):
        """Clear timer."""


timer = Timer()
start, stop = timer.start, timer.stop


def load_ipython_extension(ip):
    """Call with %load_ext <NAME>.

    Args:
        ip: IPython Shell.
    """
    start()
    ip.events.register('pre_run_cell', start)
    ip.events.register('post_run_cell', stop)


def unload_ipython_extension(ip):
    """Call with %unload_ext <NAME>.

    Args:
        ip: IPython Shell.
    """
    stop()
    clear_output()
    ip.events.unregister('pre_run_cell', start)
    ip.events.unregister('post_run_cell', stop)
