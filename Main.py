import time
import xml.etree.ElementTree as ET

class Pair:
    def __init__(self, pair_id, elo=1000.0, games=0, online_elo=1000.0, online_games=0):
        self.pair_id = pair_id
        self.physical_elo = elo
        self.games = games
        self.online_elo = online_elo  # Second ELO for event type 4
        self.online_games = online_games  # Count of online games

    def __str__(self):
        return (f"Pair ID: {self.pair_id}, Phisycal ELO: {self.physical_elo}, Online ELO: {self.online_elo}, "
                f"Phisycal Games: {self.games}, Online Games: {self.online_games}")

def concatenate_values_ordered(a, b):
    return a + "-" + b if a < b else b + "-" + a

def print_pair(type,pair_id, current_id, elo, online_elo, avg_elo, result, new_elo,new_online_elo):
    if pair_id == current_id:
        if type =="4":
            print("Online game")
        else: 
            print("Regular game")
        print(f"Current ELO: {elo}")
        print(f"Online ELO: {online_elo}")
        print(f"Average ELO: {avg_elo}")
        print(f"Result: {result}")
        print(f"Updated Pyhisical ELO: {new_elo}")
        print(f"Updated Online ELO: {new_online_elo}")
        print("--------------------")

def main():
    tree = ET.parse("Games.xml")
    root = tree.getroot()
    
    pairs_dict = {}
    gain1 = 4
    print_id = "11003-9605"  # Example ID to print details for

    for event_element in root.iter():
        if event_element.tag.startswith("event-"):
            avg_elo = 0.0
            count = 0
            event_type = event_element.find('.//info/eventtype').text
            
            # Calculate average ELO for the event
            for pair_element in event_element.findall('.//pair'):
                count += 1
                ibfn2 = pair_element.find('ibfn2').text
                if ibfn2 is None:
                    ibfn2 = "None"
                pair_id = concatenate_values_ordered(pair_element.find('ibfn1').text, ibfn2)

                avg_elo += pairs_dict.get(pair_id, Pair(pair_id)).physical_elo
            avg_elo /= count if count > 0 else 1
            avg_elo = round(avg_elo, 2)            
    
            # Update ELO ratings for each pair
            for pair_element in event_element.findall('.//pair'):
                ibfn2 = pair_element.find('ibfn2').text
                if ibfn2 is None:
                    ibfn2 = "None"
                pair_id = concatenate_values_ordered(pair_element.find('ibfn1').text, ibfn2)
                
                restot = pair_element.find('restot').text
                if restot is None or "\n" in restot:
                    avg = 0
                    count = 0
                    for i in range(1, 11):
                        tag = 'res' + str(i)
                        if pair_element.find(tag) is not None and pair_element.find(tag).text != "\n" and " " not in pair_element.find(tag).text and pair_element.find(tag).text != '':
                            avg += float(pair_element.find(tag).text)
                            count += 1
                    restot = float(avg / count)

                restot = float(restot)
                pair_obj = pairs_dict.get(pair_id, Pair(pair_id))
                                
                    
                if event_type == '4':
                    pair_obj.online_games += 1
                    new_online_elo = round(pair_obj.online_elo + gain1 * (restot - 50) + (avg_elo - pair_obj.online_elo), 2)
                    print_pair("4",pair_id, print_id, pair_obj.physical_elo, pair_obj.online_elo, avg_elo, restot, pair_obj.physical_elo ,new_online_elo)
                    pair_obj.online_elo = new_online_elo
                else:
                    pair_obj.games += 1
                    new_elo = round(pair_obj.physical_elo + gain1 * (restot - 50) +  (avg_elo - pair_obj.physical_elo), 2)
                    print_pair("0",pair_id, print_id, pair_obj.physical_elo, pair_obj.online_elo, avg_elo, restot, new_elo,pair_obj.online_elo)
                    pair_obj.physical_elo = new_elo
                pairs_dict[pair_id] = pair_obj

    return pairs_dict

if __name__ == "__main__":
    pairs_dict = main()
    threshold = 75  # Example threshold
    for pair_id, pair_obj in pairs_dict.items():
        if pair_obj.online_elo > pair_obj.physical_elo + threshold and pair_obj.online_elo != 1000 and pair_obj.games > 6:
            print(f"Significantly higher ELO: {pair_obj}")
