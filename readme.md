# Programming Assignment

This work has been implemented by Salim Fadhley. If you have any questions:
* +44 7973710574
* salimfadhley@gmail.com

## Are you using the latest version?

This project is [hosted on GitHub](https://github.com/salimfadhley/bnp_paribas_assignment_2020). Instead of downloading a zip file, why not git clone the latest viersion into your worspace?

## How to run

### With virtualenv

This approach assumes you have Python 3.8 and virtualenv. Most modern Python distributions include this tool.

```bash
cd src
./make_venv.sh
. ../venv/bin/activate
./run.sh
``` 

The expected output should look something like this:

```
INFO:tradestatus.main:Writing logs to server.log
INFO:tradestatus.main:Trade status command beginning.
INFO:tradestatus.main:Writing output to results.csv
INFO:tradestatus.main:Trade status command finished.
```

### Important scripts

* **format.sh**: Applies a number of code-formatting tools to this project's source-code.
* **make_virtualenv.sh**: Creates a new Python virtual environment.
* **run.sh**: Shows an example of how to invoke this command. Run after activating a virtual environment.
* **run_tests.sh**: Creates a new Python virtual environment. Run after activating a virtual environment.

### This project is dockerized!

If you do not want to use virtualenv (or cannot install Python 3.8), you can run the entire project from a docker container. This approach requires that you have Docker Desktop (or Docker CE on Linux hosts). It will build the Python environment

Run all the tests inside a Dockerized environment:
```bash
docker-compose run --entrypoint="/bin/bash run_tests.sh" bnp_test
```
