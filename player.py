class Player:
    def __init__(self, name, money=600, fuel=0, location='unknown'):
        self.name = name
        self.money = money
        self.fuel = fuel
        self.location = location

    def update_money(self, amount):
        self.money += amount

    def update_fuel(self, points):
        self.fuel += points

    def save_to_db(self, db_connection):

        sql = """
        INSERT INTO player (player_name, money, fuel_points, location)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE money = %s, fuel_points = %s, location = %s
        """
        cursor = db_connection.cursor()
        cursor.execute(sql, (self.name, self.money, self.fuel, self.location, self.money, self.fuel, self.location))
        db_connection.commit()

    def load_from_db(self, db_connection):

        sql = f"SELECT * FROM player WHERE player_name = '{self.name}'"
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            self.money = result['money']
            self.fuel = result['fuel_points']
            self.location = result['location']
        else:
            print("Player data not found.")
