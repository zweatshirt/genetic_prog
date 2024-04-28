# Author: Zachery Linscott

def read_file(file):
        data = []
        with open(file, 'r') as f:
            data = [line.strip() for line in f]
        return data


def write_file(file, data):
     with open(file, 'w') as f:
         for d in data:
             f.write(d + '\n')


# simple function to create files
def create_file(path, ranges):
    with open(path, 'w') as f:
        if 'negatives.bed' in path:
            for range in ranges:
                f.write('\t'.join(str(val) for val in range) + '\n')
        else:
            for range in ranges:
                f.write(range[-1] + '\n')
