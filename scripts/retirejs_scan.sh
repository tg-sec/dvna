#!/bin/bash

SAST_REPORT="/var/lib/jenkins/reports"
retire --path `pwd` --outputformat json --exitwith 0 | jq > $SAST_REPORT/retirejs_report

