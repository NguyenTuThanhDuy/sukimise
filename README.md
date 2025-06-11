# Install
```
    $ pip install mypy yapf pre-commit isort flake8
```

# Before commit

```
    pytest
    coverage html
    open htmlcov/index.html
    coverage json -q -o /dev/stdout | jq .totals.percent_covered
```

```
    $ pre-commit run --all-files
```

```
    $ mypy app/
```
