import xml.etree.ElementTree as ET

class Pair:
    def __init__(self, pair_id, elo=1000.0, games=0):
        # Initialize the Pair object with ID, ELO rating, and number of games played
        self.pair_id = pair_id
        self.elo = elo
        self.games = games

    def __str__(self):
        # String representation for easy printing
        return f"ID: {self.pair_id}, ELO: {self.elo}, Games: {self.games}"


def concatenate_values_ordered(a, b):
    # Concatenate two strings in alphabetical order
    return a + "-" + b if a < b else b + "-" + a


def print_pair(pair_id, current_id, elo, avg_elo, result, new_elo):
    # Print details if the pair_id matches the specified ID
    if pair_id == current_id:
        print(f"Current ELO: {elo}")
        print(f"Average ELO: {avg_elo}")
        print(f"Result: {result}")
        print(f"New ELO: {new_elo}")
        print("--------------------")


def main():
    # Parse the XML file
    tree = ET.parse("Games.xml")
    root = tree.getroot()
    
    pairs_dict = {}
    gain1 = 4
    gain2 = 1  # ELO gain constant
    print_id = "2345-3366"  # Example ID to print details for

    for event_element in root.iter():
        if event_element.tag.startswith("event-"):
            avg_elo = 0.0
            count = 0
            # Calculate average ELO for all pairs in the event
            for pair_element in event_element.findall('.//pair'):
                count += 1
                pair_id = concatenate_values_ordered(pair_element.find('ibfn1').text, pair_element.find('ibfn2').text)
                avg_elo += pairs_dict.get(pair_id, Pair(pair_id)).elo
            avg_elo /= count if count > 0 else 1
            avg_elo = round(avg_elo, 2)
            
            # Update ELO ratings for each pair
            for pair_element in event_element.findall('.//pair'):
                pair_id = concatenate_values_ordered(pair_element.find('ibfn1').text, pair_element.find('ibfn2').text)
                restot = float(pair_element.find('restot').text)
                pair_obj = pairs_dict.get(pair_id, Pair(pair_id))
                pair_obj.games += 1
                new_elo = round(pair_obj.elo + gain1 * (restot - 50) + gain2 * (avg_elo - pair_obj.elo),2)
                print_pair(pair_id, print_id, pair_obj.elo, avg_elo, restot, new_elo)
                pair_obj.elo = new_elo
                pairs_dict[pair_id] = pair_obj
    

if __name__ == "__main__":
    main()
    # Print candidait ID's that are good for example
    # for pair_id, pair_obj in pairs_dict.items():
    #     if pair_obj.elo>1000 and pair_obj.games<10 and pair_obj.games>5:
    #         print(pair_obj)