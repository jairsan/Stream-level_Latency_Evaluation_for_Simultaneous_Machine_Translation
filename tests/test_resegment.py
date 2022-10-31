from streaming_latency_tk.resegment import resegment


def test_resegment():
    hyp = [["a", "b", "c"], ["d"]]
    ref = [["a", "b"], ["c", "d"]]

    assert resegment(hypothesis=hyp, reference=ref) == [["a", "b"], ["c", "d"]]
