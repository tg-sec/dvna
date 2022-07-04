#!/bin/bash

REPORT="/var/lib/jenkins/reports"
npm audit --json > $REPORT/npm-audit-report

echo $? > /dev/null

