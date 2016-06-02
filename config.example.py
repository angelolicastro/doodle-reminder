"""
Doodle Reminder
Copyright (c) 2016 Angelo Licastro
See LICENSE and README.md.
"""

expectedParticipants = {
    'Gary Host': [
        'ghost@mailinator.com',
        'XXXXX@XXXXX.XXX'
    ]
};

mailgunAPIBaseURL = 'https://api.mailgun.net/v3/XXXXX.XXX'
mailgunAPIKey = 'key-XXXXX'
mailgunSMTPLogin = 'XXXXX@XXXXX.XXX'
mailgunSMTPLoginName = 'XXXXX'

# You may use %s to represent the title of the Doodle poll.
reminderEmailSubject = 'Please Complete the %s Doodle'

# You may use %s to represent the name of the nonparticipant and the URL of the
# Doodle poll, respectively.
reminderEmailText = '%s: This is an automated reminder to please complete the \
following Doodle: %s'
