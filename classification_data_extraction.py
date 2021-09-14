#!/usr/bin/env python3

import csv
import spacy
from tqdm import tqdm

import psycopg2 as psql

dbconn = {
    'dbname': '<database>',
    'user': '<user>',
    'password': 'postgres',
    'host': 'postgres',
}

query = """
select 
    description.description as text,
    cwe.cwe_id as cwe_idx,
    meta.cvss_3_score as cvss_3_score,
    meta.cvss_3 as cvss_3 
from meta 
    inner join meta_to_cwe
        ON meta_to_cwe.meta_id = meta.meta_id
    inner join cwe
        on cwe.cwe_id = meta_to_cwe.cwe_id
    inner join description 
        ON description.meta_id = meta.meta_id
    where meta.cvss_3_score != '0.00000'
"""

def main():
    conn = psql.connect(**dbconn)
    curs = conn.cursor()
    curs.execute(query)
    rows = curs.fetchall()
    conn.close()

    with open('classification.csv', 'w') as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerow(('desc', 'cwe', 'cvss_3_score', 'cvss_3'))
        writer.writerows(rows)

if __name__ == '__main__':
    main()
