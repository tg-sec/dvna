#!/bin/bash

SAST_REPORT="/var/lib/jenkins/reports"
dependency-check --scan `pwd` -f JSON -o $SAST_REPORT/depedancey-scan --prettyPrint
