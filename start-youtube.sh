#!/bin/bash

sudo pkill -SIGTERM -f file-
sudo systemctl stop filetube.service

sudo systemctl start youtube.service

exit 0
