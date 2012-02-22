from math import sqrt
from pprint import pprint

critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0, 
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5
    },
    'Toby': {
        'Snakes on a Plane':4.5,
        'You, Me and Dupree':1.0,
        'Superman Returns':4.0
    }
}

def movies():
    movies = {}
    for name in critics:
        for movie in critics[name]:
            if movies.get(movie, None) is None: movies[movie] = {}
            movies[movie][name] = critics[name][movie]
    return movies

def shared(dicta, dictb):
    """Return the keys reflecting the intersection of two dictionaries"""
    shared_items = []
    for key in dicta:
        if key in dictb:
            shared_items.append(key)
    return shared_items


def euclidean_distance(preferences, a, b):
    shared_items = shared(preferences[a], preferences[b])
    if len(shared_items) == 0: return 0

    sum_of_squares = sum(
            [pow(preferences[a][item] - preferences[b][item], 2) for item in shared_items]
        )
    return 1/(1+sqrt(sum_of_squares))

def pearson_correlation(preferences, a, b):
    shared_items = shared(preferences[a], preferences[b])
    total = len(shared_items);
    if total == 0: return 0

    sum1 = sum([preferences[a][i] for i in shared_items])
    sum2 = sum([preferences[b][i] for i in shared_items])

    sum1Sq = sum([pow(preferences[a][i],2) for i in shared_items])
    sum2Sq = sum([pow(preferences[b][i],2) for i in shared_items])

    pSum = sum([preferences[a][i]*preferences[b][i] for i in shared_items])

    distance = sqrt((sum1Sq - pow(sum1,2)/total) *
                    (sum2Sq - pow(sum2,2)/total))
    if distance == 0: return 0
    return (pSum-(sum1*sum2/total))/distance

def similar_on_same_axis(data, origin, limit, comparison):
    scores = [(comparison(data, origin, other), other) for other in data if
            other != origin]
    scores.sort( )
    scores.reverse( )
    return scores[0:limit]

def similar_on_other_axis(data, origin, comparison):
    totals = {}
    sums   = {}
    for other in data:
        if other == origin: continue
        similarity = comparison(data, origin, other)
        if similarity < 0: continue
        for item in data[other]:
            if item not in data[origin] or data[origin][item] is None:
                totals.setdefault(item,0)
                totals[item] += data[other][item] * similarity
                sums.setdefault(item,0)
                sums[item] += similarity
    rankings = [(total/sums[item], item) for item, total in totals.items( )]
    rankings.sort()
    rankings.reverse()
    return rankings


def compare_all(how):
    for critic in critics:
        for other_critic in critics:
            if critic == other_critic: continue
            compare(how, critic, other_critic)

def compare(how, critic, other_critic):
    difference = how(critics, critic, other_critic)
    print("%f     %s <=> %s" % (difference, critic, other_critic))

#print compare_all(euclidean_distance)
#compare_all(pearson_correlation)
#print movies()
#print similar_on_same_axis(movies(), 'Lady in the Water', 5, pearson_correlation)
pprint(similar_on_other_axis(critics, 'Toby', pearson_correlation))
