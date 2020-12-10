# jupyter-autotime

Display elapsed time on Jupyter.

![Demo](demo.gif)

## Getting start

1. Install
   * On shell.

      ```sh
      pip install jupyter-autotime
      ```

   * On Jupyter.

      ```python
      !pip install jupyter-autotime
      ```

1. Enable autotime

   ```python
   %load_ext autotime
   ```

## Other usage

```python
# Reload.
%reload_ext autotime

# Disable.
%unload_ext autotime
```

## Customization

* First, import the module to hack `autotime`.

   ```python
   import autotime
   ```

* Customize timespan format.

   ```python
   def my_format_timepan(timespan: float) -> str):
      """My custom timespan format."""
      # e.g. '12 sec'
      return '{} sec'.format(int(timespan))
   autotime.format_timespan = my_format_timepan
   ```

* Customize time format.

   ```python
   # e.g. '2020/12/10 16:15:11'
   autotime.TIME_FORMAT = '%Y/%m/%d %H:%M:%S'
   ```

* Customize output format.

   ```python
   # e.g. '[RUNNING] 3.09 s (2020-12-10T15:58:35)'
   autotime.RUNNING_FORMAT = '[RUNNING] {timespan} ({start})'
   # e.g. '[FINISH] 4.02 s (2020-12-10T15:59:54~2020-12-10T15:59:58)'
   autotime.FINISHED_FORMAT = '[FINISH] {timespan} ({start}~{end})'
   ```

* Customize units.

   ```python
   # e.g. 5 分 7 秒
   autotime.set_units(sec='秒', min='分', hr='時間', d='日')
   ```

* Customize output with method.

   ```python
   def my_format_output(timespan: float,
                        start_time: time.struct_time,
                        end_time: float = None,
                        is_finished: bool = False):
      """My Custom output format."""
      if is_finished:
         # e.g. 'Finished. 2.0160000000032596'
         return 'Finished. {}'.format(timespan)
      else:
         # e.g. 'Running... 1.0159999999887077'
         return 'Running... {}'.format(timespan)


   autotime.format_output = my_format_output
   ```

   * You can access below objects on custom `format_output`.
      * `autotime.UNITS (dict)`
      * `autotime.format_time (method)`
      * `autotime.TIME_FORMAT (str)`
      * `autotime.RUNNING_FORMAT (str)`
      * `autotime.FINISHED_FORMAT (str)`

## Development

* Requirements: poetry, pyenv

```sh
poetry install

poetry publish

pip install --no-cache-dir --upgrade jupyter-autotime
```
