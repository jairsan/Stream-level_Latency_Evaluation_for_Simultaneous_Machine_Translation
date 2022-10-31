from typing import List, Tuple


def compute_measures(src_sentences: List[List[str]], tgt_sentences: List[List[str]], actions: List[str],
                     read_action_repr: str, write_action_repr: str,
                     penalty_scale_factor=1.0) -> Tuple[float, float, float]:
    # Compute delays
    delays: List[int] = []
    words_read = 0
    for action in actions:
        if action == read_action_repr:
            words_read += 1
        elif action == write_action_repr:
            delays.append(words_read)
        else:
            raise Exception

    src_lens: List[int] = []
    tgt_lens: List[int] = []
    gammas: List[float] = []
    sentence_delays: List[List[float]] = []

    for s, t in zip(src_sentences, tgt_sentences):
        src_lens.append(len(s))
        tgt_lens.append(len(t))
        gammas.append(len(t) / len(s))

        this_sentence_delays = delays[:len(t)]
        delays = delays[len(t):]

        assert len(this_sentence_delays) == len(t)

        sentence_delays.append(this_sentence_delays)

    assert len(delays) == 0

#Compute AP
    AP = 0
    for i in range(len(tgt_sentences)):
        partial_score = 0
        for t in range(len(sentence_delays[i])):
            partial_score += sentence_delays[i][t] - sum(src_lens[:i])
        if tgt_lens[i] > 0:
            partial_score = partial_score / (src_lens[i] * tgt_lens[i])
        AP += partial_score

    AP = AP / len(tgt_sentences)

    #Compute AL
    AL=0
    for i in range(len(tgt_sentences)):
        partial_score=0
        tau = 0
        for t in range(1,tgt_lens[i]+1):
            tau +=1
            if sentence_delays[i][t-1] >= sum(src_lens[:i+1]):
                break

        for t in range(1,tau+1):
            partial_score += sentence_delays[i][t-1] - ( sum(src_lens[:i]) + (t - 1)/gammas[i] )
        if tau > 0 :
            partial_score = partial_score / tau

        AL += partial_score

    AL = AL / len(tgt_sentences)

    #Compute DAL
    last_gt_prime = -99999
    DAL = 0
    for i in range(len(tgt_sentences)):
        partial_score = 0
        partial_scores = []
        for t in range(1, tgt_lens[i] +1):
            if i > 0 and t == 1:
                if gammas[i-1] > 0 :
                    gt_prime = max( sentence_delays[i][t-1], last_gt_prime + penalty_scale_factor * (1/ gammas[i-1])  )
                else:
                    gt_prime = last_gt_prime
            else:
                if gammas[i] > 0:
                    gt_prime = max( sentence_delays[i][t-1], last_gt_prime + penalty_scale_factor * (1/ gammas[i])  )
                else:
                    gt_prime = last_gt_prime
            last_gt_prime = gt_prime
            partial_score += gt_prime -  ( sum(src_lens[:i]) + (t - 1)/gammas[i])

        if tgt_lens[i] > 0:
            partial_score = partial_score / tgt_lens[i]

        DAL += partial_score
    DAL = DAL / len(tgt_sentences)

    return AP, AL, DAL
