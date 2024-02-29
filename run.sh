#!/bin/bash
docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.11 python app.py
