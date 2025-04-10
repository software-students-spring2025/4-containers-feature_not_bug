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

### Setting Up the Web App

1. Clone the repository:

 ```bash
   git clone https://github.com/software-students-spring2025/4-containers-feature_not_bug.git 
 ```
2.
3.
4. Create a .env file

### Setting Up the Machine Learning Client

### Seeting up the Database

### Running tests
To ensure everything is working as expected, you can run the tests for both parts of the application.

**Web App Tests**
In the web-app directory, run:

```bash
pytest
```

**Machine Learning Client Tests**
In the machine-learning-client directory, run:

``` bash
pytest
```
