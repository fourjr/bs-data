#!/usr/bin/env python
"""
Generate data JSON from APK CSV source.
"""

import os
import csv
import json

import yaml

if __name__ == '__main__':
    with open('csv/texts.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        title = reader.fieldnames
        TID = {}
        for n, row in enumerate(reader):
            if n == 0:
                continue
            TID[row['TID']] = row['EN']

    with open('config.yml', encoding='utf-8') as f:
        config = yaml.load(f)

    csv_files = ['csv/csv_client/' + i for i in os.listdir('csv/csv_client') if i.endswith('.csv')] + \
                ['csv/csv_logic/' + i for i in os.listdir('csv/csv_logic') if i.endswith('.csv')]

    for file in csv_files:
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)

            title = reader.fieldnames

            data = []
            for n, row in enumerate(reader):
                if n == 0:
                    continue
                data.append({title[i][:1].lower() + title[i][1:]: row[title[i]] for i in range(len(title))})

            for n, i in enumerate(data):
                if file in config['id']:
                    i['id'] = config['id'][file] + n
                for j in i:
                    if isinstance(i[j], str):
                        if i[j].startswith('TID_'):
                            try:
                                i[j] = TID[i[j]]
                            except KeyError:
                                pass
                    if i[j] == '':
                        i[j] = None

            json_fp = 'json/' + file.replace('csv/', '').replace('.csv', '') + '.json'
            with open(json_fp, 'w+') as f:
                json.dump(data, f, indent=4)

        print(file)
