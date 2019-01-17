
# -*- coding: utf-8 -*-

import os
import argparse
import BUFS_KoSpacing as ks

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    path = os.getcwd()  # C:\Users\dz\Desktop\BUFS_KoSpacing

    sp = ks.SpacingModule(path)

    output = open('.\output.txt', 'w', encoding='utf-8')

    with open(args.input, encoding='utf-8-sig') as file:
        for each_line in file:
            string = each_line
            result = sp.spacing(string)
            print(result)
            print(result, file=output)
