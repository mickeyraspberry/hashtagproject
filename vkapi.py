import requests

domain = "https://api.vk.com/method"
access_token = 'd491e79ed81c7e8a68afc9febb81ef47e04d4654fe582db37dd5a66f91797b71c44f273c38e1306f906c6'
men = {}
women = {}
group = {}
people = {}


def getNewsHashTag(hashtag):
    global men, women, group, people
    likes = 0
    views = 0
    query_params = {
        'domain': domain,
        'access_token': access_token,
        'q': '%23' + hashtag,
        'count': 200,
        'extended': 1,
        'fields': 'sex,bdate'
    }

    query = "{domain}/newsfeed.search?access_token={access_token}&q={q}&count={count}" \
            "&extended={extended}&fields={fields}&v=5.65".format(**query_params)

    p = requests.get(query).json()

    for i in p['response']['profiles']:
        if i['id'] in men or i['id'] in women:
            continue
        if i['sex'] == 1:
            women[i['id']] = i
        else:
            men[i['id']] = i

    for i in p['response']['items']:
        hashstring = str(i['owner_id']) + i['text'] + str(i['date'])
        if i['owner_id'] >= 0:
            people[hashstring] = i
        else:
            group[hashstring] = i

    for v,k in people.items():
        if 'views' in k:
            views = views + k['views']['count']
        if 'likes' in k:
            likes = likes + k['likes']['count']

    for v,k in group.items():
        if 'views' in k:
            views = views + k['views']['count']
        if 'likes' in k:
            likes = likes + k['likes']['count']

    print('ok')
    return [likes, views]