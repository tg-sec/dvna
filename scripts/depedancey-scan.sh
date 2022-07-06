#!/bin/bash

SAST_REPORT="/var/lib/jenkins/reports"
/var/lib/jenkins/dependency/bin/dependency-check.sh --scan `pwd` -f JSON -o $SAST_REPORT/depedancey-scan --prettyPrint
