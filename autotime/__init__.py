"""jupyter-autotime."""

import math
import threading
import time

from IPython.display import clear_output, display, HTML

UNITS = {
    'nano': 'ns',  # nanosecond
    'micro': 'µs',  # microsecond
    'ms': 'ms',  # millisecond
    'sec': 's',  # second
    'min': 'min',  # minute
    'hr': 'h',  # hour
    'd': 'd',  # day
}


def format_time(timespan):
    """Format elapsed time.

    Args:
        timespan (float): Time span.

    Returns:
        str: Formatted string.
    """
    if timespan >= 60.0:
        parts = [(UNITS['d'], 60 * 60 * 24), (UNITS['hr'], 60 * 60),
                 (UNITS['min'], 60), (UNITS['sec'], 1)]
        time = []
        leftover = timespan
        for suffix, length in parts:
            value = int(leftover / length)
            if value > 0:
                leftover = leftover % length
                time.append(u'%s %s' % (str(value), suffix))
            if leftover < 1:
                break
        return ' '.join(time)

    units = [
        UNITS['sec'],
        UNITS['ms'],
        UNITS['micro'],
        UNITS['nano'],
    ]

    scaling = [1, 1e3, 1e6, 1e9]

    if timespan > 0.0:
        order = min(-int(math.floor(math.log10(timespan)) // 3), 3)
    else:
        order = 3
    return '%.*g %s' % (3, timespan * scaling[order], units[order])


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
        return format_time(time.monotonic() - self.start_time)

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
        self.output = display(HTML('<pre></pre>'), display_id=True)
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
