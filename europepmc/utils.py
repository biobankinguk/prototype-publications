import requests
from .models import Publication


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(set(list2))))
    union = (len(set(list1)) + len(set(list2))) - intersection

    jaccard_index = float(intersection) / union

    # if jaccard_index > 0.03:
    #     print('>>>> {}'.format(jaccard_index))
    #     print(set(list1))
    #     print(set(list2))

    result = {
        'jaccard_index': jaccard_index,
        'common_annotations': set(list1).intersection(set(list2))
    }

    return result


def get_europepmc_annotations(article_id):

    articles_endpoint = 'https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?articleIds={}&format=JSON'

    r_articles = requests.get(articles_endpoint.format(article_id))

    results = []

    for annotation in r_articles.json()[0]['annotations']:

        try:
            exact = annotation['exact']

        except:
            exact = ''

        results.append(exact)
    
    return results


def calculate_recomendation(article_id):

    result = []

    publication_annotation_list_a = get_europepmc_annotations(article_id)

    biobank_publication_list = Publication.objects.exclude(pid=article_id.split(':')[1])

    for publication in biobank_publication_list:

        publication_annotation_list_b = [x.exact for x in publication.annotations.all()]

        response = jaccard_similarity(publication_annotation_list_a, publication_annotation_list_b)

        obj = {
            'jaccard_index': response['jaccard_index'],
            'publication': publication,
            'common_annotations': response['common_annotations']
        }

        result.append(obj)

    return sorted(result, key=lambda x: x['jaccard_index'], reverse=True)
