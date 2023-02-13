from process_json import json_to_dict, process_evidence, TargetDisease, EvidenceParser, calculate_data, \
    find_target_target_relationships


# We only want the disease name and the id fields from this file
def test_load_diseases():
    data = json_to_dict('test/diseases.json')
    assert len(data) == 2
    print(data)
    assert data['Orphanet_300576']['name'] == 'Oligodontia - cancer predisposition syndrome'


def test_process_evidence():
    evidence_list = process_evidence(path='test/eva.json')
    print(evidence_list)
    assert len(evidence_list) == 4
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
    assert len(results) == 4
    assert results[0]['median'] == 0.02


def test_join_columns():
    parser = EvidenceParser(eva_path='test/eva.json', diseases_path='test/diseases.json',
                            targets_path='test/targets.json')
    results = parser.parallel_calculate()
    assert len(results) == 4
    results = parser.join_columns(results)
    assert results[0]['name'] == 'Oligodontia - cancer predisposition syndrome'
    print(results)


def test_find_target_target_relationships():
    parser = EvidenceParser(eva_path='test/eva.json', diseases_path='test/diseases.json',
                            targets_path='test/targets.json')
    count = find_target_target_relationships(parser.target_disease_set, parser.disease_target_set, "TESTGENE")
    assert count == 1

def test_target_target_parallel_calc():
    parser = EvidenceParser(eva_path='test/eva.json', diseases_path='test/diseases.json',
                            targets_path='test/targets.json')
    results = parser.parallel_target_target_calc()
    print(results)
    assert results == 1
