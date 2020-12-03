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

## Development

* Requirements: poetry, pyenv

```sh
poetry install

poetry publish

pip install --no-cache-dir --upgrade jupyter-autotime
```
