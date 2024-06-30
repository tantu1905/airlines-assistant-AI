from sqlalchemy import Column, Integer, String,ForeignKey,Text,Date,DateTime,Time
from sqlalchemy import JSON,ARRAY,Table,MetaData,delete
from sqlalchemy.orm import relationship
from .database import Base,engine
from sqlalchemy.ext.declarative import declared_attr



class QuestionAnswer(Base):
    
    __tablename__ = "question_answer"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String , nullable=False)
    
    
models = {}

class Import(Base):
    __tablename__ = "flight"
    id = Column(Integer, primary_key=True, index=True)
    departure = Column(String, nullable=False)
    arrival = Column(String, nullable=False)
    dep_airport = Column(String, nullable=False)
    arr_airport = Column(String, nullable=False)
    # dep_date_time = Column(DateTime, nullable=False)
    dep_date_time_date = Column(Date, nullable=False)
    dep_date_time_hour = Column(Time, nullable=False)
    flight_number = Column(String, nullable=False)
    
    #eklenecekler aşağıda
    #bunları ekleyip bilet oluştururlduğunda azaltma ve arttırma işlemleri yapılacak.
    #capacity = Column(Integer, nullable=False)
    #empty_seats = Column(Integer, nullable=False)
    
    # sonradan bakılacaklar aşağıda

    
    # tickets = relationship("Ticket", back_populates="flights")
    
    
    
class Ticket(Base):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) #change passport number
    flight_number = Column(String, nullable=False)
    seat_number = Column(String, nullable=False)
    pnr_code = Column(String, nullable=False)
    dep_date_time_date = Column(Date, nullable=False)
    # dep_date_time_hour = Column(Time, nullable=False)
    
    # sonradan bakılacak
    

    
    # flights = relationship("Import", back_populates="tickets")
    

# def get_table_name(location, destination):
#     table_name = f'{location}_{destination}'
#     # meta = MetaData()
#     # table_to_drop = Table(table_name, meta).drop(engine,checkfirst=True)
#     # Base.metadata.create_all(bind=engine)
#     # Base.metadata.drop_all(bind=engine)
#     # Table(f'{location}_{destination}', Base.metadata.drop(engine))

#     if table_name not in models:
#         class Import(Base):
#             __tablename__ = table_name
#             id = Column(Integer, primary_key=True, index=True)
#             departure = Column(String, nullable=False)
#             arrival = Column(String, nullable=False)
#             dep_airport = Column(String, nullable=False)
#             arr_airport = Column(String, nullable=False)
#             # dep_date_time = Column(DateTime, nullable=False)
#             dep_date_time_date = Column(Date, nullable=False)
#             dep_date_time_hour = Column(Time, nullable=False)
#             flight_number = Column(String, nullable=False)
            
            
#         models[table_name] = Import
#             #data = Column(JSON, nullable=False)
#     # delete_stmt = delete(models[table_name])
#     # engine.execute(delete_stmt)
#         Base.metadata.create_all(bind=engine)
        

#     return models[table_name]
    
    #Base.metadata.drop_all(bind=engine)
    
    #question_id = Column(Integer, ForeignKey("question_answer.id"))
    #question = relationship("QuestionAnswer", back_populates="import_data")
    

# Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

    
    

