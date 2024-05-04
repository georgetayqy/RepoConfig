# ________  _______   ________  ________  ________  ________  ________   ________ ___  ________
#|\   __  \|\  ___ \ |\   __  \|\   __  \|\   ____\|\   __  \|\   ___  \|\  _____\\  \|\   ____\
#\ \  \|\  \ \   __/|\ \  \|\  \ \  \|\  \ \  \___|\ \  \|\  \ \  \\ \  \ \  \__/\ \  \ \  \___|
# \ \   _  _\ \  \_|/_\ \   ____\ \  \\\  \ \  \    \ \  \\\  \ \  \\ \  \ \   __\\ \  \ \  \  ___
#  \ \  \\  \\ \  \_|\ \ \  \___|\ \  \\\  \ \  \____\ \  \\\  \ \  \\ \  \ \  \_| \ \  \ \  \|\  \
#   \ \__\\ _\\ \_______\ \__\    \ \_______\ \_______\ \_______\ \__\\ \__\ \__\   \ \__\ \_______\
#    \|__|\|__|\|_______|\|__|     \|_______|\|_______|\|_______|\|__| \|__|\|__|    \|__|\|_______|
#
# RepoConfig - Create RepoSense Configs and quickly deploy RepoSense on your machines
#
# Maintainer:       George Tay
# Version:          1.0
# License:          MIT License
#
# Dockerfile is inspired greatly by https://www.youtube.com/watch?v=DflWqmppOAg

FROM python:3.12

# default port that Streamlit runs on
EXPOSE 8501

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y build-essential software-properties-common git

WORKDIR /repoconfig
COPY . /repoconfig

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "Home.py"]
