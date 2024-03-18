#party_game
import random
import json

# Load game configuration from a JSON file with error handling
def load_configuration(file_path):
    try:
        with open(file_path) as f:
            config = json.load(f)
            if "places" not in config or not config["places"] or "weapons" not in config or not config["weapons"]:
                raise ValueError("Configuration file must include non-empty 'places' and 'weapons' lists.")
            return config
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file not found. Please ensure it is in the correct path.")
    except json.JSONDecodeError:
        raise ValueError("Error decoding JSON from the configuration file. Please ensure it is properly formatted.")
    except ValueError as e:
        raise ValueError(e)

class Player:
    def __init__(self, name):
        self.name = name
        self.lastVisitedPlaces = []
        self.favoriteWeapons = []
        self.isAssassin = False

    def visitPlaces(self, places):
        num_places_to_visit = min(len(places), random.randint(1, 3))  
        self.lastVisitedPlaces = random.sample(places, num_places_to_visit)

    def chooseFavoriteWeapons(self, weapons):
        num_weapons_to_choose = min(len(weapons), random.randint(1, len(weapons)))  
        self.favoriteWeapons = random.sample(weapons, num_weapons_to_choose)

    def suspectPlayers(self, players):
        suspects = random.sample(players, 2)
        print(f"{self.name} suspects {', '.join([s.name for s in suspects])}")
        return suspects

    def accusePlayer(self, players):
        accused = random.choice(players)
        print(f"{self.name} accuses {accused.name}")
        return accused

class Game:
    def __init__(self, places, weapons, num_players):
        if not places or not weapons or num_players < 2:
            raise ValueError("Invalid game setup: Ensure there are enough places, weapons, and at least two players.")
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.places = places
        self.weapons = weapons
        self.assassin = random.choice(self.players)
        self.assassin.isAssassin = True
        self.isOver = False

    def startGame(self):
        for player in self.players:
            player.visitPlaces(self.places)
            player.chooseFavoriteWeapons(self.weapons)
        print("The game has started.")

    def nextRound(self):
        murder_place = random.choice(self.places)
        murder_weapon = random.choice(self.weapons)
        self.assassin.visitPlaces([murder_place])
        if murder_weapon not in self.assassin.favoriteWeapons:
            self.assassin.favoriteWeapons.append(murder_weapon)

        print(f"A murder happened at {murder_place} with a {murder_weapon}.")

        for player in self.players:
            if player is not self.assassin:
                suspects = player.suspectPlayers(self.players)
                accused = player.accusePlayer(suspects)
                if accused is self.assassin:
                    print(f"{player.name} has correctly accused the assassin. Game over.")
                    self.isOver = True
                    return

        if not self.isOver and len(self.players) <= 2:
            print("The assassin wins.")
            self.isOver = True

    def play(self):
        self.startGame()
        while not self.isOver:
            self.nextRound()

# Main function to run the game with error handling
def main():
    config_path = "c:/Users/aseel/Downloads/BackendCourse/week5/lecture11/game_config.json"
    try:
        config = load_configuration(config_path)
        places = config["places"]
        weapons = config["weapons"]
        num_players = 5  

        game = Game(places, weapons, num_players)
        game.play()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()