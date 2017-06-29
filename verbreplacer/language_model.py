from srilm_wrapper import NgramScorer

ngram_scorer = NgramScorer()


def get_chunks_score(tokens, verb_ind, _ind):
    # print(tokens, verb_ind, _ind)
    if verb_ind > _ind and _ind > 0:
        score = ngram_scorer.score(' '.join(tokens[_ind:verb_ind+1]))['logprob']
    elif verb_ind < _ind and _ind > 0:
        score = ngram_scorer.score(' '.join(tokens[verb_ind:_ind+1]))['logprob']
    else:
        score = 0.0
    return score


def get_trigram_score(tokens, verb_ind):
    score = 0.0
    for i in range(3):
        if verb_ind-i > -1:
            score += ngram_scorer.score(' '.join(tokens[int(verb_ind-i):int(verb_ind-i+3)]))['logprob']
    return score


def language_model_score(tokens, verb_ind, cand_verb, obj_ind, subj_ind):
    # print(len(tokens), verb_ind, tokens, cand_verb)
    tokens[verb_ind] = cand_verb
    # print(obj_ind, subj_ind)
    score = get_chunks_score(tokens, verb_ind, obj_ind) + get_chunks_score(tokens, verb_ind, subj_ind)
    if score == 0.0:
        score = get_trigram_score(tokens, verb_ind)
    return score


def get_lm_score(candidate_list, tokens, verb, verb_in_cand, verb_ind, obj_ind, subj_ind):
    lm_score = []
    for cand_verb, score in candidate_list:
        lm_score.append((cand_verb, language_model_score(tokens, int(verb_ind), cand_verb, obj_ind, subj_ind)))
    if verb not in verb_in_cand:
        lm_score.append((verb, language_model_score(tokens, int(verb_ind), verb, obj_ind, subj_ind)))
    lm_score = sorted(lm_score, key=lambda x: x[1], reverse=True)
    return lm_score