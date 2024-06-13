"""

Modified version of the 2019 script by Brian Thompson shared under
the Apache V2 License: 

Copyright 2019 Brian Thompson

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
from math import ceil 
from random import seed as seed
import numpy as np
import pickle

logger = logging.getLogger('vecalign')
logger.setLevel(logging.WARNING)
logFormatter = logging.Formatter("%(asctime)s  %(levelname)-5.5s  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

from utils.dp_utils import make_alignment_types, make_one_to_many_alignment_types, print_alignments, read_alignments, \
    read_in_embeddings, make_doc_embedding, vecalign

from utils.score import score_multiple, log_final_scores


def vecalign_custom(src, 
             tgt, 
             src_embed, 
             tgt_embed, 
             debug_save_stack:bool= False, 
             print_aligned_text = False , 
             gold_alignment = None, 
             search_buffer_size:int = 5, 
             num_samps_for_norm:int = 100, 
             costs_sample_size:int = 20000, 
             max_size_full_dp:int = 300, 
             del_percentile_frac:float = 0.2, 
             alignment_max_size:int = 4, 
             one_to_many:int = None, 
             verbose = False
             ):
    """
    src         preprocessed source file to align       (path to file)
    tgt         preprocessed target file to align       (path to file)
    gold_alignment  preprocessed target file to align   (?path to file?)
    src_emded       Source embeddings. Requires two arguments: first is a text file, sencond is a binary embeddings file        (?tuple of two string?)
    tgt_embed       Target embeddings. Requires two arguments: first is a text file, sencond is a binary embeddings file        (?tuple of two strings?)
    alignment_max_size  Searches for alignments up to size N-M, where N+M <= this value. Note that the the embeddings must support the requested number of overlaps (int)
    """
    # make runs consistent
    seed(42)
    np.random.seed(42)
    
    n = src.split('engbook')[-1].strip()

    if len(src) != len(tgt):
        raise Exception('number of source files must match number of target files')
    
    if gold_alignment is not None:
        if len(gold_alignment) != len(src):
            raise Exception('number of gold alignment files, if provided, must match number of source and target files')
        
    if verbose:
        import logging
        logger.setLevel(logging.INFO)

    if alignment_max_size < 2:
        logger.warning('Alignment_max_size < 2. Increasing to 2 so that 1-1 alignments will be considered')
        alignment_max_size = 2


    ##SPECIAL CASE WITH one_to_many: 
    # without flag: one_to_many==default, with flag but no argument: one_to_many==const, with flag and argument: one_to_many==argument
    # parser.add_argument('--one_to_many', type=int, nargs='?', default=None, const=50,
    #                     help='Perform one to many (e.g. 1:1, 1:2, ... 1:M) alignment.'
    #                     ' Argument specifies M but will default to 50 if flag is set but no argument is provided. Overrides --alignment_max_size (-a).')
    if one_to_many == '': 
        one_to_many = 50

    src_sent2line, src_line_embeddings = read_in_embeddings(src_embed[0], src_embed[1])
    tgt_sent2line, tgt_line_embeddings = read_in_embeddings(tgt_embed[0], tgt_embed[1])

    src_max_alignment_size = 1 if one_to_many is not None else alignment_max_size
    tgt_max_alignment_size = one_to_many if one_to_many is not None else alignment_max_size

    width_over2 = ceil(max(src_max_alignment_size, tgt_max_alignment_size) / 2.0) + search_buffer_size

    test_alignments = []
    stack_list = []
    # for src_file, tgt_file in zip(src, tgt):
    #     print(src_file)
    # for src_file, tgt_file in zip(src, tgt):
    src_file = src
    tgt_file = tgt
    logger.info('Aligning src="%s" to tgt="%s"', src_file, tgt_file)
    src_lines = open(src_file, 'rt', encoding="utf-8").readlines()
    vecs0 = make_doc_embedding(src_sent2line, src_line_embeddings, src_lines, src_max_alignment_size)

    tgt_lines = open(tgt_file, 'rt', encoding="utf-8").readlines()
    vecs1 = make_doc_embedding(tgt_sent2line, tgt_line_embeddings, tgt_lines, tgt_max_alignment_size)

    if one_to_many is not None:
        final_alignment_types = make_one_to_many_alignment_types(one_to_many)
    else:
        final_alignment_types = make_alignment_types(alignment_max_size)
    logger.debug('Considering alignment types %s', final_alignment_types)

    stack = vecalign(vecs0=vecs0,
                        vecs1=vecs1,
                        final_alignment_types=final_alignment_types,
                        del_percentile_frac=del_percentile_frac,
                        width_over2=width_over2,
                        max_size_full_dp=max_size_full_dp,
                        costs_sample_size=costs_sample_size,
                        num_samps_for_norm=num_samps_for_norm)
    # write final alignments to stdout
    print_alignments(stack[0]['final_alignments'], scores=stack[0]['alignment_scores'],
                        src_lines=src_lines if print_aligned_text else None,
                        tgt_lines=tgt_lines if print_aligned_text else None)
    
    filename_persist = f'data/intermediate/alignments/sentence_pairs_alignment{n}.txt'
    with open(filename_persist, 'w+') as output_file:
        for alignment, score in zip(stack[0]['final_alignments'], stack[0]['alignment_scores']):
            output_file.write(f"{alignment} {score}\n")

    test_alignments.append(stack[0]['final_alignments'])
    stack_list.append(stack)

    if gold_alignment is not None:
        gold_list = [read_alignments(x) for x in gold_alignment]
        res = score_multiple(gold_list=gold_list, test_list=test_alignments)
        log_final_scores(res)

    if debug_save_stack:
        pickle.dump(stack_list, open(debug_save_stack, 'wb'))







# # TODO: implement this like it should be!
# #   not sure where this is supposed to go, there's no calling instance to this entire class
# #test code: 
# data_source = ''
# data_target = ''
# source_embed = ''
# target_embed = ''
# print_aligned_text = ''
# vecalign(
#     data_source,
#     data_target,
#     source_embed,
#     target_embed,
#     print_aligned_text
# )
