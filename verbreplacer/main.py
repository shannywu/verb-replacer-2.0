import parser
import re
import language_model
import db_finder_old
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from srilm_wrapper import NgramScorer
 
wordnet_lemmatizer = WordNetLemmatizer()

wiki_channel_count = defaultdict(lambda: defaultdict(tuple))
be_verbs = {'be', 'is', 'am', 'are', 'was', 'were', '\'s', '\'d', 'been', 'should', 'could', 'would', 'shall', 'can', 'will'}


def tokenize(sent):
    return re.findall('[A-Za-z\']+', sent)


def parse_sent(sent):
    return parser.parse(sent)


def lemmatize_verb(verb):
    return wordnet_lemmatizer.lemmatize(verb, pos='v')


def lemmatize_obj(obj):
    return wordnet_lemmatizer.lemmatize(obj, pos='n')


def get_channel(verb):
    channel_list = sorted(db_finder_old.search_channel(verb), key=lambda x: x[2], reverse=True)
    return channel_list


def get_coll(obj, wrong):
    coll_list = sorted(db_finder_old.search_coll(obj), key=lambda x: x[1], reverse=True)
    return coll_list


def get_union(_list, verb_in_both, weight):
    union_verb = []
    for i, verb_cnt in enumerate(_list):
        if verb_cnt[0] not in verb_in_both:
            union_verb.append((verb_cnt[0], weight/(i+1)))
    return union_verb


def build_candidate_list(channel_list, coll_list, wrong):
    candidate_list = []
    for i, coll_cnt in enumerate(coll_list):
        for j, ch_cnt in enumerate(channel_list):
            if coll_cnt[0] == ch_cnt[0]:
                candidate_list.append((coll_cnt[0], 1/(i+1) + 1/(j+1)))
                break
    verb_in_both = list(map(lambda x: x[0], candidate_list))
    verb_in_channel = get_union(channel_list[:20], verb_in_both, 1)
    verb_in_coll = get_union(coll_list[:60], verb_in_both, 1)

    candidate_list = candidate_list + verb_in_channel + verb_in_coll
    candidate_list = sorted(candidate_list, key=lambda x: x[1], reverse=True)
    
    return candidate_list


def rerank(lm_score, candidate_list):
    lm_score = dict(lm_score)
    reranked_list = []
    for cand_verb, score in candidate_list:
        reranked_list.append((cand_verb, score - float(1/lm_score[cand_verb])))
    reranked_list = sorted(reranked_list, key=lambda x: x[1], reverse=True)
    return reranked_list


def get_verb_rank(_list, verb):
    for i, item in enumerate(_list):
        if item[0] == verb:
            return i+1


def rv_main(line):
    print(line)
    sent = line.strip()
    verb_obj_subj = parse_sent(sent)
    tokens = tokenize(sent)
    ranks = []
    for verb, obj, subj in verb_obj_subj:
        print('>>>>', verb, obj, subj)
        verb_ind = tokens.index(verb)
        print(verb_ind)
        obj_ind = -1
        subj_ind = -1
        verb = lemmatize_verb(verb.lower())
        channel_list = get_channel(verb)

        if obj:
            print(obj, tokens)
            obj_ind = tokens.index(obj)
            obj = lemmatize_obj(obj)
            coll_list = get_coll(obj, verb.lower())
        else:
            coll_list = []

        if subj:
            subj_ind = tokens.index(subj)

        print('channel_list: ', channel_list)
        print('coll_list: ', len(coll_list))
        candidate_list = build_candidate_list(channel_list, coll_list, verb)

        verb_in_cand = list(map(lambda x: x[0], candidate_list))
        
        lm_score = language_model.get_lm_score(candidate_list, tokens, verb, verb_in_cand, verb_ind, obj_ind, subj_ind)
        print('>>lm_score: ', len(lm_score), lm_score[:5])
        wrong_verb_rank = get_verb_rank(lm_score, verb)
        print(wrong_verb_rank)
        if wrong_verb_rank > 5 or not wrong_verb_rank:
            reranked_list = rerank(lm_score, candidate_list)
            sug_list = []
            for i, (c_verb, score) in enumerate(reranked_list[:3]):
                ch_rank = get_verb_rank(channel_list, c_verb)
                if ch_rank:
                    orig = channel_list[ch_rank-1][1]
                    avg = channel_list[ch_rank-1][2]
                else:
                    orig = 'not in channel'
                    avg = 'not in channel'
                sug_list.append((i+1, c_verb, orig, round(avg, 2)))
            results = {'wrong_verb': verb, 'object': obj, 'sug_list': sug_list}
            print(results)
            return results
        else:
            return {}


# load_wiki_reg_cnt()
# rv_main('I would like to eat dinner with you.')