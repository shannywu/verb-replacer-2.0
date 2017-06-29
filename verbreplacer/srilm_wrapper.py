#/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import subprocess
import os
import fcntl
import shlex
import sys
import re

score_re = re.compile('(\S+)=\s*(-*\d+)')

# command = 'java -mx2048m -cp "%s": edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -tokenized -escaper edu.stanford.nlp.process.PTBEscapingProcessor -outputFormat wordsAndTags,penn,typedDependenciesCollapsed -outputFormatOptions basicDependencies "%s" -' % (parser_path, model_path)

def _convert_result_to_list(result):
    tokens = ', '.join(result.strip().splitlines()[1:]).split(', ')
    input_info = [item.split(' ')[::-1] for item in tokens[:-1]]
    info = {k: int(v) for k, v in input_info}
    info.update((key, float(val)) for key, val in score_re.findall(tokens[-1]))

    return info

def _parse_wrapper(scorer):
    def __wrapper(self, text, raw=False):
        text = text.strip()
        if not text:
            return b'' if raw else ''

        result = scorer(self, text)

        if raw:
            return result.strip()
        else:
            res = _convert_result_to_list(result)
            return res
    return __wrapper

class NgramScorer:

    @staticmethod
    def set_nonblock_read(output):
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def __init__(self, path_to_lm='srilm-1.7.2/big.lm', arguments=[]):
        # DEVNULL = open(os.devnull, 'wb')
        # outputFormat: wordsAndTags, penn, typedDependencies
        args = shlex.split('-ppl - -lm {0} -debug 1'.format(path_to_lm))
        self._scorer = subprocess.Popen(['ngram'] + args,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                                        # stderr=DEVNULL)
        # NgramScorer.set_nonblock_read(self._scorer.stdout)

    @_parse_wrapper
    def score(self, text):
        self._scorer.stdin.write('{0}\n'.format(text).encode('utf-8'))
        self._scorer.stdin.flush()

        result = ''
        while True:
            try:
                result += self._scorer.stdout.readline().decode('utf-8')
            except:
                continue
            if result and result[-2:] == '\n\n':
                return result
