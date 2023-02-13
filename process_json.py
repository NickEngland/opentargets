import json
import argparse
import multiprocessing
from statistics import median
from collections import defaultdict, namedtuple
from typing import List, Dict

# Json is missing a wrapping list making it unable to parse the whole file at once
diseases_path = 'download/diseases.json'
targets_path = 'download/targets.json'
eva_path = 'download/eva.json'

TargetDisease = namedtuple("TargetDisease", "target disease")


def json_to_dict(path: str):
    data = {}
    for line in open(path, 'r'):
        item = json.loads(line)
        data[item['id']] = item
    return data


def process_evidence(path=eva_path) -> dict:
    target_disease_dict = defaultdict(list)
    for line in open(path, 'r'):
        item = json.loads(line)
        target_disease = TargetDisease(item['targetId'], item['diseaseId'])
        score = item['score']
        target_disease_dict[target_disease].append(score)
    return target_disease_dict


def calculate_data(target_data, scores) -> dict:
    scores.sort()
    result = {'diseaseId': target_data.disease,
              'targetId': target_data.target,
              'median': median(scores),
              'highest_scores': scores[-3:][::-1]}
    return result


class EvidenceParser:
    def __init__(self, eva_path=eva_path, targets_path=targets_path, diseases_path=diseases_path):
        self.targets = json_to_dict(targets_path)  # approvedSymbol
        self.diseases = json_to_dict(diseases_path)  # name
        self.eva = process_evidence(eva_path)

    def parallel_calculate(self) -> List[Dict]:
        with multiprocessing.Pool() as pool:
            results = pool.starmap(calculate_data, self.eva.items())
            return results

    def join_columns(self, results: List[Dict]):
        for item in results:
            item['name'] = self.diseases[item['diseaseId']]['name']
            item['approvedSymbol'] = self.targets[item['targetId']]['approvedSymbol']
        return results


def main():
    parser = argparse.ArgumentParser(description='Process JSON data')
    parser.add_argument("--evidence", default=eva_path)
    parser.add_argument("--output", default="output.json")
    args = parser.parse_args()
    evidence_parser = EvidenceParser(args.evidence)
    results = evidence_parser.parallel_calculate()
    evidence_parser.join_columns(results)
    results.sort(key=lambda item: item['median'])
    with open(args.output, 'w') as output:
        json.dump(results, output)


if __name__ == '__main__':
    main()
