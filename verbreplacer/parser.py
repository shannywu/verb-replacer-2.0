'''
name: parser.py
goal: extract verbs and verb-obj pairs
input: a sentence
output: verb-obj pairs (list of tuples)
example_input: 'Bring a blanket or lawn chair and appreciate the summer wind .'
example_output: [('Bring', 'chair', 'vn'), ('appreciate', 'wind', 'vn')]
'''

from nltk.parse.stanford import StanfordDependencyParser
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
dep_parser = StanfordDependencyParser(PROJECT_ROOT + '/stanford-parser-full-2015-04-20/stanford-parser.jar', PROJECT_ROOT + '/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar')
be_verbs = {'be', 'is', 'am', 'are', 'was', 'were', '\'s', '\'d', 'been', 'should', 'could', 'would', 'shall', 'can', 'will'}


# def check_obj_dependency(item):
#     # print(item)
#     # ((u'suggest', u'VB'), u'dobj', (u'requests', u'NNS'))
#     if item[1] in {'dobj', 'nmod', 'nsubjpass'}:
#         # print(item)
#         if item[0][1][0] == 'V' and item[2][1][0] == 'N':
#                 # and item[2][1] != 'NNP':  # and item[0][0] == wrong
#             return True
#         elif item[2][1][0] == 'V' and item[0][1][0] == 'N':
#                 # and item[0][1] != 'NNP':  # and item[2][0] == wrong
#             return True
#         else:
#             return False
#     else:
#         return False


# def check_subj_dependency(item):
#     # print(item)
#     # ((u'suggest', u'VB'), u'dobj', (u'requests', u'NNS'))
#     if item[1] == 'nsubj':
#         # print(item)
#         if item[0][1][0] == 'V' and item[2][1][0] == 'N':
#                 # and item[2][1] != 'NNP':  # and item[0][0] == wrong
#             return True
#         else:
#             return False
#     else:
#         return False


def find_verb(relations, verb_obj):
    verbs = set()
    for word_1, rel, word_2 in relations:
        if rel not in ['dobj', 'nmod', 'nsubjpass']:
            if word_1[1][0] == 'V' and (word_1[0] not in verb_obj) and (word_1[0] not in be_verbs):
                verbs.add((word_1[0], None))
            elif word_2[1][0] == 'V' and (word_2[0] not in verb_obj) and (word_2[0] not in be_verbs):
                verbs.add((word_2[0], None))
    return verbs


def check_rel(relations):
    verb_obj = set()
    verb_subj = set()
    for item in relations:
        # print(item)
        if item[1] in {'dobj', 'nmod', 'nsubjpass'}:
            # print(item)
            if item[0][1][0] == 'V' and item[2][1][0] == 'N':
                    # and item[2][1] != 'NNP':  # and item[0][0] == wrong
                verb_obj.add((item[0][0], item[2][0]))
                # return True
            elif item[2][1][0] == 'V' and item[0][1][0] == 'N':
                    # and item[0][1] != 'NNP':  # and item[2][0] == wrong
                verb_obj.add((item[2][0], item[0][0]))
            # else:
            #     return False
        elif item[1] == 'nsubj':
            if item[0][1][0] == 'V' and item[2][1][0] == 'N':
                verb_subj.add((item[0][0], item[2][0]))
        elif item[1] == 'xcomp':
            if item[0][1][0] == 'V' and item[2][1][0] == 'J':
                verb_obj.add((item[0][0], item[2][0]))
    return list(verb_obj), list(verb_subj)


def combine_obj_subj(verb_obj, verb_subj):
    # print(verb_obj, verb_subj)
    combined = []
    if verb_subj:
        verb_subj = dict(verb_subj)
        for verb1, obj in verb_obj:
            # for verb2, subj in verb_subj:
            #     if verb1 == verb2:
                    # print(verb1, obj, subj)
            try:
                combined.append((verb1, obj, verb_subj[verb1]))
            except:
                #     print(verb1, obj, None)
                combined.append((verb1, obj, None))
    else:
        combined = [(verb, obj, None) for verb, obj in verb_obj]
    # print(combined)
    return combined


def parse(sent):
    for parsed_sent in dep_parser.raw_parse(sent):
        relations = list(parsed_sent.triples())
        # print(relations)
    verb_obj, verb_subj = check_rel(relations)
    _verbs = [verb for verb, obj in verb_obj]
    verbs = find_verb(relations, set(_verbs))
    verb_obj.extend(verbs)

    combined = combine_obj_subj(verb_obj, verb_subj)
    return combined


# from nltk.stem import WordNetLemmatizer
 
# wordnet_lemmatizer = WordNetLemmatizer()

# # with open('rv.clc.develop.txt') as f:
# verb_obj_pair = set()
# with open('rv.clc.develop.txt') as f:
#     for line in f.readlines():
#         verb_obj_subj = parse(line.strip())
#         for verb, obj, subj in verb_obj_subj:
#             if obj:
#                 verb_obj_pair.add((wordnet_lemmatizer.lemmatize(verb, pos='v'), obj))

# fout = open('rv.clc.develop.verb.obj.pair.txt', 'w')
# for verb, obj in verb_obj_pair:
#     fout.write('{}\t{}\n'.format(verb, obj))
# fout.close()
# print(parse('I am sorry to make you happy .'))
# print('--------------')
# print(parse('Having a sport after class is also fun .'))
# print('--------------')
# print(parse('All Japanese children accept a solid education .'))