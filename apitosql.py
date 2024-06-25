from databases.database import SessionLocal,engine,Base
from thyfs import get_fly_info_thyapi
from databases.models import Import
import json
from datetime import datetime
from databases.models import Import

def test():
    db = SessionLocal()
    array1 = ["IST","SAW"]
    iata_codes = [
    "LON",  # Londra
    "PAR",  # Paris
    "AMS",  # Amsterdam
    "BER",  # Berlin
    "STR",  # Stuttgart
    "MUC",  # München
    "MRS",  # Marsilya
    "PRG",  # Prag
    "MOW",  # Moskova
    "LED",  # St.Petersburg
    "DXB",  # Dubai
    "SIN",  # Singapur
    "SYD",  # Sydney
    "TYO",  # Tokyo
    "KIX",  # Osaka
    "SEL",  # Seoul
    "TZX",  # Trabzon
    "MLX",  # Malatya
    "ESB",  # Ankara
    "ADB",  # Izmir
    "AYT",  # Antalya
    "ADA",  # Adana
    "DIY",  # Diyarbakır
    "KSY",  # Kars
    "MSR",  # Muş
    "GRZ",  # Graz
    "WAW",  # Varşova
    "ATH",  # Atina
    "GYD",  # Bakü
    "FCO",  # Roma
    "MXP",  # Milano
    "MAD",  # Madrid
    "BCN",  # Barcelona
    "ZRH",  # Zürih
    "BRU",   # Brüksel
    "KYA",  # Konya
    "OGU",  # Ordu-Giresun
    "GZT",  # Gaziantep
    "ASR",  # Kayseri
    ]

    # for i in iata_codes:
        
    db.query(Import).delete()
    db.commit()
    print (f'deleted')
        # try:
        #     json_data = get_fly_info_thyapi("IST", i)
        #     data3 = json.dumps(json_data)
        #     data4 = json.loads(data3)
        #     for k in json_data:
        #         # json_import = get_table_name(k["departure_loc"], k["arrival_loc"])
        #         # Tabloyu temizle
        #         db.query(json_import).delete()
        #         db.commit()
        #         print (f'IST and {k["arrival_loc"]} deleted')
        #         break  # Tabloyu bir kez temizledikten sonra döngüden çık
        # except AttributeError:
        #     print(f'IST and {i} not found')
    for i in iata_codes:
        try:
            json_data = get_fly_info_thyapi("IST",i)
        #json['departure_date_time_date'] = json['departure_date_time_date'].isoformat()
            data3 = json.dumps(json_data)
            data4 = json.loads(data3)
            # db.query(json_import).delete()
            # db.commit()
            for k in json_data:
                # meta = MetaData()
                # table_to_drop = Table(f'IST_{i}', meta).drop(engine,checkfirst=True)
                # tablename = f'IST_{k["arrival_loc"]}'
                # json_import = get_table_name(k["departure_loc"],k["arrival_loc"])

                
            # json_import = Import(departure=json_data[0]["departure_loc"],arrival=json_data[0]["arrival_loc"],data=data4).__init__(json_data[0]["departure_loc"],json_data[0]["arrival_loc"])
                dep_date_time = datetime.fromisoformat(k["departure_date_time"].replace("Z", "+00:00"))
                dep_date_time_date = dep_date_time.date()
                dep_date_time_hour = dep_date_time.time()
                import_instance = Import(departure=k["departure_loc"],arrival=k["arrival_loc"],dep_airport=k["departure_airport"],arr_airport=k["arrival_airport"],dep_date_time_date=dep_date_time_date,dep_date_time_hour=dep_date_time_hour,flight_number=k["flight_number"])
                db.add(import_instance)
                print (f'added IST and {k["arrival_loc"]}')
                db.commit()
                db.refresh(import_instance)

                # Base.metadata.create_all(bind=engine)
            
        except AttributeError:
            print (f'not found')
            
    print ("test")
    Base.metadata.create_all(bind=engine)   