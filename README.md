# GoDutch!: The Receipt Splitter App

![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Machine Learning Client Build Status](https://github.com/software-students-spring2025/4-containers-feature_not_bug/actions/workflows/mach-learn-test.yml/badge.svg)
![Web App Build Status](https://github.com/software-students-spring2025/4-containers-feature_not_bug/actions/workflows/web-app-test.yml/badge.svg)

GoDutch is an innovative app that allows users to seamlessly split restaurant bills among multiple people. The app utilizes a machine learning client to extract data from receipts, including dishes, taxes, and tips. After uploading or taking a picture of a receipt, users can input the number of people splitting the bill and describe what each person ordered. The app then allocates the tax and tip proportionally among the dishes.

## Team Members

- [Shamaamah Ahmad](https://github.com/shamaamahh)
- [Marcos Huh](https://github.com/mh6355)
- [Maya Humston](https://github.com/mayhumst)
- [Tarini Mathur](https://github.com/tmathur2005)

## Project Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python 3.x** (for the machine learning client) - [Install Python 3.x](https://www.python.org/downloads/)
- **pip** (Python package installer) - [Install pip](https://pip.pypa.io/en/stable/)
- **Git** (for version control) - [Install Git](https://git-scm.com/)

### How to Run this Project

1. Clone the repository and cd to the location where you have saved the repo :

 ```bash
git clone https://github.com/software-students-spring2025/4-containers-feature_not_bug.git 
cd path_to_your_repo_copy
 ```
2. Run the Machine Learning Client:

```bash
cd machine-learning-client
pipenv install
pipenv run python app.py
```
This starts the ML service on http://localhost:5001.

3. Run the Web App:

```bash
cd web-app
pipenv install
pipenv run python app.py
```
This starts the frontend server on http://localhost:5000.

4. Create a .env file inside the web-app directory (and machine-learning-client if needed). Here is an example:

```dotenv
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
MONGO_DBNAME="dutch_pay" 
```

### Running Tests
To ensure everything is working as expected, you can run the tests for both parts of the application.

**Web App Tests**

```bash
cd web-app
pipenv run pytest
```

**Machine Learning Client Tests**

``` bash
cd machine-learning-client
pipenv run pytest
```

### Additional Information

- Be sure to run both servers at the same time to fully test functionality.
- All secrets and credentials should live in .env files (not committed).
