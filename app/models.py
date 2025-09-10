from datetime import date, time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, Float, ForeignKey, String, Table, Column, Integer
from datetime import datetime

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class = Base)


class Customers(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))

    service_tickets: Mapped[list['ServiceTickets']] = relationship('ServiceTickets', back_populates='customer')


class Mechanics(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    salary: Mapped[float] = mapped_column(Float)
    address: Mapped[str] = mapped_column(String(255))

    service_mechanics: Mapped[list['ServiceMechanics']] = relationship('ServiceMechanics', back_populates='mechanic')


class ServiceTickets(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    service_desc: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    car_VIM: Mapped[str] = mapped_column(String(255), nullable=False)
    service_date: Mapped[date] = mapped_column(Date,default=datetime.now())
    
    customer: Mapped['Customers'] = relationship('Customers', back_populates='service_tickets')
    service_mechanics: Mapped[list['ServiceMechanics']] = relationship('ServiceMechanics', back_populates='ticket')
    ticket_inventory: Mapped[list['TicketInventory']] = relationship('TicketInventory', back_populates='ticket')


class ServiceMechanics(Base):
    __tablename__ = 'service_mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey('service_tickets.id', ondelete='CASCADE'))
    mechanic_id: Mapped[int] = mapped_column(ForeignKey('mechanics.id', ondelete='CASCADE'))

    mechanic: Mapped['Mechanics'] = relationship('Mechanics', back_populates='service_mechanics')
    ticket: Mapped['ServiceTickets'] = relationship('ServiceTickets', back_populates='service_mechanics')
    
#-----
class TicketInventory(Base):
    __tablename__ = 'ticket_inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    inventory_id: Mapped[int] = mapped_column(ForeignKey('inventory.id', ondelete='CASCADE'))
    ticket_id: Mapped[int] = mapped_column(ForeignKey('service_tickets.id', ondelete='CASCADE'))

    inventory: Mapped['Inventory'] = relationship('Inventory', back_populates='ticket_inventory')
    ticket: Mapped['ServiceTickets'] = relationship('ServiceTickets', back_populates='ticket_inventory')
    
    
class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)

    ticket_inventory: Mapped[list['TicketInventory']] = relationship('TicketInventory', back_populates='inventory')