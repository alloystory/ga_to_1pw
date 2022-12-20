#!/bin/bash
mkdir -p $(pwd)/google_auth_pb/
protoc --python_out=google_auth_pb google_auth.proto
