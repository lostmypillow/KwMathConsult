# Reservation System API

## Development
### Prerequisites

1. See [this](https://github.com/mkleehammer/pyodbc/wiki/Install) for things to do before installing pyodbc
2. If on Linux, see [this](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Cdebian17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#17) for installing the MS ODBC 17 driver for SQL Server 
3. Create a virtual environment using the requirements.txt in this repo
4. Fill out server details in .env file


### Run Server
```bash
fastapi dev main.py
```

## Production (Docker on Linux)
### Prerequisities
1. Fill out server details in .env file
2. Make setup.sh executable
```bash
chmod +x setup.sh
```
### Run
Just run setup.sh
```bash
./setup.sh
```
## Why Docker?
"setup.sh" (and in extension "Dockerfile") contains many frivolous commands that you would've had to type line by line by hand in order to fulfill all the prerequisites (including developement prequisites and FastAPI production prequisites), **it thus ensures the ability to reproduce the same application across multiple Linux systems**

## What setup.sh actually does behind the scenes
1. setup.sh checks if Docker is installed. If not, installs Docker.
2. setup.sh checks if services are running, if not, launches Docker Compose files
3. Docker Compose builds images based on Dockerfile, which installs the second batch of requirements (SQL server drivers) to a **self-contained** container


## Authors and acknowledgment
Johnny (Lost) - jmlin0101@gmail.com