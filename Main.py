import xml.etree.ElementTree as ET

class Pair:
    def __init__(self, pair_id, results=[],elo = 1000):
        self.pair_id = pair_id
        self.results = results
        self.elo = elo

    def add_result(self, result):
        self.results.append(result)

    def __str__(self):
        return f"Pair({self.pair_id}, {self.results})"

def concatenate_values_ordered(a, b):
    return a + "-" + b if a < b else b + "-" + a

root = ET.parse("Games.xml").getroot()
pairs_dict = {}
count = 0
# Iterate through all elements with a tag that starts with 'event-'
for event_element in root.iter():
    if event_element.tag.startswith("event-"):
        avgElo = 0
        count = 0 
        for pair_element in event_element.findall('.//pair'):
            count+=1
            pair_id = concatenate_values_ordered(pair_element.find('ibfn1').text, pair_element.find('ibfn2').text)
            if pair_id in pairs_dict:
                avgElo += pairs_dict[pair_id].elo
            else:
                avgElo +=1000
            # Iterate through each pair element within the event
        avgElo/= count
        print(avgElo)
        for pair_element in event_element.findall('.//pair'):
            pair_id = concatenate_values_ordered(pair_element.find('ibfn1').text, pair_element.find('ibfn2').text)
            restot = float(pair_element.find('restot').text)
            if pair_id in pairs_dict:
                pairs_dict[pair_id].add_result(restot)
            else:
                pair_obj = Pair(pair_id, [restot])
                pairs_dict[pair_id] = pair_obj

# Print the pairs with their accumulated results
for pair_id, pair_obj in pairs_dict.items():
    print(pair_obj)
