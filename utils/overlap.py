#!/usr/bin/env python3

"""
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


# import argparse

from utils.dp_utils import yield_overlaps
#is a perfect in-place replacement for go. 
def make_overlap(source, target, num_overlaps = 4):
    """
        Single method called directly from imports. Requires english and latin files? 
        source of these files is still unclear!
    """
    output = set()
    #print(source)
    # for fin in source:
    #                   rt = default for saying : Read(r) in Text(t) mode
    lines = open(source, 'rt', encoding="utf-8").readlines()
    #Generator expression is used here.
    for out_line in yield_overlaps(lines, num_overlaps):
        output.add(out_line)

    # for reproducibility
    output = list(output)
    output.sort()
    #                       wt = Write(w) in default Text(t) mode.
    with open(target, 'wt', encoding="utf-8") as fout:
        for line in output:
            fout.write(line + '\n')


#changed argument order and added default of 4 to num_overlaps to mimic args-read behaviour:           
#def go(output_file, input_files, num_overlaps):
# ASSESSMENT: you don't need to keep the go function, it's a redundant copy of make_overlap. 
# def go(input_files, output_file, num_overlaps=4):'
#     output = set()
#     for fin in input_files:
#         lines = open(fin, 'rt', encoding="utf-8").readlines()
#         for out_line in yield_overlaps(lines, num_overlaps):
#             output.add(out_line)

#     # for reproducibility
#     output = list(output)
#     output.sort()

#     with open(output_file, 'wt', encoding="utf-8") as fout:
#         for line in output:
#             fout.write(line + '\n')



"""
    this was part of the original function. It reads three arguments when called from the shell
    i
    o 
    n 

    Then it passes these arguments to a function go(o,n,i)                                 
                        
    We want to rewrite the calling instances to directly call overlap.go(o,n,i)
    
def _main():
    parser = argparse.ArgumentParser('Create text file containing overlapping sentences.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--inputs', type=str, nargs='+',
                        help='input text file(s).')

    parser.add_argument('-o', '--output', type=str,
                        help='output text file containing overlapping sentneces')

    parser.add_argument('-n', '--num_overlaps', type=int, default=4,
                        help='Maximum number of allowed overlaps.')

    args = parser.parse_args()
    go(output_file=args.output,
       num_overlaps=args.num_overlaps,
       input_files=args.inputs)


if __name__ == '__main__':
    _main()


"""



"""
        #original codebase calls like this: 
        ## generate overlaps file using the eng and lat sentences in the sentences_NH folder
        # !python overlap.py -i sentences_NH/engbook37 -o sentences_NH/engoverlaps37.eng -n 10
        # !python overlap.py -i sentences_NH/latbook37 -o sentences_NH/latoverlaps37.lat -n 10
        arg =    val                            ==> vecalign argument (original shellscript)
        i   = sentences_NH/engbook37            ==> 
        o   = sentences_NH/engoverlaps37.eng    ==> 
        n   = 10                                ==> 
"""