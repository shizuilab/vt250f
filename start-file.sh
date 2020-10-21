#!/bin/bash

pkill -SIGTERM -f youtube-
sudo systemctl stop youtube.service

sudo systemctl start filetube.service

exit 0
