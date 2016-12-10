#!/usr/bin/env bash

# obtains all data tables from database
./manage.py dumpdata demo.user --format json > evaluation/user.json
./manage.py dumpdata demo.candidate --format json > evaluation/candidate.json
./manage.py dumpdata demo.interview --format json > evaluation/interview.json
./manage.py dumpdata demo.transcript --format json > evaluation/transcript.json
./manage.py dumpdata demo.postsurvey --format json > evaluation/postsurvey.json
./manage.py dumpdata demo.presurvey --format json > evaluation/presurvey.json
./manage.py dumpdata demo.feedback --format json > evaluation/feedback.json
./manage.py dumpdata demo.recruiter --format json > evaluation/recruiter.json