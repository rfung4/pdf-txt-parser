import json
import re
import sys
import os

DEFAULT_INPUT_FILE_NAME = 'INPUT.TXT'
data_point_regex = re.compile('(N/A|[0-9]+%|[0-9]+,?[0-9]?\\.?[0-9]+)')

flag_map = {  # Flags are distinctive features used to identify lines containing values
    'EPS': 'EPS attributable to common stockholders, basic (non-GAAP)',
    'Total revenues': 'Total revenues',
    'Free cash flow': 'Cash and cash equivalents',
    'Net Income': 'income attributable to common stockholders (GAAP)'
}


def run(file_name=DEFAULT_INPUT_FILE_NAME):
    line_map = {}

    print("Reading text file...\n")
    with open(file_name) as file:  # Read text file and get line map using flags
        for line in file:
            for k, v in flag_map.items():
                if v in line:
                    line_map[k] = line

    results = {}  # JSON results dict

    for label, line in line_map.items():
        values = data_point_regex.findall(line)
        results[label] = values[-3]
        print(f"Parsed {label}: {results[label]}")

    with open('txt_results.json', 'w') as fp:
        json.dump(results, fp)

    output = f'{os.path.dirname(os.path.abspath(__file__))}\{"txt_results.json"}'
    print(f"\nExecution complete, output written to: {output}")


if __name__ == '__main__':
    param = ''

    try:
        param = sys.argv[1]
    except IndexError:
        pass

    if param:
        print(f"Parsing txt file with name: {param}")
    else:
        print(f"Parsing txt file with name {DEFAULT_INPUT_FILE_NAME}")

    run(param) if param else run()




