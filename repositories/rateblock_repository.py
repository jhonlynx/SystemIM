import psycopg2
from database.Database import DBConnector

class RateBlockRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_rate_block(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM RATEBLOCK;")
        rateblock = cursor.fetchall()
        cursor.close()
        conn.close()
        return rateblock
    
    def get_reading_by_id(self, reading_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM METER WHERE READING_ID = %s;",
            (reading_id,)
        )
        reading = cursor.fetchall()
        cursor.close()
        conn.close()
        return reading
    

    def create_reading(self, read_date, prev_read, pres_read, meter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO READING (READING_DATE, READING_PREV, READING_CURRENT, METER_ID)
            VALUES (%s, %s, %s, %s)
            RETURNING READING_ID;
        """, (read_date, prev_read, pres_read, meter_id))
        new_reading_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return new_reading_id

