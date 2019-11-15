import requests
from .models import Biobank, Publication


def jaccard_similarity(list1_original, list2_original):

    list1 = [item.lower() for item in list1_original]
    list2 = [item.lower() for item in list2_original]

    intersection = len(list(set(list1).intersection(set(list2))))
    union = (len(set(list1)) + len(set(list2))) - intersection

    jaccard_index = float(intersection) / union

    # if jaccard_index > 0.03:
    #     print('>>>> {}'.format(jaccard_index))
    #     print(set(list1))
    #     print(set(list2))

    result = {
        'jaccard_index': jaccard_index,
        'common_annotations': ', '.join(sorted(set(list1).intersection(set(list2))))
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

    biobank_list = Biobank.objects.all()

    for biobank in biobank_list:

        annotation_list_b = biobank.exact_annotations.split(',')

        response = jaccard_similarity(publication_annotation_list_a, annotation_list_b)

        obj = {
            'jaccard_index': response['jaccard_index'],
            'biobank': biobank,
            'common_annotations': response['common_annotations']
        }

        result.append(obj)

    return sorted(result, key=lambda x: x['jaccard_index'], reverse=True)


def calculate_recomendation_by_publication(article_id):

    result = []

    publication_annotation_list_a = get_europepmc_annotations(article_id)

    biobank_publication_list = Publication.objects.exclude(pid=article_id.split(':')[1])

    for publication in biobank_publication_list:

        publication_annotation_list_b = [x.exact for x in publication.annotations.all()]

        response = jaccard_similarity(publication_annotation_list_a, publication_annotation_list_b)

        obj = {
            'jaccard_index': response['jaccard_index'],
            'publication': publication,
            'biobank': publication.biobank,
            'common_annotations': response['common_annotations']
        }

        result.append(obj)

    uniq_biobank = set()
    uniq_result = []

    for p in sorted(result, key=lambda x: x['jaccard_index'], reverse=True):

        if p['biobank'] not in uniq_biobank:

            uniq_biobank.add(p['biobank'])

            uniq_result.append(p)

    return uniq_result
