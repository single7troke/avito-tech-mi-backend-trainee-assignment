from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class AvitoSearch(Base):
    __tablename__ = "avitosearch"

    id = Column(Integer, primary_key=True, index=True)
    search_phrase = Column(String, index=True)
    region = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    location_id = Column(Integer, ForeignKey("location.locationId"))

    items = relationship("Statistics", back_populates="owner")
    topfiveitems = relationship("TopFive", back_populates="owner")
    owner = relationship("Location", back_populates="childe")


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    region_name = Column(String, unique=True, index=True)
    locationId = Column(Integer, unique=True, index=True)

    childe = relationship("AvitoSearch", back_populates="owner")


class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("avitosearch.id"))

    owner = relationship("AvitoSearch", back_populates="items")

class TopFive(Base):
    __tablename__ = "topfive"

    id = Column(Integer, primary_key=True, index=True)
    topfive = Column(ARRAY(Integer))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("avitosearch.id"))

    owner = relationship("AvitoSearch", back_populates="topfiveitems")
