# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Undocumented changes

## [0.1.0] - 2025-02-07

- Undocumented changes


## [0.2.0] - 2025-03-31

### Added
- VideoPlayer.vue from KwTouchScreen_api, no additional modifications

## [0.2.1] - 2025-04-03

### Added
- `CHANGELOG.md` for changelog
- sync_version.py to sync `package.json` version number to FastAPI constructor in `/backend/src/main.py`
- Echo version number in `run.sh`

### Changed
- Image API path cahnged from legacy to KwTouchScreen_api's '/picture' endpoint
- Moved `pyodbc.md` to root
- Moved `run.sh` to root
- Moved `README.md` from backend folder to root
- Changed all `.env` to `.env.example` and removed all values
- Frontend site name to KwMathConsult
- Bumped `package.json` version

### Removed
- Unnecessary Docker files in `/backend` folder
- Unnecessary `/backend/.vscode` folder

## [0.2.2] - 2025-04-11

### Added
- Logic in `deploy.sh` (formerly known as `run.sh`) to check for existence of `.env` in backend folder before deployment
- Response class for our only endpoint to make it clear (as clear as it can be without breaking API compatibility with RPi clients) what responses the endpoint will return

### Changed
- `run.sh` to `deploy.sh`, to make it clear it's a script for deployment
- Synced all application and website names

## Removed
- `public` folder from backend