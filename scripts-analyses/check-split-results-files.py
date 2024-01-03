#!/usr/bin/python
import json
import argparse

"""
This script checks that a results file that has been concatenated from several parts
has (i) the correct number of examples, (ii) no duplicated docids, (iii) the same
correct indices for the fewshot examples (in the case of 1-shot). It does this by 
comparing the results file (model1_results) to a second results file that was created
in a single run (model2_results). This assumes that the same dataset and prompt was used to
produce the two files and that the same random seed was used. Typically, this can be useful
to compare the output of the larger BLOOM models (which may need to be run in several parts 
and concatenated with the results of a smaller BLOOM model (which can be run in one go).

Usage: check-split-results-files.py model1_results_file model2_results_file
"""


parser = argparse.ArgumentParser()
parser.add_argument('model1_results')
parser.add_argument('model2_results')
args = parser.parse_args()


def read_results_file(filename):
    results = {}
    with open(filename) as fp:
        for line in fp:
            dict_results = json.loads(line)
            assert dict_results['doc_id'] not in results, 'Document ids should not appear several times in the same results file'
            results[dict_results['doc_id']] = dict_results
    return results

model1_results = read_results_file(args.model1_results)
model2_results = read_results_file(args.model2_results)

assert len(model1_results) == len(model2_results), 'The two results files should have not the same number of unique examples'

# check the fewshot examples used
for docid in model1_results:
    if model1_results[docid]['fewshot_num'] == model2_results[docid]['fewshot_num']:
        assert model1_results[docid]['fewshot_idx'] == model2_results[docid]['fewshot_idx'], 'Fewshot examples differ: \n' + args.model1_results + '\n' + args.model2_results

print('All checks run!')

