# HealthcarePlanMarketplace
Example Healthcare Plan Marketplace 
based on https://homework.adhoc.team/slcsp/

## Summary

The Healthcare Plan Marketplace application is designed to 
manage and query healthcare plans and ZIP code mappings to rate areas. 
It allows users to determine the Second Lowest Cost Silver Plan (SLCSP) 
based on the ZIP code provided. 
The application handles multiple entries for ZIP codes, 
ensuring accurate mapping to rate areas, states, county codes, and plan names.

## Features

- Reading and parsing CSV files for ZIP codes and healthcare plans.
- Mapping ZIP codes to corresponding rate areas, including handling multiple entries per ZIP code.
- Filtering healthcare plans based on rate area, state, and metal level.
- Determining the SLCSP for a given ZIP code by sorting filtered plans by their rates.

## How to Run

### Running the Application

To run the Healthcare Plan Marketplace application, you can use the provided `run.sh` script or execute a Docker command directly if Docker is installed on your system. The application expects two CSV files: one for ZIP codes and one for healthcare plans, which should be present in the current directory or specified paths.

Using the `run.sh` Script:

Make sure the `run.sh` script is executable:

```bash
chmod +x run.sh
```

Then, execute the script:

```
./run.sh
```

Using Docker Command Directly:

```bash
docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.11 python app.py
```

### Running the Tests

To run the tests for the Healthcare Plan Marketplace application, you can use the provided test.sh script or execute a Docker command directly.

Using the test.sh Script:

Ensure the test.sh script is executable:

```bash
chmod +x test.sh
```

Then, execute the script:

```bash
./test.sh
```

Using Docker Command Directly for Tests:

```bash
docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.11 python -m unittest test_app.py
```

## Dependencies

- Python 3.11
- Docker

Ensure Docker is installed and running on your system to use the provided scripts or commands.


## Note

The application assume that the CSV files zips.csv, plans.csv and slcsp.csv are located in the current working directory. Adjust the paths in the application code if your files are located elsewhere.

