import unicodecsv as csv
import time

from googleapiclient.discovery import build

# create service object for querying
key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
service = build('translate', 'v2', developerKey=key)

# main translate function
def translate(word, language):

    try:
        return service.translations().list(
            q=word,
            target=language,
        ).execute()['translations'][0]['translatedText']

    except:
        # return None on any errors
        return None


# define languages
languages = {
    'es': 'spanish',
    'de': 'german',
    'ga': 'gaelic',
    'nl': 'dutch',
    'fr': 'french',
    'ca': 'catallan',
    'haw': 'hawaiian',
    'ko': 'korean',
    'ja': 'japanese',
}

if __name__ == '__main__':

    # read in words
    words = [line.rstrip('\n') for line in open('words.txt')]

    # read in results we already have
    with open('output.csv') as f:
        reader = csv.DictReader(f)
        existing_words = set([row['word'] for row in reader])

    # get diff of desired words and words we've already translated
    words = list(set(words) - set(existing_words))

    # iterate through words
    for word in words:

        # create empty list to contain results
        results = []

        # iterate through languages
        for lang, pretty_lang in languages.items():

            # get translation
            translation = translate(word, lang)

            print lang, pretty_lang, word, translation

            # add result
            results.append(dict(
                language=pretty_lang,
                language_code=lang,
                word=word,
                translation=translation,
            ))

        # append batch of word's results to csv
        with open('output.csv', 'a') as f:
            keys = results[0].keys()
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writerows(results)

        time.sleep(3)
