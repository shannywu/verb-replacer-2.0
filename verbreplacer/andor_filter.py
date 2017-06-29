import linggle_api

SE = linggle_api.Linggle()


''' filter and count and/or ngram '''
def res_filter(res, conj):
    filtered_res = list(filter(lambda x: x[0][1] == conj, res))
    cnt = sum([item[1] for item in filtered_res])
    return filtered_res, cnt


''' get and/or relation between verbs from Linggle '''
def get_and_or_from_linggle(word_a, word_b):
    # if '_' in word_a or '_' in word_b:
    query1 = (word_a.replace('_', '+') + ' and/or ' + word_b.replace('_', '+')).split()
    # print('query1: ', query1)
    res = SE[' '.join(query1)]
    query2 = (word_b.replace('_', '+') + ' and/or ' + word_a.replace('_', '+')).split()
    # print('query2: ', query2)
    res.extend(SE[' '.join(query2)])
    # else:
        # query = (word_a + '/' + word_b + ' and/or ' + word_a + '/' + word_b).split()
        # print('query: ', query)
        # res = SE[' '.join(query)]
    
    res = list(filter(lambda x: x[0][0] != x[0][-1], res))  # filter out ngrams like 'receive and receive'
    return res


'''
conditions:
1) both "and" and "or" in result ngrams
2) # of "and" > # of "or"
'''
def check_and_or_relation(res):
    co_exist = False
    alike = False
    conj = [item[0][1] for item in res]
    # print(conj)
    if 'and' and 'or' in conj:
        co_exist = True
    _and, _and_cnt = res_filter(res, 'and')
    _or, _or_cnt = res_filter(res, 'or')
    if _and_cnt > _or_cnt:
        alike = True
    if co_exist and alike:
        return True
    else:
        return False


def filterer(coll_list, wrong):
    coll_res = []
    for verb, cnt in coll_list:
        res = get_and_or_from_linggle(wrong, verb)
        if check_and_or_relation(res):
            # print(verb)
            coll_res.append((verb, cnt))
    return coll_res


def cand_filterer(cand_list, wrong):
    cand_res = []
    for cand_verb, score, coll_rank, ch_rank, coll_cnt, ch_cnt in cand_list:
        res = get_and_or_from_linggle(wrong, cand_verb)
        if check_and_or_relation(res):
            # print(verb)
            cand_res.append((cand_verb, score, coll_rank, ch_rank, coll_cnt, ch_cnt))
    return cand_res
