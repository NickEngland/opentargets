import ujson
import argparse
import multiprocessing
from threading import Thread
from queue import Queue
import itertools
from statistics import median
from collections import defaultdict, namedtuple
from typing import List, Dict

# Json is missing a wrapping list making it unable to parse the whole file at once
default_diseases_path = 'download/diseases.json'
default_targets_path = 'download/targets.json'
default_eva_path = 'download/eva.json'

TargetDisease = namedtuple("TargetDisease", "target disease")


def extract_value_from_json(path: str, column: str):
    data = {}
    for line in open(path, 'r', encoding='utf8'):
        item = ujson.loads(line)
        data[item['id']] = item[column]
    return data


def process_evidence(path=default_eva_path) -> Dict[TargetDisease, List]:
    target_disease_dict = defaultdict(list)
    for line in open(path, 'r', encoding='utf8'):
        item = ujson.loads(line)
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


def find_target_target_relationships(target_disease_set, disease_target_set, target) -> int:
    """
    This calculates the number of other targets which *target* shares at least 2 diseases with
    :param target_disease_set:
    :param disease_target_set:
    :param target:
    :return: The number of other targets which share at least 2 diseases with *target*
    """
    targets = defaultdict(int)
    diseases = target_disease_set.get(target)
    for disease in diseases:
        for target2 in disease_target_set.get(disease):
            targets[target2] += 1
    # remove self
    del targets[target]
    return len([target for target in targets if targets[target] >= 2])


class EvidenceParser:
    def __init__(self, eva_path=default_eva_path, targets_path=default_targets_path,
                 diseases_path=default_diseases_path):
        self.targets = extract_value_from_json(targets_path, "approvedSymbol")  # approvedSymbol
        self.diseases = extract_value_from_json(diseases_path, "name")  # name
        self.eva = process_evidence(eva_path)
        self.target_disease_set = defaultdict(set)
        self.disease_target_set = defaultdict(set)
        self.create_target_disease_sets()

    def parallel_calculate(self) -> List[Dict]:
        with multiprocessing.Pool() as pool:
            results = pool.starmap(calculate_data, self.eva.items())
            return results

    def parallel_target_target_calc(self) -> int:
        targets = zip(itertools.repeat(self.target_disease_set),
                      itertools.repeat(self.disease_target_set),
                      self.target_disease_set.keys())
        with multiprocessing.Pool() as pool:
            results = pool.starmap(find_target_target_relationships, targets)
            return sum(results)//2

    def join_columns(self, results: List[Dict]):
        for item in results:
            item['name'] = self.diseases[item['diseaseId']]
            item['approvedSymbol'] = self.targets[item['targetId']]
        return results

    def create_target_disease_sets(self):
        for key in self.eva.keys():
            self.target_disease_set[key.target].add(key.disease)
            self.disease_target_set[key.disease].add(key.target)


def main():
    parser = argparse.ArgumentParser(description='Process JSON data')
    parser.add_argument("--evidence", default=default_eva_path)
    parser.add_argument("--output", default="output.json")
    args = parser.parse_args()
    print("Loading JSON for analysis from", args.evidence)
    evidence_parser = EvidenceParser(args.evidence)
    print("Running calculations")
    results = evidence_parser.parallel_calculate()
    print("Joining columns")
    evidence_parser.join_columns(results)
    results.sort(key=lambda item: item['median'])
    print("Writing output to", args.output)
    with open(args.output, 'w', encoding='utf8') as output:
        ujson.dump(results, output)
    print("Calculating target-disease-target pairs")
    results = evidence_parser.parallel_target_target_calc()
    print(results, "Target-target pairs which share at least 2 diseases")


if __name__ == '__main__':
    main()
