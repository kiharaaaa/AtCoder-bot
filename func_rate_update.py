import requests

def exe(contest):
    url = f'https://atcoder.jp/contests/' + contest + '/results/json'
    response = requests.get(url).json()
    if response == []:
        return False, []

    lines=[]
    with open("setting.txt", "r") as f:
        lines = f.readlines()
    members = lines[4].split()
    members.pop(0)
    num = len(members)

    list = []

    for p in response:
        for member in members:
            if p['UserName'] == member:
                result = []
                oldRate = abs(p['OldRating'])
                newRate = abs(p['NewRating'])
                difference = newRate - oldRate
                if difference > 0:
                    difference = "+" + str(difference)
                performance = p["Performance"]

                oldRate = str(oldRate)
                newRate = str(newRate)
                difference = str(difference)
                performance = str(performance)

                result.append(member)
                result.append(oldRate)
                result.append(newRate)
                result.append(difference)
                result.append(performance)

                list.append(result)

    list = sorted(list, reverse=True, key=lambda x: x[4])
    return True, list
