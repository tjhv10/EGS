import xml.etree.ElementTree as ET

class Pair:
    def __init__(self, pair_id, elo=1000.0, games=0):
        self.pair_id = pair_id
        self.elo = elo
        self.games = games

    def __str__(self):
        return f"ID: {self.pair_id}, ELO: {self.elo}, Games: {self.games}"


def concatenate_values_ordered(a, b):
    return a + "-" + b if a < b else b + "-" + a


def printPair(curId,okId,elo,avg_elo,restot,res):
    if curId==okId:
        print("current ELO: "+str(elo))
        print("avg ELO: "+str(avg_elo))
        print("result: "+str(restot))
        print("new ELO: "+str(round(res, 2)))
        print("--------------------")


    
def main():
    root = ET.parse("Games.xml").getroot()
    pairs_dict = {}
    gain = 7
    printId = "40854-49-335"
    for event_element in root.iter():
        if event_element.tag.startswith("event-"):
            avg_elo = 0.0
            count = 0
            for pair_element in event_element.findall('.//pair'):
                count += 1
                pair_id = concatenate_values_ordered(pair_element.find('ibfn1').text, pair_element.find('ibfn2').text)
                if pair_id in pairs_dict:
                    avg_elo += pairs_dict[pair_id].elo
                else:
                    avg_elo += 1000.0
            avg_elo /= count
            avg_elo = round(avg_elo, 2)               
            for pair_element in event_element.findall('.//pair'):
                pair_id = concatenate_values_ordered(pair_element.find('ibfn1').text, pair_element.find('ibfn2').text)
                restot = float(pair_element.find('restot').text)
                if pair_id in pairs_dict:
                    pairs_dict[pair_id].games += 1
                    res = pairs_dict[pair_id].elo + gain * (restot - 50) + avg_elo - pairs_dict[pair_id].elo
                    printPair(pair_id,printId,pairs_dict[pair_id].elo,avg_elo,restot,res)
                    pairs_dict[pair_id].elo = round(res, 2)
                else:
                    pair_obj = Pair(pair_id)
                    pairs_dict[pair_id] = pair_obj
                    pairs_dict[pair_id].games += 1
                    res = pairs_dict[pair_id].elo + gain * (restot - 50) + avg_elo - pairs_dict[pair_id].elo
                    printPair(pair_id,printId,pairs_dict[pair_id].elo,avg_elo,restot,res)
                    pairs_dict[pair_id].elo = round(res, 2)
    # for pair_id, pair_obj in pairs_dict.items():
    #     if pair_obj.elo>1000:
    #         print(pair_obj)
main()


