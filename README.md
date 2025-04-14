# GoDutch!: The Receipt Splitter App

![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Machine Learning Client Build Status](https://github.com/software-students-spring2025/4-containers-feature_not_bug/actions/workflows/mach-learn-test.yml/badge.svg)
![Web App Build Status](https://github.com/software-students-spring2025/4-containers-feature_not_bug/actions/workflows/web-app-test.yml/badge.svg)

GoDutch is an innovative app that allows users to seamlessly split restaurant bills among multiple people. The app utilizes a machine learning client to extract data from receipts, including dishes, taxes, and tips. After uploading or taking a picture of a receipt, users can input the number of people splitting the bill and describe what each person ordered. The app then allocates the tax and tip proportionally among the dishes.

## Table of Contents
- [Team Members](#team-members)
- [Project Setup Instructions](#project-setup-instructions)
  - [Prerequisites](#prerequisites)
  - [How to Run this Project - No Docker](#how-to-run-this-project---no-docker)
    - [Running Tests](#running-tests)
  - [How to Run this Project - With Docker](#how-to-run-this-project---with-docker)
    - [Prerequisites](#prerequisites-1)
    - [Running the App with Docker](#running-the-app-with-docker)
  - [Additional Information](#additional-information)

## Team Members

- [Shamaamah Ahmad](https://github.com/shamaamahh)
- [Marcos Huh](https://github.com/mh6355)
- [Maya Humston](https://github.com/mayhumst)
- [Tarini Mathur](https://github.com/tmathur2005)

## Project Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python 3.x** - [Install Python 3.x](https://www.python.org/downloads/)
- **pip** (Python package installer) - [Install pip](https://pip.pypa.io/en/stable/)
- **Git** (for version control) - [Install Git](https://git-scm.com/)
- **Tesseract** (To run the machine learning client)
  - Install with `sudo apt-get install -y tesseract-ocr`


Additionally, create a .env file inside BOTH the web-app directory and the machine-learning-client directory. Here is an example:

```dotenv
MONGO_URI=mongodb+srv://[username]:[password]@[cluster].mongodb.net/dbname
MONGO_DBNAME="[database_name]" 

# ML Client Configuration
TESSERACT_PATH=/usr/bin/tesseract
```

**IMPORTANT:** If you are running the Docker version of this project, add this value to the .env:

```dotenv
ML_CLIENT=ml-client
```

Populate these variables with true values specific to your cluster, following this format. 

---
### How to Run this Project - No Docker

1. Clone the repository and cd to the location where you have saved the repo :

 ```bash
git clone https://github.com/software-students-spring2025/4-containers-feature_not_bug.git 
cd path_to_your_repo_copy
 ```
2. Open one terminal to run the Machine Learning Client:

```bash
cd machine-learning-client
pipenv install
pipenv run python app.py
```
This starts the ML service on http://localhost:4999.

3. Open a second terminal to run the Web App:

```bash
cd web-app
pipenv install
pipenv run python app.py
```
This starts the frontend server on http://localhost:5000.


#### Running Tests
To ensure everything is working as expected, you can run the pytests for both parts of the application.

**Web App Tests**

```bash
cd web-app
pipenv run python -m pytest
```

**Machine Learning Client Tests**

``` bash
cd machine-learning-client
pipenv run python -m pytest
```

---
### How to Run this Project - With Docker

You can containerize and run the entire application using Docker and Docker Compose

#### Prerequisites
Make sure you have the following installed:
- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)

#### Running the App with Docker

To spin up both the machine learning client and webapp in containers:

``` bash
git clone https://github.com/software-students-spring2025/4-containers-feature_not_bug.git
cd 4-containers-feature_not_bug
docker-compose up --build
```

This will:
- Build both the ML Client and Web App containers,
- Start the services on the default ports:
  - web-app: http://localhost:5000
  - ml-client: http://localhost:4999
 

**Stopping the containers**

When you're done:

```bash
docker-compose down
```

---
### Additional Information

- Be sure to run both servers at the same time to fully test functionality.
- All secrets and credentials should live in .env files (not committed).
