from databases.database import SessionLocal, engine, Base
from thyfs import get_fly_info_thyapi
from databases.models import Import,Ticket,QuestionAnswer
import json
from datetime import datetime

def test():
    db = SessionLocal()
    try:
        array1 = ["IST", "SAW"]
        iata_codes = [
            "LON", "PAR", "AMS", "BER", "STR", "MUC", "MRS", "PRG", "MOW", "LED", 
            "DXB", "SIN", "SYD", "TYO", "KIX", "SEL", "TZX", "MLX", "ESB", "ADB", 
            "AYT", "ADA", "DIY", "KSY", "MSR", "GRZ", "WAW", "ATH", "GYD", "FCO", 
            "MXP", "MAD", "BCN", "ZRH", "BRU", "KYA", "OGU", "GZT", "ASR"
        ]

        # Clear the Import table
        db.query(Import).delete()
        db.commit()
        print('Deleted all records from Import table')

        # Fetch flight info and insert into the database
        for i in iata_codes:
            try:
                json_data = get_fly_info_thyapi("IST", i)
                for k in json_data:
                    dep_date_time = datetime.fromisoformat(k["departure_date_time"].replace("Z", "+00:00"))
                    dep_date_time_date = dep_date_time.date()
                    dep_date_time_hour = dep_date_time.time()
                    import_instance = Import(
                        departure=k["departure_loc"],
                        arrival=k["arrival_loc"],
                        dep_airport=k["departure_airport"],
                        arr_airport=k["arrival_airport"],
                        dep_date_time_date=dep_date_time_date,
                        dep_date_time_hour=dep_date_time_hour,
                        flight_number=k["flight_number"]
                    )
                    db.add(import_instance)
                    print(f'Added flight from IST to {k["arrival_loc"]}')
                    db.commit()
                    db.refresh(import_instance)
            except AttributeError as e:
                print(f'Error processing flights from IST to {i}: {e}')
            except Exception as e:
                print(f'Unexpected error: {e}')

        print("Test completed")
        Base.metadata.create_all(bind=engine)
    finally:
        db.close()

# Run the test function


# def capacity_control():
#     db = SessionLocal()
    
#     query = db.query(Ticket)

def reset_qa():
    db = SessionLocal()
    try:
        db.query(QuestionAnswer).delete()
        db.commit()
        print('Deleted all records from QA table')
    finally:
        db.close()