#!/bin/bash

set -x
SAST_REPORT="/var/lib/jenkins/reports"
auditjs ossi --json > $SAST_REPORT/auditjs_Reports
