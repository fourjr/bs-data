#!/usr/bin/env python
"""
Generate data JSON from APK CSV source.
"""

import os
import csv
import json

import requests
import yaml

if __name__ == '__main__':
    all_data = {}

    with open('csv/texts.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        title = reader.fieldnames
        TID = {}
        for n, row in enumerate(reader):
            if n == 0:
                continue
            TID[row['TID']] = row['EN']

    try:
        with open('config.yml', encoding='utf-8') as f:
            config = yaml.load(f)
    except FileNotFoundError:
        config = {'id': []}

    if config.get('asset_url'):
        # update assets
        print('Syncing CSV Files')
        for i in os.listdir('csv/csv_client'):
            with open(f'csv/csv_client/{i}', 'w+', encoding='utf8') as f:
                data = requests.get(f"{config['asset_url']}/csv_client/{i}").text
                f.write('\n'.join([i for i in data.splitlines() if i]) + '\n')
        print('csv_client')

        for i in os.listdir('csv/csv_logic'):
            with open(f'csv/csv_logic/{i}', 'w+', encoding='utf8') as f:
                data = requests.get(f"{config['asset_url']}/csv_logic/{i}").text
                f.write('\n'.join([i for i in data.splitlines() if i]) + '\n')
        print('csv_logic')

        with open('csv/texts.csv', 'w+', encoding='utf8') as f:
            data = requests.get(f"{config['asset_url']}/localization/texts.csv").text
            f.write('\n'.join([i for i in data.splitlines() if i]) + '\n')

        print('CSV Files synced')

    csv_files = [('csv/csv_client/' + i, i) for i in os.listdir('csv/csv_client') if i.endswith('.csv')] + \
                [('csv/csv_logic/' + i, i) for i in os.listdir('csv/csv_logic') if i.endswith('.csv')]

    for fp, fn in csv_files:
        with open(fp, encoding='utf-8') as f:
            reader = csv.DictReader(f)

            title = reader.fieldnames

            data = []
            for n, row in enumerate(reader):
                if n == 0:
                    continue
                data.append({title[i][:1].lower() + title[i][1:]: row[title[i]] for i in range(len(title))})

            for n, i in enumerate(data):
                if fn in config['id']:
                    i['id'] = config['id'][fn] + n
                if fn in config['scId']:
                    i['scId'] = config['scId'][fn] + n
                i_keys = list(i.keys())
                for j in i_keys:
                    if isinstance(i[j], str):
                        if i[j].startswith('TID_'):
                            i['raw' + j[0].upper() + j[1:]] = i[j]
                            try:
                                i[j] = TID[i[j]]
                            except KeyError:
                                pass

                        # Typing
                        elif '.' in i[j]:
                            try:
                                i[j] = float(i[j])
                            except ValueError:
                                pass
                        else:
                            try:
                                i[j] = int(i[j])
                            except ValueError:
                                pass

                        if isinstance(i[j], str):
                            if i[j].lower() == 'true':
                                i[j] = True
                            elif i[j].lower() == 'false':
                                i[j] = False

                    if i[j] == '':
                        i[j] = None

                    # Clean
                    elif isinstance(i[j], str):
                        i[j] = i[j].strip()

            if fn == 'maps.csv':
                # make maps look cool
                rp_data = {}
                for i in data:
                    if i['group']:
                        latest_grp = i['group']
                        rp_data[i['group']] = [i['data']]
                    else:
                        rp_data[latest_grp].append(i['data'])
                data = {i: rp_data[i] for i in sorted(rp_data.keys())}

            with open('json/' + fn.replace('.csv', '.json'), 'w+') as f:
                json.dump(data, f, indent=4)

        all_data[fn.replace('.csv', '')] = data
        print(fp)

    # texts.csv
    with open('csv/texts.csv') as fp:
        reader = csv.DictReader(fp)
        data = {}
        for n, row in enumerate(reader):
            if n == 0:
                continue
            data[row['TID'].replace('TID_', '')] = row['EN']

        print('csv/texts.csv')
        all_data['texts'] = data

        with open('json/texts.json', 'w+') as f:
            json.dump(data, f, indent=4)

    # all.json
    with open('all.json', 'w+') as f:
        print('all.json')
        json.dump(all_data, f, indent=4)
