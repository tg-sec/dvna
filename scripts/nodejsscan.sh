#!/bin/bash

SAST_REPORTS="/var/lib/jenkins/reports"
nodejsscan --directory `pwd` --output ${SAST_REPORTS}/nodejsscan-report'
