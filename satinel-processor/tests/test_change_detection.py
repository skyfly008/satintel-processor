from satintel.change_detection import compute_change_stats


def test_change_stats():
    res = compute_change_stats(None, None)
    assert isinstance(res, dict)
    assert "activity_score" in res
