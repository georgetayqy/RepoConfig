# RepoConfig

Create custom RepoSense configs and scaffolding for quick deployment!

## Requirements

There are multiple ways you can run RepoConfig on your machine: either directly using Python, or through Docker 
(recommended)!

### Python

You will need to install `Python 3.12`, and install the requirements as detailed in the [requirements.txt](requirements.txt)
file.

To install the requirements, run the following command:

```shell
pip install -r requirements.txt
```

or

```shell
pip3 install -r requirements.txt
```

if `pip` does not work.

You will also need `git` version `2.45.0` installed. Any earlier version may work, but your mileage may vary.

### Docker

Head over to the [Docker webpage](https://www.docker.com/products/docker-desktop/) and install Docker Desktop on your computer.

If you are on Windows, you may need to install Windows Subsystem Linux 2 in order for Docker to work properly.

## Usage

To run the application, run the following command:

```shell
streamlit run Home.py
```

If successful, your browser should open and you will be redirected to the app.
