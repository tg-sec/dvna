#!/bin/bash

SAST_REPORT="/var/lib/jenkins/reports"
retire --path `pwd` --outputformat json | jq > $SAST_REPORT/retirejs_scan
