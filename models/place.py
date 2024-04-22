#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table(
            "place_amenity",
            Base.metadata,
            Column("place_id", String(60), ForeignKey("places.id"),
                   primary_key=True, nullable=False),
            Column("amenity_id", String(60), ForeignKey("amenities.id"),
                   primary_key=True, nullable=False),
            mysql_charset="latin1"
            )


class Place(BaseModel, Base):
    """ A place to stay """
    import models
    __tablename__ = "places"
    __table_args__ = ({'mysql_default_charset': 'latin1'})

    if getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", cascade="all, delete",
                               backref="place")
        amenities = relationship("Amenity",
                                 secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def amenities(self):
            """Getter for amenities"""
            all_amenities = models.storage.all(Amenity)
            place_amenities = []
            for am_id in amenity_ids:
                key = "Amenity." + am_id
                place_amenities.append(all_amenities[key])

            return place_amenities

        @amenities.setter
        def amenities(self, obj):
            """Setter for amenities."""
            if type(obj) is Amenity:
                amenity_ids.append(obj.id)
