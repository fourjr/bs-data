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
    TID = {}
    for i in os.listdir('localization'):
        with open(f'localization/{i}', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            title = reader.fieldnames
            lang = i.replace('.csv', '')
            if lang == 'texts':
                lang = 'en'

            TID[lang] = {}
            for n, row in enumerate(reader):
                if n == 0:
                    continue
                TID[lang][row['TID']] = row[lang.upper()]

    all_data = {i: {} for i in TID}

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
                        if j == 'tID':
                            i['raw' + j[0].upper() + j[1:]] = i[j].replace('TID_', '')

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
            else:
                # languages
                for lang in TID:
                    for n, i in enumerate(data):
                        i_keys = list(i.keys())
                        for j in i_keys:
                            if j == 'rawTID':
                                try:
                                    i['tID'] = TID[lang]['TID_' + i['rawTID']]
                                except KeyError:
                                    pass

                with open(f"json/{lang}/{fn.replace('.csv', '.json')}", 'w+') as f:
                    json.dump(data, f, indent=4)

                all_data[lang][fn.replace('.csv', '')] = data

        print(fp)

    # tid.json
    for i in TID:
        with open(f'json/{i}/tid.json', 'w+') as f:
            json.dump(TID[i], f, indent=4)

    # all.json
    for i in all_data:
        with open(f'json/{i}/all.json', 'w+') as f:
            print(f'json/{i}/all.json')
            json.dump(all_data[i], f, indent=4)
