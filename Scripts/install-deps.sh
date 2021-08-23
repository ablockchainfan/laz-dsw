#!/bin/bash

set -o errexit
set -o verbose

# Install local CDK CLI version
npm install

# Install project dependencies
pip install -r requirements.txt 
