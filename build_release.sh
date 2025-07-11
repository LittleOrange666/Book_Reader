#!/bin/bash
if [ -z $1 ]; then
  echo "version is required for the release build"
  echo "Usage: $0 <version>"
else
  echo "Building version $1"
  docker build . -t littleorange666/book_reader:$1 --no-cache | exit 1
  echo "Pushing version $1"
  docker push littleorange666/book_reader:$1
  echo "Building latest"
  docker build . -t littleorange666/book_reader:latest | exit 1
  echo "Pushing latest"
  docker push littleorange666/book_reader:latest
fi