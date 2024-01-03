#!/usr/bin/python
import os
import re
import glob
import json

"""
This script collates the results for the wikiner_fr task based on the output folder
containing examples and slim* files, and writes out latex tables with the results
based on fuzzy precision, recall and f-score.

Usage: python wikiner_results.py <task_folder>

E.g. python wikiner_results.py wikiner_fr
"""

def read_json(json_file):
    if '.jsonl' in json_file:
        contents = []
        with open(json_file) as fp:
            for line in fp:
                contents.append(json.loads(line))
    else:
        contents = json.load(open(json_file))
    return contents
 
def read_results(task_folder):
    results = {}
    for shotnum in 'zero-shot', 'one-shot':
        results[shotnum] = {}
        for model in os.listdir(task_folder + '/' + shotnum):
            if model[0] == '.' or "fewshot" in model:
                continue
            results[shotnum][model] = {}
            for run in os.listdir(task_folder + '/' + shotnum + '/' + model):
                if run[0] == '.':
                    continue
                template = re.match('.*?template_name-(.+?)--', run).group(1)
                run_folder = task_folder + '/' + shotnum + '/' + model + '/' + run + '/outputs'
                results[shotnum][model][template] = {}

                try:
                    slim_file = glob.glob(run_folder + '/slim*')[0] # decomment for analysis
                    example_files = [x for x in glob.glob(run_folder + '/examples*') if 'limited' not in x]
                    assert len(example_files) == 1, example_files
                    example_files.sort(key=os.path.getmtime)
                    example_file = example_files[0]

                except Exception:
                    continue

                results[shotnum][model][template]['slim'] = read_json(slim_file) # decomment for analysis
                results[shotnum][model][template]['examples'] = read_json(example_file)
    return results

def escape_list(orig_list):
    escaped_list = [x.replace('_', '\_') for x in orig_list]
    return escaped_list

def escape(word):
    escaped = word.replace('_', '\_')
    return escaped

def prepare_table(results):
    model_list = ['bloom_560m', 'bloom_1b1', 'bloom_3b',  'bloom_7b1', 'bloom', 'bloomz']
    template_list = ['list_PER', 'list_LOC', 'list_ORG']

    # list_ templates results table
    if False:
        print(r'Invite & Modèle & \# exemples & Précision & Rappel & F-mesure \\')
        print('\midrule')
        for template in template_list:
            print(r'\multirow{12}{*}{\promptex' + escape(template) + r'}} ')
            for model in model_list:
                print(r'& \multirow{2}{*}{' + escape(model) + '} ', end='')
                for num, shotnum in enumerate(['zero-shot', 'one-shot']):
                    print((' & ' * (num + 1)) + str(num), end= ' & ')
                    for s, score in enumerate('prf'):
                        if model not in results[shotnum] or template not in results[shotnum][model] or 'slim' not in results[shotnum][model][template]:
                            print('-', end=' & ')
                        else:
                            value = "{:.2f}".format(round(results[shotnum][model][template]['slim']['results'][s]['fuzzy_list_' + score], 2)).replace('.', ',')
                            if value == '0':
                                value = '0.00'
                            print(value, end=' & ')
                    print(r' \\')
            print('\midrule')
    else:
        print(r' & & \multicolumn{3}{c}{\zeroshot} && \multicolumn{3}{c}{\oneshot} \\')
        print(r'Invite & Modèle & P & R & F1 && P & R & F1\\')
        print('\midrule')
        for template in template_list:
            print(r'\multirow{6}{*}{' + escape(template) + r'} ')
            for model in model_list:
                print(' & ' + escape(model.replace('bloom', r'\bloom')), end='')
                for num, shotnum in enumerate(['zero-shot', 'one-shot']):
                    for s, score in enumerate('prf'):
                        if model not in results[shotnum] or template not in results[shotnum][model] or 'slim' not in results[shotnum][model][template]:
                            print('& -')
                        else:
                            value = "{:.2f}".format(round(results[shotnum][model][template]['slim']['results'][s]['fuzzy_list_' + score], 2)).replace('.', ',')
                            if value == '0':
                                value = '0.00'
                            print(' & ' + value, end=' ')
                print(r' \\')
            print('\midrule')
            

    # choose_entity results table
    print(r'\Prompt & Modèle & \# exemples & Précision \\')
    print('\midrule')
    for template in ['choose_entity']:
        print(r'\multirow{12}{*}{\promptex{' + escape(template) + r'}} ')
        for model in model_list:
            print(r' & \multirow{2}{*}{' + escape(model.replace('bloom', r'\bloom')) + r'}', end='')
            for num, shotnum in enumerate(['zero-shot', 'one-shot']):
                print((' & ' * (num + 1)) + str(num), end=' ')

                if model not in results[shotnum] or template not in results[shotnum][model] or 'slim' not in results[shotnum][model][template]:
                    print('& -')
                else:
                    value = "{:.2f}".format(round(results[shotnum][model][template]['slim']['results'][0]['acc'], 2)).replace('.', ',')
                    print(' & ' + value, end=' ')
                print(r' \\')
        print('\midrule')
        
    


if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('task_folder')
    args = parser.parse_args()

    results = read_results(args.task_folder)
    prepare_table(results)
