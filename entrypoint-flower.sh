#!/bin/sh

celery --broker=redis://redis:6379/0 flower
