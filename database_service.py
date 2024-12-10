from database_connection import create_db_connection  # Import the function here

class DatabaseService:
    def __init__(self):
        self.connection = create_db_connection()  # Use the imported function to create the connection

    def execute_query(self, query, fetch_one=False):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        if fetch_one:
            return cursor.fetchone()
        return cursor.fetchall()

    def execute_non_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def get_player_data(self, player_name):
        sql = f"SELECT * FROM player WHERE player_name = '{player_name}'"
        return self.execute_query(sql, fetch_one=True)

    def get_goods(self, airport_name):

        sql = f"""
        SELECT g.name, g.price, g.weight, g.value
        FROM goods g
        JOIN goods_in_country gc ON g.goods_id = gc.goods_id
        JOIN airport a ON gc.iso_country = a.iso_country
        WHERE a.name = '{airport_name}'
        """
        return self.execute_query(sql)

    def get_missions(self, player_level):

        sql = f"SELECT * FROM missions WHERE level_required <= {player_level}"
        return self.execute_query(sql)

    def update_player_data(self, player):
        sql = f"""
        UPDATE player
        SET money = {player.money}, fuel_points = {player.fuel}, location = '{player.location}'
        WHERE player_name = '{player.name}'
        """
        self.execute_non_query(sql)
