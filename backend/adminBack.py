from repositories.client_repository import ClientRepository
from repositories.user_repository import UserRepository
from repositories.billing_repository import BillingRepository
from repositories.address_repository import AddressRepository
from repositories.category_repository import CategoryRepository
from repositories.meter_repository import MeterRepository
from repositories.reading_repository import ReadingRepository
from repositories.transaction_repository import TransactionRepository
from repositories.rateblock_repository import RateBlockRepository
import psycopg2
from datetime import datetime
from database.Database import DBConnector


class adminPageBack:
    def __init__(self, user_name="System"):
        self.user_name = user_name

    def log_action(self, message):
        try:
            db = DBConnector()
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO system_logs (message, user_name, timestamp)
                VALUES (%s, %s, %s)
            """, (message, self.user_name, datetime.now()))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Logging error: {e}")

    def fetch_clients(self):
        client_repository = ClientRepository()
        clients = client_repository.get_all_clients()
        self.log_action("Fetched all clients")
        return clients

    def fetch_users(self):
        user_repository = UserRepository()
        users = user_repository.get_all_employee()
        self.log_action("Fetched all users")
        return users

    def fetch_user_by_id(self, user_id):
        user_repository = UserRepository()
        user = user_repository.get_user_by_id(user_id)
        self.log_action(f"Fetched user by ID: {user_id}")
        return user

    def fetch_billing(self):
        billing_repository = BillingRepository()
        billing = billing_repository.get_all_billing()
        self.log_action("Fetched all billing records")
        return billing

    def add_billing(self, billing_due, billing_total, billing_consumption, reading_id, client_id, categ_id,
                    billing_date, billing_status, billing_amount, billing_sub_capital, billing_late_payment,
                    billing_penalty, billing_total_charge):
        billing_repository = BillingRepository()
        result = billing_repository.create_billing(billing_due, billing_total, billing_consumption, reading_id,
                                                   client_id, categ_id, billing_date, billing_status,
                                                   billing_amount, billing_sub_capital, billing_late_payment,
                                                   billing_penalty, billing_total_charge)
        self.log_action(f"Added billing for client ID: {client_id}")
        return result

    def fetch_client_by_id(self, client_id):
        client_repository = ClientRepository()
        client = client_repository.get_client_by_id(client_id)
        self.log_action(f"Fetched client by ID: {client_id}")
        return client

    def add_client(self, client_name, client_lname, client_contact_num, client_location, meter_id,
                   address_id, categ_id, client_mname, status):
        client_repository = ClientRepository()
        result = client_repository.create_client(client_name, client_lname, client_contact_num, client_location,
                                                 meter_id, address_id, categ_id, client_mname, status)
        self.log_action(f"Added new client: {client_name} {client_lname}")
        return result

    def fetch_categories(self):
        category_repository = CategoryRepository()
        categories = category_repository.get_category()
        self.log_action("Fetched all categories")
        return categories

    def get_category_by_id(self, id):
        category_repository = CategoryRepository()
        category = category_repository.get_category_by_id(id)
        self.log_action(f"Fetched category by ID: {id}")
        return category

    def toggle_category_status(self, id, status):
        category_repository = CategoryRepository()
        result = category_repository.toggle_status_category(id, status)
        self.log_action(f"Toggled category status: ID={id}, Status={status}")
        return result

    def fetch_address(self):
        address_repository = AddressRepository()
        address = address_repository.get_address()
        self.log_action("Fetched all addresses")
        return address

    def get_address_by_id(self, id):
        address_repository = AddressRepository()
        address = address_repository.get_address_by_id(id)
        self.log_action(f"Fetched address by ID: {id}")
        return address

    def toggle_address_status(self, id, status):
        address_repository = AddressRepository()
        result = address_repository.toggle_status(id, status)
        self.log_action(f"Toggled address status: ID={id}, Status={status}")
        return result

    def add_reading(self, read_date, prev_read, pres_read, meter_id):
        reading_repository = ReadingRepository()
        result = reading_repository.create_reading(read_date, prev_read, pres_read, meter_id)
        self.log_action(f"Added new reading for meter ID: {meter_id}")
        return result

    def add_meter(self, meter_last_reading, serial_number):
        meter_repository = MeterRepository()
        result = meter_repository.create_meter(meter_last_reading, serial_number)
        self.log_action(f"Added new meter: SN={serial_number}")
        return result

    def fetch_meter_by_id(self, meter_id):
        meter_repository = MeterRepository()
        meter = meter_repository.get_meter_by_id(meter_id)
        self.log_action(f"Fetched meter by ID: {meter_id}")
        return meter

    def update_meter_latest_reading(self, pres_read, read_date, meter_id):
        meter_repository = MeterRepository()
        result = meter_repository.update_meter(pres_read, read_date, meter_id)
        self.log_action(f"Updated latest reading for meter ID: {meter_id}")
        return result

    def fetch_rate_blocks_by_categ(self, categ_id):
        rateblock_repo = RateBlockRepository()
        blocks = rateblock_repo.get_rate_block_by_category(categ_id)
        self.log_action(f"Fetched rate blocks for category ID: {categ_id}")
        return blocks

    def fetch_transactions(self):
        transactions_repository = TransactionRepository()
        transactions = transactions_repository.get_all_transaction()
        self.log_action("Fetched all transactions")
        return transactions

    def update_client(self, client_id, fname, lname, contact, location, mname):
        client_repository = ClientRepository()
        result = client_repository.update_client(client_id, fname, lname, contact, location, mname)
        self.log_action(f"Updated client: ID={client_id}")
        return result

    def update_client_status(self, client_id, new_status):
        client_repository = ClientRepository()
        result = client_repository.update_client_status(client_id, new_status)
        self.log_action(f"Updated client status: ID={client_id}, Status={new_status}")
        return result

    def fetch_meters(self):
        meter_repository = MeterRepository()
        meters = meter_repository.get_all_meters()
        self.log_action("Fetched all meters")
        return meters

    def update_meter(self, meter_id, serial_number, meter_code, last_read):
        meter_repository = MeterRepository()
        result = meter_repository.update_meter(meter_id, serial_number, meter_code, last_read)
        self.log_action(f"Updated meter: ID={meter_id}")
        return result

    def get_meter_by_id(self, meter_id):
        meter_repository = MeterRepository()
        meter = meter_repository.get_meter_by_id(meter_id)
        self.log_action(f"Fetched meter by ID: {meter_id}")
        return meter

    def fetch_readings_by_meter_id(self, meter_id):
        reading_repository = MeterRepository()
        readings = reading_repository.get_readings_by_meter_id(meter_id)
        self.log_action(f"Fetched readings for meter ID: {meter_id}")
        return readings

    def fetch_transaction_logs(self):
        transaction_repo = TransactionRepository()
        logs = transaction_repo.get_all_transaction_logs()
        self.log_action("Fetched transaction logs")
        return logs

    def fetch_system_logs(self):
        transaction_repo = TransactionRepository()
        logs = transaction_repo.get_all_system_logs()
        self.log_action("Fetched system logs")
        return logs
