# TODO Erase this file after verifying that it is not needed for anything.
# It is part of original code and I am unsure of its purpose.

# #!/usr/bin/env python
# # -*- coding: utf8 -*-
# from __future__ import absolute_import, division, print_function, unicode_literals
# 
# import re
# 
# import yaml
# from pylarion.exceptions import PylarionLibException
# 
# # Implement internals of embedding SimpleTestPlan and SimpleTestRun
# # specific data into text and parsing them back. See interface.py.
# 
# 
# _COMMON_EMBEDDING_TITLE = 'pylarion.structured-field'
# _START = 'start'
# _END = 'end'
# _EMBEDDING_START = '[{0}-{1}]'.format(_COMMON_EMBEDDING_TITLE, _START)
# _EMBEDDING_END = '[{0}-{1}]'.format(_COMMON_EMBEDDING_TITLE, _END)
# 
# 
# def _yaml_to_text(yaml_object_to_embed, prefix, suffix):
# 
#     if not prefix:
#         prefix = ''
# 
#     if prefix:
#         if not prefix.endswith('\n'):
#             prefix = '{0}\n'.format(prefix)
# 
#     if not suffix:
#         suffix = ''
# 
#     return '{0}{1}\n{2}{3}\n{4}'.format(
#                                    prefix,
#                                    _EMBEDDING_START,
#                                    yaml.dump(yaml_object_to_embed, default_flow_style=False),
#                                    _EMBEDDING_END,
#                                    suffix)
# 
# 
# def _text_to_yaml(text=''):
# 
#     flags = re.MULTILINE | re.DOTALL
#     prefix = re.sub('^\\[{0}-{1}\\]\\s*$.*'.format(_COMMON_EMBEDDING_TITLE, _START), '', text, flags=flags)
#     suffix = re.sub('.*^\\[{0}-{1}\\]\\s*\\n'.format(_COMMON_EMBEDDING_TITLE, _END), '', text, flags=flags)
# 
#     meat = re.sub('.*^\\[{0}-{1}\]\\s*$\\n'.format(_COMMON_EMBEDDING_TITLE, _START), '', text, flags=flags)
#     meat = re.sub('^\\[{0}-{1}\\]\\s*$.*'.format(_COMMON_EMBEDDING_TITLE, _END), '', meat, flags=flags)
# 
#     yaml_object = yaml.load(meat)
# 
#     return yaml_object, prefix, suffix
# 
# 
# class _SimpleTestPlanTextEmbedding(object):
# 
#     def __init__(self, parentPlanURI=None):
#         self.yaml_object = None
#         self.prefix = None
#         self.suffix = None
# 
#     def to_text(self):
#         return _yaml_to_text(self.yaml_object, self.prefix, self.suffix)
# 
#     @classmethod
#     def instantiate_from_parent_uri(cls, uri):
#         retval = _SimpleTestPlanTextEmbedding()
#         retval.yaml_object = {
#                              'header': {
#                                         'subject': 'pylarion.',
#                                         'formatVersion': 0.0,
#                                         'dataType': 'SimpleTestPlan'
#                                         },
#                              'data': {
#                                       'parentPlan': {
#                                                      'uri': uri
#                                                      }
#                                       }
#                              }
#         return retval
# 
#     @classmethod
#     def instantiate_from_text(cls, text):
#         if not text:
#             return None
#         if _EMBEDDING_START not in text:
#             return None
#         if _EMBEDDING_END not in text:
#             return None
#         yaml_object, prefix, suffix = _text_to_yaml(text)
#         if not yaml_object:
#             return None
#         retval = None
#         try:
#             assert('pylarion. == yaml_object['header']['subject'])
#             assert(0.0 == yaml_object['header']['formatVersion'])
#             assert('SimpleTestPlan' == yaml_object['header']['dataType'])
#             assert(yaml_object['data']['parentPlan'].has_key('uri'))
#             retval = _SimpleTestPlanTextEmbedding()
#             retval.yaml_object = yaml_object
#             retval.prefix = prefix
#             retval.suffix = suffix
#         except:
#             pass
#         return retval
# 
#     @classmethod
#     def get_parent_plan_uri(cls, text):
#         embedding = _SimpleTestPlanTextEmbedding.instantiate_from_text(text)
#         if not embedding:
#             raise PylarionLibException('Not SimpleTestPlan embedding: {0}'.format(text))
#         return embedding.yaml_object['data']['parentPlan']['uri']
# 
#     @classmethod
#     def set_parent_plan_uri(cls, text, uri):
#         embedding = _SimpleTestPlanTextEmbedding.instantiate_from_text(text)
#         if not embedding:
#             raise PylarionLibException('Not SimpleTestPlan embedding: {0}'.format(text))
#         embedding.yaml_object['data']['parentPlan']['uri'] = uri
#         return embedding.to_text()
# 
#     @classmethod
#     def get_linked_work_items_pids(cls, text):
#         embedding = _SimpleTestPlanTextEmbedding.instantiate_from_text(text)
#         if not embedding:
#             raise PylarionLibException('Not SimpleTestPlan embedding: {0}'.format(text))
#         if not embedding.suffix:
#             embedding.suffix = ''
#         # TODO: check the format: just a repetition of (like)
#         # <div id="polarion_wiki macro name=module-workitem;params=id=BRTR-4985|external=true"></div>
#         # without newlines
#         retval = []
#         for matched in re.findall(r'<div id="polarion_wiki macro name=module-workitem;params=id=[A-Z0-9-]*\|external=true"></div>', embedding.suffix, re.DOTALL):
#             subs = re.sub(r'\|external=true"></div>$', '', matched)
#             subs = re.sub(r'.*=', '', subs)
#             if subs:
#                 retval.append(subs)
#         return retval
# 
#     @classmethod
#     def set_linked_work_items_pids(cls, text, wipids):
#         embedding = _SimpleTestPlanTextEmbedding.instantiate_from_text(text)
#         if not embedding:
#             raise PylarionLibException('Not SimpleTestPlan embedding: {0}'.format(text))
#         embedding.suffix = ''
#         for pid in wipids:
#             embedding.suffix = '{0}<div id="polarion_wiki macro name=module-workitem;params=id={1}|external=true"></div>'.format(embedding.suffix, pid)
#         return embedding.to_text()
# 
# 
# class _SimpleTestRunTextEmbedding(object):
# 
#     def __init__(self):
#         self.yaml_object = None
#         self.prefix = None
#         self.suffix = None
# 
#     def to_text(self):
#         return _yaml_to_text(self.yaml_object, self.prefix, self.suffix)
# 
#     @classmethod
#     def instantiate_from_plan_uri(cls, uri):
#         retval = _SimpleTestPlanTextEmbedding()
#         retval.yaml_object = {
#                              'header': {
#                                         'subject': 'pylarion.,
#                                         'formatVersion': 0.0,
#                                         'dataType': 'SimpleTestRun'
#                                         },
#                              'data': {
#                                       'plan': {
#                                                'uri': uri
#                                                }
#                                       }
#                              }
#         return retval
# 
#     @classmethod
#     def instantiate_from_text(cls, text):
#         if not text:
#             return None
#         if _EMBEDDING_START not in text:
#             return None
#         if _EMBEDDING_END not in text:
#             return None
#         yaml_object, prefix, suffix = _text_to_yaml(text)
#         if not yaml_object:
#             return None
#         retval = None
#         try:
#             assert('pylarion. == yaml_object['header']['subject'])
#             assert(0.0 == yaml_object['header']['formatVersion'])
#             assert('SimpleTestRun' == yaml_object['header']['dataType'])
#             assert(yaml_object['data']['plan'].has_key('uri'))
#             retval = _SimpleTestRunTextEmbedding()
#             retval.yaml_object = yaml_object
#             retval.prefix = prefix
#             retval.suffix = suffix
#         except:
#             pass
#         return retval
# 
#     @classmethod
#     def get_plan_uri(cls, text):
#         embedding = _SimpleTestRunTextEmbedding.instantiate_from_text(text)
#         if not embedding:
#             return None
#         return embedding.yaml_object['data']['plan']['uri']
# 
#     @classmethod
#     def set_plan_uri(cls, text, uri):
#         embedding = _SimpleTestRunTextEmbedding.instantiate_from_text(text)
#         if not embedding:
#             raise PylarionLibException('Not SimpleTestRun embedding: {0}'.format(text))
#         embedding.yaml_object['data']['plan']['uri'] = uri
#         return embedding.to_text()
# 
>>>>>>> d7f7b29... minor fixes

