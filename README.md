# Doodle Reminder

Doodle Reminder is a script that reminds people who have not participated in a Doodle poll to participate in it.

## Requirements

* Python 3
* Beautiful Soup
* Requests
* A Mailgun account

## Installation

    git clone https://github.com/angelolicastro/doodle-reminder.git
    cd doodle-reminder
    cp config.example.py config.example

## Configuration

Each expected participant has an entry in `config.expectedParticipants` (a `dict`) where the key (a `str`) is the name of the expected participant and the value (a `list`) is the email address(es) of the expected participant. An email with the subject of `config.reminderEmailSubject` and the text of `config.reminderEmailSubject` will be sent to each nonparticipant's email address(es) using the Mailgun API.

## Usage

    doodle-reminder.py [-h] url

## Example

    $ python3 doodle-reminder.py http://doodle.com/poll/bspa6scnxhdaqecy
    doodle-reminder.py: Reminding 1 person to participate in the Monthly Meeting poll...
    doodle-reminder.py: Reminding Gary Host... Done.
    doodle-reminder.py: 1 person has been reminded to participate in the Monthly Meeting poll.

## License

[The MIT License (MIT)](LICENSE)

Copyright (c) 2016 [Angelo Licastro](http://angelolicastro.com)
