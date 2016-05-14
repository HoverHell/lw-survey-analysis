#!/usr/bin/env python

import json
import libsurveyanalysis

survey_structure = libsurveyanalysis.SurveyStructure('lw_2016_survey_structure.txt')

column_infos = []


keys_flat = [
    dict(survey_structure[key], key=key, group=group)
    for group, keys in survey_structure.groups()
    for key in keys]

# # Example `key_info`s:
# {'answers': [], 'code': 'GeneralPrivacy', 'dtype': 'Y',
#   'group': 'Privacy', 'key': 'GeneralPrivacy',
#   'label': 'Can we include your survey data in a public dataset?',
#   'sub_questions': []}
# {'answers': [
#     {'code': '1', 'dtype': '0', 'label': 'Nuclear war'},
#     # ...
#     {'code': '8', 'dtype': '0', 'label': 'Economic / political collapse'}],
#   'code': 'XRiskType', 'dtype': 'L', 'group': 'Technological Unemployment (Futurology Part 2)',
#   'key': 'XRiskType',
#   'label': 'Which disaster do you think is ...',
#   'sub_questions': [
#       {'code': 'other', 'dtype': '0', 'label': 'Other', 'unknown': '1'}]}
# {'answers': [], 'code': 'EndOfWorkConcerns', 'dtype': 'M',
#   'group': 'Technological Unemployment (Futurology Part 2)', 'key': 'EndOfWorkConcerns',
#   'label': 'If machines end all or almost all employment, what are your biggest worries? Pick two.',
#   'sub_questions': [
#       {'code': '1', 'dtype': '0', 'label': 'People will just idle about in destructive ways', 'unknown': '1'},
#       # ...
#       {'code': '4', 'dtype': '0', 'label': "The machines won't need us, and we'll starve to death or be otherwise liquidated", 'unknown': '1'},
#       {'code': 'other', 'dtype': '0', 'label': 'Other', 'unknown': '1'}]}

# [11:54:28] <namespace> If it has subquestions, if other put in the
# other question label with presets since it's predictable, if not
# other then go through each subquestion like it's a main question and
# concatenate the main question key and the subquestion key with
# square brackets surrounding the subquestion key.
# [11:54:47] <namespace> If it doesn't have subquestions, you put in
# the data with just the main question data.

for key_info in keys_flat:
    base_info = dict(key_info)
    for key in ('sub_questions', 'answers'):
        base_info.pop(key, None)
    here_columns = []

    code = key_info['code']

    is_other_question = (
        len(key_info['sub_questions']) == 1 and
        key_info['sub_questions'][0]['code'] == 'other')
    is_subquestions_question = (
        key_info['sub_questions'] and not is_other_question)
    if not is_subquestions_question:
        here_columns.append(dict(base_info, sql_key=code, csv_key=code))

    for subquestion in key_info['sub_questions']:
        here_info = dict(
            base_info,
            csv_key='%s[%s]' % (key_info['code'], subquestion['code']),
            sql_key='%s_%s' % (key_info['code'], subquestion['code']))
        here_info.update(subquestion)
        here_columns.append(here_info)

    column_infos.extend(here_columns)


csv_column_infos = {info['csv_key']: info for info in column_infos}
# Unspecified columns: {'SingularityHealth', 'startlanguage'}
# Not-in-data columns: {'EmailAddress'}


if __name__ == '__main__':
    with open('column_infos.json', 'w') as fo:
        json.dump(
            column_infos, fo,
            indent=2, ensure_ascii=False, sort_keys=True)
