# Reservation System API

## Prerequisites
1. See [this](https://github.com/mkleehammer/pyodbc/wiki/Install) for things to do before installing pyodbc
2. If on Linux, see [this](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Cdebian17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#17) for installing the MS ODBC 17 driver for SQL Server 
3. Create a virtual environment using the requirements.txt in this repo


## Development Server
```bash
fastapi dev main.py
```

## Production (Docker)
```bash
docker-compose up -d
```

## Authors and acknowledgment
Johnny (Lost) - jmlin0101@gmail.com