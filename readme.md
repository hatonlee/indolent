# indolent
A python app for tracking habits. Interface using tkinter, sqlite via SQLAlchemy for data storage.

### Useful links
- [Changelog](/CHANGELOG.md)
- [App requirements](/docs/requirements.md) <br>
- [Time tracking](/docs/timetracking.md)
- [AI Usage](/docs/ai.md)

### Installation

1. Setup dependencies:

```bash
poetry install
```

2. Start the app:

```bash
poetry run invoke start
```

### Testing

- Run unit tests:

```bash
poetry run invoke coverage-raport
```
This generates a report to the directory [htmlcov](/htmlcov).
