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
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
RUNNING_FORMAT = '⌛ {timespan} ({start})'
FINISHED_FORMAT = '✔️ {timespan} ({start}/{end})'


def set_units(**units):
    """Set units.

    Args:
        d (str, optional): Day.
        hr (str, optional): Hour.
        min (str, optional): Minute.
        sec (str, optional): Second.
        ms (str, optional): Millisecond.
        micro (str, optional): Microsecond.
        nano (str, optional): Nanosecond.
    """
    for k, v in units.items():
        if k not in UNITS.keys():
            raise ValueError(f'Unknown unit: "{k}"')
        if not isinstance(v, str):
            raise ValueError(f'Unit must be string. "{k}" is {type(v)}.')
        UNITS[k] = v


def format_timespan(timespan):
    """Format time span.

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

    units = [UNITS[k] for k in ['sec', 'ms', 'micro', 'nano']]
    scaling = [1, 1e3, 1e6, 1e9]

    if timespan > 0.0:
        order = min(-int(math.floor(math.log10(timespan)) // 3), 3)
    else:
        order = 3
    return '%.*g %s' % (3, timespan * scaling[order], units[order])


def format_output(timespan, start_time, end_time=None, is_finished=False):
    """Format output.

    Args:
        timespan (float): Time span.
        start_time (time.struct_time): Start time.
        end_time (time.struct_time, optional): End time.
        is_finished (bool, optional): Is finished. Default to False.

    Returns:
        str: Output string.
    """
    timespan_str = format_timespan(timespan)
    start_time_str = time.strftime(TIME_FORMAT, start_time)
    if is_finished:
        end_time_str = time.strftime(TIME_FORMAT, end_time)
        return FINISHED_FORMAT.format(timespan=timespan_str,
                                      start=start_time_str,
                                      end=end_time_str)
    else:
        return RUNNING_FORMAT.format(timespan=timespan_str,
                                     start=start_time_str)


class Timer():
    """Timer."""

    __slots__ = [
        'start_monotonic',  # float
        'start_time',  # time.struct_time
        'output',  # IPython.core.display.DisplayHandle
        'running',  # bool
        'worker',  # threading.Thread
    ]

    UPDATE_DURATION = 0.11

    def _update_output(self, text):
        """Update output.

        Args:
            text (str): Display text.
        """
        self.output.update(HTML(f'<pre>{text}</pre>'))

    def _run_loop(self):
        """Run counter."""
        self.running = True

        self.start_time = time.localtime()
        self.start_monotonic = time.monotonic()
        while self.running:
            timespan = time.monotonic() - self.start_monotonic
            output = format_output(timespan, self.start_time)
            self._update_output(output)
            time.sleep(self.UPDATE_DURATION)

    def start(self):
        """Start timer."""
        self.output = display(HTML('<pre></pre>'), display_id=True)
        self.worker = threading.Thread(target=self._run_loop)
        self.worker.start()

    def stop(self):
        """Stop timer."""
        timespan = time.monotonic() - self.start_monotonic
        end_time = time.localtime()
        self.running = False

        while self.worker.is_alive():
            pass

        output = format_output(timespan,
                               self.start_time,
                               end_time,
                               is_finished=True)
        self._update_output(output)

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
