class Airport:
    @staticmethod
    def get_location(db_connection, airport_name):
        sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE name = '{airport_name}'"
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            latitude = result['latitude_deg']
            longitude = result['longitude_deg']
            return (latitude, longitude)
        return None

    @staticmethod
    def get_goods(db_connection, airport_name):


        sql = f"""
        SELECT g.name, g.price, g.weight, g.value
        FROM goods g
        JOIN goods_in_country gc ON g.goods_id = gc.goods_id
        JOIN airport a ON gc.iso_country = a.iso_country
        WHERE a.name = '{airport_name}'
        """
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()
