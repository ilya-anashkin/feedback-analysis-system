#!/bin/bash

start_backend() {
  fastapi dev app/main.py
}

lint() {
  echo "Run black..."
  black app
  echo "Run isort..."
  isort app
}

calc_coverage() {
  coverage run -m pytest && coverage report
}

run_test() {
  python -m tests/
}

make_docs() {
  pdoc app -o app/docs
}

if [ "$1" == "backend" ]; then
  start_backend
elif [ "$1" == "lint" ]; then
  lint
elif [ "$1" == "test" ]; then
  run_test
elif [ "$1" == "coverage" ]; then
  calc_coverage
elif [ "$1" == "docs" ]; then
  calc_coverage
else
  echo "Unknown argument: $1"
  echo "Usage: $0 {backend|lint|test|coverage|docs}"
  exit 1
fi