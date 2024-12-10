from geopy.distance import distance
from airport import Airport
from player import Player

class Game:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def calculate_distance(self, departure, arrival):
        try:
            # Fetch coordinates for both airports
            departure_coords = Airport.get_location(self.db_connection, departure)
            arrival_coords = Airport.get_location(self.db_connection, arrival)

            # Validate coordinates before calculating distance
            if departure_coords and arrival_coords:
                return distance(departure_coords, arrival_coords).km
            else:
                raise ValueError("Invalid airport coordinates.")
        except Exception as e:
            print(f"Error in calculating distance: {e}")
            return None

    def get_mission(self, player_level):

        sql = f"SELECT * FROM missions WHERE level_required <= {player_level}"
        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute(sql)
        missions = cursor.fetchall()
        return missions
