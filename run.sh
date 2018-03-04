#!/usr/bin/env bash
pip install -r requirements.txt
python server.py collectstatic --noinput
python server.py migrate --noinput
systemctl restart nginx
systemctl restart django
supervisorctl restart all
