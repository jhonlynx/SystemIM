import psycopg2
from database.Database import DBConnector

class MeterRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_all_meters(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT m.METER_ID, m.SERIAL_NUMBER, m.METER_CODE, 
                    m.METER_LAST_READING_DATE, c.CLIENT_NAME, c.CLIENT_LNAME
                FROM METER m
                LEFT JOIN CLIENT c ON c.METER_ID = m.METER_ID
                ORDER BY m.METER_ID ASC
            """)

            meters = cursor.fetchall()

            formatted_meters = [
                (meter_code, f"{client_name} {client_lname}" if client_name and client_lname else "N/A",
                serial_number, last_read, meter_id)
                for (meter_id, serial_number, meter_code, last_read, client_name, client_lname) in meters
            ]

            return formatted_meters

        except Exception as e:
            print(f"Database error: {e}")
            return []

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    

    def create_meter(self, meter_last_reading, serial_number):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO METER (
                METER_LAST_READING, METER_LAST_READING_DATE, METER_CODE, SERIAL_NUMBER
            ) VALUES (
                %s, CURRENT_DATE,
                'MTR-' || LPAD(nextval('meter_code_alphanumeric')::text, 5, '0'), %s
            )
            RETURNING METER_ID;
        """, (
            meter_last_reading, serial_number
        ))
        new_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_id

    def update_meter_latest_reading(self, pres_read, read_date, meter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE METER
                       SET METER_LAST_READING      = %s,
                           METER_LAST_READING_DATE = %s
                       WHERE METER_ID = %s
                       """, (pres_read, read_date, meter_id))
        conn.commit()
        cursor.close()
        conn.close()
    
    def update_meter(self, meter_id, serial_number, meter_code, last_read):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE meter 
                SET serial_number = %s, 
                    meter_code = %s, 
                    meter_last_read = %s  
                WHERE meter_id = %s
            """, (
                serial_number, 
                meter_code, 
                last_read, 
                meter_id
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_readings_by_meter_id(self, meter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM READING WHERE METER_ID = %s ORDER BY READING_DATE DESC", (meter_id,))
        readings = cursor.fetchall()
        cursor.close()
        conn.close()
        return readings        
