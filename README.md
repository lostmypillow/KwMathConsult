# Reservation System API
- [Reservation System API](#reservation-system-api)
  - [Project Structure](#project-structure)
  - [Development](#development)
  - [Production](#production)
  - [Q\&A](#qa)
    - [Why Docker?](#why-docker)
    - [What does setup.sh actually do behind the scenes?](#what-does-setupsh-actually-do-behind-the-scenes)
  - [Authors](#authors)

## Project Structure
```
.
└── [root folder]/
    ├── .vscode
    ├── documentation
    │   ├── index.html         # Open this file for docs!
    │   └── [other html files] # IGNORE!
    ├── src/
    │   ├── __init__.py
    │   ├── cardholder.py
    │   ├── database.py
    │   ├── device.py
    │   ├── main.py
    │   └── test_main.py
    ├── .env
    ├── .gitignore
    ├── docker-compose.debug.yml
    ├── docker-compose.yml
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt
    └── setup.sh

```
- FastAPI's documentation is at the "/docs" endpoint when you [run the dev server](#run-dev-server).
- Alternatively, launch pdoc via `pdoc src` in the terminal.
- Run `pdoc src -o ./documentation` after creating a virtual environment to generate the pdoc HTML files after a change in any source files.

## Development

1. See [this](https://github.com/mkleehammer/pyodbc/wiki/Install) for things to do before installing pyodbc with pip
   
2. If on Linux, see [this](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Cdebian17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#17) for installing the MS ODBC 17 driver for SQL Server 

3. Create a virtual environment using the requirements.txt in this repo
- On VSCode: Ctrl/Command + Shift + P > Select Python:Create Environment > Check requirements.txt when prompted

- On PyCharm: It should automatically prompt you to install prerequisites from requirements.txt

- If all else fails, on Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate

# and for when you want to exit the venv:
deactivate
```

4. [Install Docker](https://docs.docker.com/engine/install/). [Why Docker?](#why-docker)

5. Fill out server details in the .env file

6. Run Dev Server

```bash
fastapi dev main.py
```

 - FastAPI might not shutdown correctly (release ports) even after you Control+C. Just kill the running Python process (using Task Manager in Windows or `kill [insert python process PID here]` in Linux)
  
- If you're using VSCode, just click Run & Debug, it will start a Docker Debug session as defined in docker-compose.debug.yml. Might lose the hot reload, but it's more controllable and reproducible than `fastapi dev` command.


## Production

1. Fill out server details in .env file
   
2. Make setup.sh executable
   
```bash
chmod +x setup.sh
```

3. Run setup.sh
   
```bash
./setup.sh
```

## Q&A

### Why Docker?
**Docker ensures the ability to reproduce the same application across different operating systems.** It's especially needed here with all the prerequisites to pyodbc and all that.



### What does setup.sh actually do behind the scenes?
"setup.sh" (and in extension "Dockerfile") contains many frivolous commands that you would've had to type in order to fulfill all the prerequisites (including [developement prequisites](#prerequisites) and FastAPI production prequisites

Essentially: 
1. setup.sh checks if Docker is installed. If not, installs Docker.
2. setup.sh checks if services are running, if not, uses `docker-compose` to run the docker-compose.yml file
3. `docker-compose` builds images based on Dockerfile, which installs the 2 batches of requirements (SQL server drivers and python requirements) and launches the container.


## Authors
Johnny (Lost) - jmlin0101@gmail.com