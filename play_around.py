import requests
import time

base_url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'

res1 = requests.get(base_url, params={'query': 'ACK_FUND:UK Biobank', 'format': 'json'})
next_marker = res1.json().get('nextCursorMark', '')
hit_count = res1.json().get('hitCount', 0)
# print(res1.url)
res1.close()
results = res1.json().get('resultList').get('result')
while next_marker != '*' and next_marker != '':

    res2 = requests.get(base_url, params={'query': 'ACK_FUND:UK Biobank',
                                          'cursorMark': next_marker,
                                          'format': 'json'})
    next_marker = res2.json().get('nextCursorMark', '')
    # print(next_marker)
    arts = res2.json().get('resultList').get('result')
    if not arts:
        break
    results.extend(arts)
    res2.close()
    # time.sleep(0.1)
    print(hit_count, len(results), next_marker)
assert len(results) == hit_count
