#!/bin/bash
export PROD=TRUE
source venv/bin/activate
pgrep gunicorn | xargs kill
gunicorn index:app 
