#!/usr/bin/env python3

"""
Doodle Reminder
Copyright (c) 2016 Angelo Licastro
See LICENSE and README.md.
"""

from os import _exit
from os.path import basename
from traceback import print_exc

try:
    import config
except ImportError as e:
    print('%s: The configuration file is missing.' % basename(__file__))
    print('%s: Please check that config is not missing.' %
    (basename(__file__)))
    _exit(0)
except SyntaxError as e:
    print('%s: config is malformed.' % basename(__file__))
    print_exc()
    print('%s: Please fix the above syntax error.' % (basename(__file__)))
    _exit(0)

from argparse import ArgumentParser

try:
    from bs4 import BeautifulSoup
except ImportError as e:
    print('%s: bs4 is a required dependency.' % basename(__file__))
    print('%s: Please install the required bs4 dependency to continue.' %
    basename(__file__))
    _exit(0)

from json import loads
from re import match, search

try:
    from requests import get, post
except ImportError as e:
    print('%s: requests is a required dependency.' % basename(__file__))
    print('%s: Please install the required requests dependency to continue.' %
    basename(__file__))
    _exit(0)

from sys import argv

def isValidDoodlePoll(url):
    """Returns True if url is probably a valid Doodle poll, False otherwise."""
    return (match('http(s)?://(www.)?doodle\.com/poll/.+', url) and
    get(url).status_code == 200)

def isProbableSMSGateway(emailAddress):
    """Returns True if emailAddress is probably a SMS gateway, False
    otherwise.
    """
    return match('\d{10}@.+', emailAddress)

def getJSON(beautifulSoup):
    """Returns a JSON object containing poll information.

    WARNING: This function is volatile. The position of the <script> tag
    containing the JSON object containing poll information is subject to
    change.
    """
    s = beautifulSoup.find_all('script')[15].encode('utf-8')
    return loads(search(b'{"poll":.+}', s).group(0).decode('utf-8'))

def main():
    parser = ArgumentParser(description='Reminds people who have not \
    participated in a Doodle poll to participate in it.')
    parser.add_argument('url', help='The URL of a valid Doodle poll.')
    args = parser.parse_args()

    if not isValidDoodlePoll(args.url):
        print('%s: %s is probably not a valid Doodle poll.' %
        (basename(__file__), args.url))
        _exit(0)

    html = get(args.url).text
    beautifulSoup = BeautifulSoup(html, 'html.parser')
    j = getJSON(beautifulSoup)

    participantsNames = list()
    for participant in j['poll']['participants']:
        participantsNames.append(participant['name'])
    try:
        expectedParticipantsNames = list(config.expectedParticipants.keys())
    except AttributeError as e:
        print('%s: Something went wrong. config.expectedParticipants is \
        probably empty.' % basename(__file__))
        _exit(0)
    nonParticipantsNames = list(set(expectedParticipantsNames) -
    set(participantsNames))
    nonParticipants = len(nonParticipantsNames)
    title = j['poll']['title']

    if nonParticipants == 0:
        print('%s: Everyone has already participated in the %s poll.' %
        (basename(__file__), title))
        _exit(0)
    else:
        print('%s: Reminding %d %s to participate in the %s poll...' %
        (basename(__file__), nonParticipants, 'person' if nonParticipants == 1
        else 'people', title))

    for nonParticipantName in nonParticipantsNames:
        print('%s: Reminding %s...' % (basename(__file__), nonParticipantName),
        end=' ')
        for emailAddress in config.expectedParticipants[nonParticipantName]:
            post('%s/messages' % config.mailgunAPIBaseURL,
                auth = ('api', config.mailgunAPIKey),
                data = {
                    'to': '%s' % emailAddress,
                    'from': '%s <%s>' % (config.mailgunSMTPLoginName,
                    config.mailgunSMTPLogin),
                    'subject': None if isProbableSMSGateway(emailAddress) else
                    config.reminderEmailSubject % title,
                    'text': config.reminderEmailText % (nonParticipantName,
                    args.url)
                });
        print('Done.')
    print('%s: %d %s has been reminded to participate in the %s poll.' %
    (basename(__file__), nonParticipants, 'person' if nonParticipants == 1 else
    'people', title))

if __name__ == '__main__':
    main()
