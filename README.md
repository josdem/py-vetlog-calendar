# 🐍 Vetlog Calendar
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
[![GitHub](https://github.com/josdem/py-vetlog-calendar/actions/workflows/ci.yml/badge.svg)](https://github.com/josdem/py-vetlog-calendar/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=josdem_py-vetlog-calendar&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=josdem_py-vetlog-calendar)

**Installation**

1. Clone the repository

```sh
git clone https://github.com/josdem/py-vetlog-calendar
cd py-vetlog-calendar
```

2. Install the dependencies

```sh
uv sync

# To include dev dependencies (e.g., for testing):
uv sync --extra dev
```

3. (Optional) Verify installation

```sh
uv run version
```

## Usage

**Run**

```sh
# List user's token paths
uv run paths

# List users with pets with pending vaccinations
uv run users

# List pets with pending vaccinations
uv run pets

# Check pending vaccinations and create Google Calendar events
uv run vaccinations

# Check pending vaccinations and create Google Calendar events in Spanish
uv run vaccinations --language es

# List pets with pending deworming
uv run dewormings
```

**Test**

```sh
# Test everything
uv run pytest tests/unit -v

# Test a specific file
uv run pytest tests/unit/test_config.py

# Test a matching keyword
uv run pytest -k config
```

**Format**

```sh
# Check code for linting/formatting issues (does not fix)
uv run ruff check

# Format code automatically
uv run ruff format

# Automatically fix linting issues
uv run ruff check --fix
```

**Links**
- https://github.com/josdem/py-vetlog-calendar/wiki
- https://github.com/josdem/vetlog-spring-boot



## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/habartakh"><img src="https://avatars.githubusercontent.com/u/177358275?v=4?s=100" width="100px;" alt="Hajar Bartakh"/><br /><sub><b>Hajar Bartakh</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=habartakh" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://itsiiie.github.io/resume-site/"><img src="https://avatars.githubusercontent.com/u/111443349?v=4?s=100" width="100px;" alt="Shashank Singh"/><br /><sub><b>Shashank Singh</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=itsiiie" title="Code">💻</a> <a href="#infra-itsiiie" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nightcityblade"><img src="https://avatars.githubusercontent.com/u/260356847?v=4?s=100" width="100px;" alt="nightcityblade"/><br /><sub><b>nightcityblade</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=nightcityblade" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/xyaz1313"><img src="https://avatars.githubusercontent.com/u/197202025?v=4?s=100" width="100px;" alt="xyaz1313"/><br /><sub><b>xyaz1313</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=xyaz1313" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ahnewtown32"><img src="https://avatars.githubusercontent.com/u/158523418?v=4?s=100" width="100px;" alt="ahnewtown32"/><br /><sub><b>ahnewtown32</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=ahnewtown32" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://ayaanfaisal.com"><img src="https://avatars.githubusercontent.com/u/63867307?v=4?s=100" width="100px;" alt="Ayaan Faisal"/><br /><sub><b>Ayaan Faisal</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=AppleAyaan" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jtenorio-dev"><img src="https://avatars.githubusercontent.com/u/133891193?v=4?s=100" width="100px;" alt="Jomari Tenorio"/><br /><sub><b>Jomari Tenorio</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=jtenorio-dev" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/adwibha"><img src="https://avatars.githubusercontent.com/u/138350158?v=4?s=100" width="100px;" alt="Akhil"/><br /><sub><b>Akhil</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=adwibha" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://terminalchai.com/"><img src="https://avatars.githubusercontent.com/u/213856599?v=4?s=100" width="100px;" alt="Terminal Chai"/><br /><sub><b>Terminal Chai</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=terminalchai" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/paarothecoder"><img src="https://avatars.githubusercontent.com/u/212145438?v=4?s=100" width="100px;" alt="mukhiyaJI"/><br /><sub><b>mukhiyaJI</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=paarothecoder" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/josejdiaz-1970"><img src="https://avatars.githubusercontent.com/u/191517686?v=4?s=100" width="100px;" alt="josejdiaz-1970"/><br /><sub><b>josejdiaz-1970</b></sub></a><br /><a href="https://github.com/josdem/py-vetlog-calendar/commits?author=josejdiaz-1970" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!