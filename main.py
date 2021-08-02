'''
File: main.py
This file creates a command line application that enables interaction
with each of the different oracle protocols
'''

import argparse

def parse_args():
    '''
    Creates parser to grab arguments from the command line
    '''
    parser = argparse.ArgumentParser(description="This file creates a command line application that enables interaction with each of the different oracle protocols")
    parser.add_argument('-o', '--oracle',
                        help="CSV file to write the results to",
                        default="tellor")
    parser.add_argument('-f', '--function',
                        help="Function to use for each specific oracle",)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    '''
    Grabs arguments and runs!
    '''
    args = parse_args()
    print(args.oracle)