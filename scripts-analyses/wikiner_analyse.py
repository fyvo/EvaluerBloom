#!/usr/bin/python
from wikiner_results import read_results
import re

"""
This script enables analysis of the wikiner results. Based on the example files in the
given task folder, it calculates values for the analysis based on the following categories:
incorrectly empty, correctly_empty, partial, hallucinated, long, in_fewshot, several, only_1,
total_examples.

Usage: python wikiner_analyse.py <task_folder>

E.g. python wikiner_analyse.py wikiner_fr
"""

model_list = ['bloom_560m', 'bloom_1b1', 'bloom_3b',  'bloom_7b1', 'bloom', 'bloomz']
template_list = ['list_PER', 'list_LOC', 'list_ORG', 'choose_entity']

def view_examples(results):
    lens = {}
    for numshot in 'zero-shot', 'zero-shot':
        for model in ["bloom"]: #results[numshot]:
            for template in results[numshot][model]:
                print(template)
                print(results[numshot][model][template])
                for example in results[numshot][model][template]['examples']:
                    print(example['ctx'])
                    print('target = ', example['target'])
                    print('pred = ', example['pred'])
                    pred = example['pred']
                    if len(pred.split()) not in lens:
                        lens[len(pred.split())] = 0
                    lens[len(pred.split())] += 1
            print(sorted(lens.items(), key=lambda x: x[1])[:10])


def clean_element(element):
    element = re.sub("[\"'«»“”    ]+$", "", re.sub("^[\"'«»“”    ]+", "", element))
    element = element.strip()
    return element


def clean_up_list_elements(list_to_clean):
    return [x for x in set([clean_element(x) for x in list_to_clean]) if x != '']
                    
def make_list(text_list):
    if '\n' in text_list:
        tabline = text_list.split('\n')
    elif ';' in text_list:
        tabline = text_list.split(';')
    else:
        tabline = text_list.split(',')
    return tabline
                    
def error_analysis(results):
    errors = {}
    for numshot in 'one-shot', 'zero-shot':
        errors[numshot] = {}
        for template in template_list:
            print()
            errors[numshot][template] = {}
            for model in model_list:
                

                errors[numshot][template][model] = {'incorrectly_empty': 0, 'correctly_empty': 0, 'partial': 0, 'hallucinated': 0, 'long': 0,
                                                     'in_fewshot': 0, 'several': 0, 'only_1': 0, 'total_examples': 0}
                
                if 'list' not in template:
                    continue
                
                if 'examples' not in results[numshot][model][template]:
                    continue
                for example in results[numshot][model][template]['examples']:
                    errors[numshot][template][model]['total_examples'] += 1
                    pred = example['pred']
                    target = example['target']
                    context = example['ctx']

                    if type(target) == list:
                        if len(target) != 1:
                            print(target)
                        assert len(target) == 1, 'The analysis assumes that there is only one target'
                        target = target[0]

                    pred_list = clean_up_list_elements(make_list(pred))
                    target_list = clean_up_list_elements(make_list(target))
                        
                    # several items assumed to be in the prediction according to the fuzzy list matching
                    if '\n' in pred.strip() or ',' in pred or ';' in pred:
                        errors[numshot][template][model]['several'] += 1

                    # prediction more than 10 tokens
                    if len(pred.split()) > 10:
                        errors[numshot][template][model]['long'] += 1

                    # partial match of prediction
                    for ind_pred in pred_list:
                        if ind_pred in clean_element(target) and ind_pred not in target_list:
                            errors[numshot][template][model]['partial'] += 1
                            #print(example['ctx'])
                            #print('target = ', example['target'])
                            #print('pred = ', [example['pred']])
                            #print('ind pred = ', ind_pred)
                            #print('target list = ', target_list)
                            #input()
                    # empty prediction when shouldn't be empty
                    if pred.strip() == '' and target.strip() != '':
                        errors[numshot][template][model]['incorrectly_empty'] += 1
                    # empty prediction when should be empty
                    if pred.strip() == '' and target.strip() == '':
                        errors[numshot][template][model]['correctly_empty'] += 1
                    # only one prediction when should be multiple
                    if len(target_list) > 1 and len(pred_list) < 2:
                        errors[numshot][template][model]['only_1'] += 1
                    # prediction in few-shot example and not in context
                    if pred in re.sub('###.+?$', '', context) and pred not in re.sub('^.+?###', '', context):
                        errors[numshot][template][model]['in_fewshot'] += 1
                    # prediction not in any part of the context
                    if pred not in context:
                        errors[numshot][template][model]['hallucinated'] += 1
                print(model, numshot, template, errors[numshot][template][model])


def analyse_cats_choose(results):
    errors = {}
    for numshot in 'one-shot', 'zero-shot':
        errors[numshot] = {}
        for template in ['choose_entity']:
            errors[numshot][template] = {}
            print()
            for model in model_list:
                errors[numshot][template][model] = {}
                #import pdb; pdb.set_trace()
                if 'examples' not in results[numshot][model][template]:
                    print('skipping', model, numshot, template)
                    continue
                correct, total = 0, 0
                for example in results[numshot][model][template]['examples']:

                    pred = example['pred']
                    target = example['target']
                    context = example['ctx']

                    if target not in errors[numshot][template][model]:
                        errors[numshot][template][model][target] = {}
                    if pred not in errors[numshot][template][model][target]:
                        errors[numshot][template][model][target][pred] = 0
                    errors[numshot][template][model][target][pred] += 1

                    if target == pred:
                        correct +=1
                    total +=1
                    
                print(model, numshot, template, errors[numshot][template][model])
                print(correct, total, correct/total)

                    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('task_folder')
    args = parser.parse_args()

    results = read_results(args.task_folder)
    #view_examples(results)
    error_analysis(results)
    #analyse_cats_choose(results)
