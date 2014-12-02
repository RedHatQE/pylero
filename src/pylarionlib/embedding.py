#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import re

import yaml

# Implement internals of embedding SimpleTestPlan and SimpleTestRun
# specific data into text and parsing them back. See interface.py.


_COMMON_EMBEDDING_TITLE = 'pylarion-structured-field'
_START = 'start'
_END = 'end'
_EMBEDDING_START = '[{}-{}]'.format(_COMMON_EMBEDDING_TITLE, _START)
_EMBEDDING_END = '[{}-{}]'.format(_COMMON_EMBEDDING_TITLE, _END)


def _yamlToText(yamlObjectToEmbed, prefix, suffix):
    
    if not prefix:
        prefix = ''

    if not suffix:
        suffix = ''
         
    return '{}{}\n{}{}\n{}'.format(
                                   prefix,
                                   _EMBEDDING_START,
                                   yaml.dump(yamlObjectToEmbed, default_flow_style=False),
                                   _EMBEDDING_END,
                                   suffix)


def _textToYAML(text=''):

    flags = re.MULTILINE | re.DOTALL
    prefix = re.sub('^\\[{}-{}\\]\\s*$.*'.format(_COMMON_EMBEDDING_TITLE, _START), '', text, flags=flags)
    suffix = re.sub('.*^\\[{}-{}\\]\\s*\\n'.format(_COMMON_EMBEDDING_TITLE, _END), '', text, flags=flags)

    meat = re.sub('.*^\\[{}-{}\]\\s*$\\n'.format(_COMMON_EMBEDDING_TITLE, _START), '', text, flags=flags)
    meat = re.sub('^\\[{}-{}\\]\\s*$.*'.format(_COMMON_EMBEDDING_TITLE, _END), '', meat, flags=flags)

    yamlObject = yaml.load(meat)

    return yamlObject, prefix, suffix


class _SimpleTestPlanTextEmbedding(object):

    def __init__(self, parentPlanURI=None):
        self.yamlObject = None
        self.prefix = None
        self.suffix = None

    def toText(self):
        return _yamlToText(self.yamlObject, self.prefix, self.suffix)

    @classmethod
    def instantiateFromParentURI(cls, uri):
        retval = _SimpleTestPlanTextEmbedding()
        retval.yamlObject = {
                             'header': {
                                        'subject': 'pylarion',
                                        'formatVersion': 0.0,
                                        'dataType': 'SimpleTestPlan'
                                        },
                             'data': {
                                      'parentPlan': {
                                                     'uri': uri
                                                     }
                                      }
                             }
        return retval

    @classmethod
    def instantiateFromText(cls, text):
        if not text:
            return None
        if _EMBEDDING_START not in text:
            return None
        if _EMBEDDING_END not in text:
            return None
        yamlObject, prefix, suffix = _textToYAML(text)
        if not yamlObject:
            return None
        retval = None
        try:
            assert('pylarion' == yamlObject['header']['subject'])
            assert(0.0 == yamlObject['header']['formatVersion'])
            assert('SimpleTestPlan' == yamlObject['header']['dataType'])
            assert(yamlObject['data']['parentPlan'].has_key('uri'))
            retval = _SimpleTestPlanTextEmbedding()
            retval.yamlObject = yamlObject
            retval.prefix = prefix
            retval.suffix = suffix
        except:
            pass
        return retval

    @classmethod
    def getParentPlanURI(cls, text):
        embedding = _SimpleTestPlanTextEmbedding.instantiateFromText(text)
        if not embedding:
            raise PylarionLibException('Not SimpleTestPlan embedding: {}'.format(text))
        return embedding.yamlObject['data']['parentPlan']['uri']

    @classmethod
    def setParentPlanURI(cls, text, uri):
        embedding = _SimpleTestPlanTextEmbedding.instantiateFromText(text)
        if not embedding:
            raise PylarionLibException('Not SimpleTestPlan embedding: {}'.format(text))
        embedding.yamlObject['data']['parentPlan']['uri'] = uri
        return embedding.toText()


class _SimpleTestRunTextEmbedding(object):

    def __init__(self):
        self.yamlObject = None
        self.prefix = None
        self.suffix = None

    def toText(self):
        return _yamlToText(self.yamlObject, self.prefix, self.suffix)

    @classmethod
    def instantiateFromPlanURI(cls, uri):
        retval = _SimpleTestPlanTextEmbedding()
        retval.yamlObject = {
                             'header': {
                                        'subject': 'pylarion',
                                        'formatVersion': 0.0,
                                        'dataType': 'SimpleTestRun'
                                        },
                             'data': {
                                      'plan': {
                                               'uri': uri
                                               }
                                      }
                             }
        return retval

    @classmethod
    def instantiateFromText(cls, text):
        if not text:
            return None
        if _EMBEDDING_START not in text:
            return None
        if _EMBEDDING_END not in text:
            return None
        yamlObject, prefix, suffix = _textToYAML(text)
        if not yamlObject:
            return None
        retval = None
        try:
            assert('pylarion' == yamlObject['header']['subject'])
            assert(0.0 == yamlObject['header']['formatVersion'])
            assert('SimpleTestRun' == yamlObject['header']['dataType'])
            assert(yamlObject['data']['plan'].has_key('uri'))
            retval = _SimpleTestRunTextEmbedding()
            retval.yamlObject = yamlObject
            retval.prefix = prefix
            retval.suffix = suffix
        except:
            pass
        return retval

    @classmethod
    def getPlanURI(cls, text):
        embedding = _SimpleTestRunTextEmbedding.instantiateFromText(text)
        if not embedding:
            raise PylarionLibException('Not SimpleTestRun embedding: {}'.format(text))
        return embedding.yamlObject['data']['plan']['uri']

    @classmethod
    def setPlanURI(cls, text, uri):
        embedding = _SimpleTestRunTextEmbedding.instantiateFromText(text)
        if not embedding:
            raise PylarionLibException('Not SimpleTestRun embedding: {}'.format(text))
        embedding.yamlObject['data']['plan']['uri'] = uri
        return embedding.toText()


from pylarionlib.exceptions import PylarionLibException
