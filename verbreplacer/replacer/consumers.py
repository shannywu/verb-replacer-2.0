import logging
import json
from channels.sessions import channel_session
# from replacer.models import TranslateRequest
from replacer.main import rv_main

log = logging.getLogger(__name__)


@channel_session
def ws_connect(message):
    prefix = message['path'].strip('/').split('/')[0]
    if prefix != 'replace':
        log.debug('invalid ws path=%s', message['path'])
        return


@channel_session
def ws_receive(message):
    def reply_json(status, content):
        msg = {'type': status, 'content': content}
        message.reply_channel.send({'text': json.dumps(msg)})
    data = json.loads(message['text'])

    for status, content in rv_main(data['text']):
        reply_json(status, content)
