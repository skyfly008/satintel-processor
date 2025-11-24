from satintel.api_fetch import fetch_dynamic_imagery, batch_fetch


def test_fetch_single():
    p = fetch_dynamic_imagery('AREA_1','2023-01-01')
    assert isinstance(p, str)


def test_batch_fetch():
    tasks = [{'area_id':'AREA_1','date':'2023-01-01'},{'area_id':'AREA_1','date':'2021-01-01'}]
    res = batch_fetch(tasks)
    assert len(res) == 2
