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
    first.description as ru,
    second.description as en
from description first
    inner join description second
        on first.checksum = second.checksum
    where first.language_code = 'ru' and second.language_code = 'en';
 """

ennlp = spacy.load('en_core_web_lg')
runlp = spacy.load('ru_core_news_lg')

def get_rows(text, nlp):
    return [sent.text for sent in nlp(text).sents]

def main():
    conn = psql.connect(**dbconn)
    curs = conn.cursor()
    curs.execute(query)
    rows = curs.fetchall()
    conn.close()

    with open('translation.csv', 'w') as file:
        writer = csv.writer(file, delimiter='|')
        for row in tqdm(rows):
            ru_text, en_text = row
            new_rows = tuple(zip(get_rows(ru_text, runlp), get_rows(en_text, ennlp)))
            writer.writerows(new_rows)

if __name__ == '__main__':
    main()
