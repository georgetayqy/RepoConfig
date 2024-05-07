#!/bin/bash

sudo yum update
sudo yum install docker git -y
sudo systemctl start docker
git clone https://github.com/asdfghjkxd/RepoConfig
cd RepoConfig
sudo docker build -t asdfghjklxd/repoconfig:latest .
sudo docker run -it -p 8501:8501 asdfghjklxd/repoconfig
