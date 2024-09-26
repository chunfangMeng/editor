#!/bin/bash
cp template.env .env
uvicorn main:app --host 0.0.0.0 --port 9099 --reload --workers 1
