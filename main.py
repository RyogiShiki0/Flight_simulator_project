from game import Game
from database_service import DatabaseService
from player import Player

def main():
    player = None
    print("Welcome to Nordic Flight Simulator!")

    # Loop until valid choice is given
    while True:
        print("[1] Start a New Game")
        print("[2] Load Saved Game")
        choice = input("Please select an option: ")

        if choice == "1":
            # Start a new game
            name = input("Enter your player name: ")
            player = Player(name)  # Create a new player
            db_service = DatabaseService()
            player.save_to_db(db_service.connection)  # Save player to the database
            break
        elif choice == "2":
            # Load an existing game
            db_service = DatabaseService()
            player_name = input("Enter your player name to load: ")
            player_data = db_service.get_player_data(player_name)
            if player_data:
                player = Player(player_data['player_name'], player_data['money'], player_data['fuel_points'], player_data['location'])
                break
            else:
                print("No player found with that name.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # Create the game instance with the database connection
    game = Game(db_service.connection)

    # Simulate playing 100 rounds
    for round_num in range(1, 101):
        print(f"Round {round_num}:")
        departure = input("Enter departure airport: ")
        arrival = input("Enter arrival airport: ")
        distance = game.calculate_distance(departure, arrival)

        if distance:
            print(f"Distance between {departure} and {arrival}: {distance:.2f} km")
            fuel_cost = distance * 0.1  # Example: 0.1 fuel per km
            if player.fuel >= fuel_cost:
                player.update_fuel(-fuel_cost)
                player.update_money(100)  # Earning money for the flight
                print(f"Flight completed. Remaining fuel: {player.fuel}")
            else:
                print("Not enough fuel for this flight.")
        else:
            print("Invalid airports or unable to calculate distance.")

        # Save progress after each round
        player.save_to_db(db_service.connection)

    print("Game over! Your final stats:")
    print(f"Name: {player.name}, Money: {player.money}, Fuel: {player.fuel}, Location: {player.location}")

# Ensure the main function is called to start the game
if __name__ == "__main__":
    main()
