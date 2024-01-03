#!/usr/bin/python
import json
import argparse

"""
This script checks that an examples file that has been concatenated from several parts
has (i) the correct number of examples, (ii) no duplicated docids, (iii) the same
correct indices for the fewshot examples (in the case of 1-shot). It does this by 
comparing the examples file (model1_results) to a second examples file that was created
in a single run (model2_results). This assumes that the same dataset, prompt and few-shot number
(either zero or one) was used to produce the two files and that the same random seed was used. 
Typically, this can be useful to compare the output of the larger BLOOM models (which may need 
to be run in several parts and concatenated with the results of a smaller BLOOM model (which can be run in one go).

Usage: python check-split-examples-files.py model1_results_file model2_examples_file

E.g. python check-split-examples-files.py wikiner_fr/one-shot/bloom/eval_bloom--model_name-bloom--task_name-wikiner_fr--template_name-list_PER--data_name-wikiner_fr--num_fewshot-1/outputs/examples.concat.model\=-gpfsdswork-dataset-HuggingFace_Models-bigscience-bloom.task\=wikiner_fr.templates\=list-PER.fewshot\=1.batchsize\=2.seed\=1234.json wikiner_fr/one-shot/bloom_1b1/eval_bloom--model_name-bloom_1b1--task_name-wikiner_fr--template_name-list_PER--data_name-wikiner_fr--num_fewshot-1/outputs/examples.model\=-gpfsdswork-dataset-HuggingFace_Models-bigscience-bloom-1b1.task\=wikiner_fr.templates\=list-PER.fewshot\=1.batchsize\=16.seed\=1234.timestamp\=2023-11-27T14\:39\:36.json
"""


parser = argparse.ArgumentParser()
parser.add_argument('model1_examples')
parser.add_argument('model2_examples')
args = parser.parse_args()


def read_examples_file(filename):
    examples = {}
    with open(filename) as fp:
        for line in fp:
            dict_examples = json.loads(line)
            assert dict_examples['doc_id'] not in examples, 'Document ids should not appear several times in the same examples file'
            examples[dict_examples['doc_id']] = dict_examples
    return examples

model1_examples = read_examples_file(args.model1_examples)
model2_examples = read_examples_file(args.model2_examples)

assert len(model1_examples) == len(model2_examples), 'The two examples files should have not the same number of unique examples'

# check the fewshot examples used
for docid in model1_examples:
    if model1_examples[docid]['fewshot_num'] == model2_examples[docid]['fewshot_num']:
        assert model1_examples[docid]['fewshot_idx'] == model2_examples[docid]['fewshot_idx'], 'Fewshot examples differ: \n' + args.model1_examples + '\n' + args.model2_examples

print('All checks run!')

