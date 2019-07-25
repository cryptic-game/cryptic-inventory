#!/bin/sh

coverage run -m unittest discover -v tests
coverage report
coverage erase
