from repositories.client_repository import ClientRepository
from repositories.user_repository import UserRepository
from repositories.billing_repository import BillingRepository
from repositories.address_repository import AddressRepository
from repositories.category_repository import CategoryRepository
from repositories.meter_repository import MeterRepository
from repositories.reading_repository import ReadingRepository
from repositories.transaction_repository import TransactionRepository



class adminPageBack:
    def fetch_clients(self):
        client_repository = ClientRepository()
        return client_repository.get_all_clients()

    def fetch_users(self):
        user_repository = UserRepository()
        return user_repository.get_all_employee()
    
    def fetch_user_by_id(self, user_id):
        user_repository = UserRepository()
        return user_repository.get_user_by_id(user_id)
    
    def fetch_billing(self):
        billing_repository = BillingRepository()
        return billing_repository.get_all_billing()
    
    def add_billing(self, billing_due, 
                       billing_total, 
                       billing_consumption, 
                       reading_id, 
                       client_id, 
                       categ_id, 
                       billing_date,  
                       billing_status, 
                       billing_amount, 
                       billing_sub_capital,
                       billing_late_payment, 
                       billing_penalty, 
                       billing_total_charge):
        billing_repository = BillingRepository()
        return billing_repository.create_billing( 
                       billing_due, 
                       billing_total, 
                       billing_consumption, 
                       reading_id, 
                       client_id, 
                       categ_id, 
                       billing_date,  
                       billing_status, 
                       billing_amount, 
                       billing_sub_capital,
                       billing_late_payment, 
                       billing_penalty, 
                       billing_total_charge)#adjusta ang imo billing repo kay ang akong gipasa dictionary nalang 
                                                             #or if mas dalian ka usba ang akoa bungkaga and dictionary ig pasa(taas na kaayong code)
    

    def fetch_client_by_id(self, client_id):
        client_repository = ClientRepository()
        return client_repository.get_client_by_id(client_id)
    
    def add_client(self, client_name, client_lname, client_contact_num, client_location, meter_id, address_id, categ_id, client_mname, status):
        client_repository = ClientRepository()
        return client_repository.create_client(client_name, client_lname, client_contact_num, client_location, meter_id, address_id, categ_id, client_mname, status)


    def fetch_categories(self):
        category_repository = CategoryRepository()
        return category_repository.get_category()
    
    def get_category_by_id(self, id):
        category_repository = CategoryRepository()
        return category_repository.get_category_by_id(id)
    
    def toggle_category_status(self, id, status):
        category_repository = CategoryRepository()
        return category_repository.toggle_status_category(id, status)
    
    def fetch_address(self):
        address_repository = AddressRepository()
        return address_repository.get_address()
    
    def get_address_by_id(self, id):
        address_repository = AddressRepository()
        return address_repository.get_address_by_id(id)
    
    def toggle_address_status(self, id, status):
        address_repository = AddressRepository()
        return address_repository.toggle_status(id, status)
    
    def add_reading(self, read_date, prev_read, pres_read, meter_id):
        reading_repository = ReadingRepository()
        return reading_repository.create_reading(read_date, prev_read, pres_read, meter_id)
    
    #meters
    def add_meter(self, meter_last_reading, serial_number):
        meter_repository = MeterRepository()
        return meter_repository.create_meter(meter_last_reading, serial_number)
    
    def fetch_meter_by_id(self, meter_id):
        meter_repository = MeterRepository()
        return meter_repository.get_meter_by_id(meter_id)
    
    def update_meter_latest_reading(self, pres_read, read_date, meter_id):
        meter_repository = MeterRepository()
        return meter_repository.update_meter(pres_read, read_date, meter_id)
    
    def fetch_rate_blocks_by_categ(self, categ_id):
        #butngi lang pd logic ari than base lang sa taas para testing
        return #aa
    
    def fetch_transactions(self):
        transactions_repository = TransactionRepository()
        return transactions_repository.get_all_transaction()
    
    def update_client(self, client_id, fname, lname, contact, location, mname):
        client_repository = ClientRepository()
        return client_repository.update_client(client_id, fname, lname, contact, location, mname)
    
    def update_client_status(self, client_id, new_status):
        client_repository = ClientRepository()
        return client_repository.update_client_status(client_id, new_status)
    
    def fetch_meters(self):
        meter_repository = MeterRepository()
        return meter_repository.get_all_meters()
    
    def update_meter(self, meter_id, serial_number, meter_code, last_read):
        meter_repository = MeterRepository()
        return meter_repository.update_meter(meter_id, serial_number, meter_code, last_read)
    
    def get_meter_by_id(self, meter_id):
        meter_repository = MeterRepository()
        return meter_repository.get_meter_by_id(meter_id)