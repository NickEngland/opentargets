from process_json import json_to_dict, diseases_path, process_evidence, TargetDisease, EvidenceParser, calculate_data


# We only want the disease name and the id fields from this file
def test_load_diseases():
    data = json_to_dict('test/diseases.json')
    assert len(data) == 1
    print(data)
    assert data['Orphanet_300576']['name'] == 'Oligodontia - cancer predisposition syndrome'


def test_process_evidence():
    evidence_list = process_evidence(path='test/eva.json')
    print(evidence_list)
    assert len(evidence_list) == 1
    assert evidence_list[TargetDisease("ENSG00000168646", "Orphanet_300576")] == [0.02]


def test_calculate_data():
    data = calculate_data(TargetDisease("target", "disease"), [0.4, 0.5, 0.6, 0.4, 0.6])
    assert data['median'] == 0.5
    assert data['highest_scores'] == [0.6, 0.6, 0.5]


def test_parallel_calculate():
    parser = EvidenceParser(eva_path='test/eva.json', diseases_path='test/diseases.json',
                            targets_path='test/targets.json')
    results = parser.parallel_calculate()
    print(results)
    assert len(results) == 1
    assert results[0]['median'] == 0.02


def test_join_columns():
    parser = EvidenceParser(eva_path='test/eva.json', diseases_path='test/diseases.json',
                            targets_path='test/targets.json')
    results = parser.parallel_calculate()
    assert len(results) == 1
    results = parser.join_columns(results)
    assert results[0]['name'] == 'Oligodontia - cancer predisposition syndrome'
    print(results)
