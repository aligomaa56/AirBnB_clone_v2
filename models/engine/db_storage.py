#!/usr/bin/python3
"""db_storge class"""
from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.place import Place, place_amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.review import Review
from models.city import City
from models.user import User


__objs = {"State": State, "Amenity": Amenity,
             "City": City, "Place": Place,
             "Review": Review, "User": User}

class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Instatntiates a new model"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(getenv('HBNB_MYSQL_USER'),
                                                 getenv('HBNB_MYSQL_PWD'),
                                                 getenv('HBNB_MYSQL_HOST'),
                                                 getenv('HBNB_MYSQL_DB')),
                                                pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """all method"""
        _dict = {}
        if cls is None:
            for obj in __objs.values():
                objs = self.__session.query(obj).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    _dict[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                _dict[key] = obj
        return _dict

    def new(self, obj):
        """add the object to the current database"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        self.__session.delete(obj)

    def reload(self):
        """relod from db"""
        from models.user import User
        from models.state import State
        from models.place import Place
        from models.review import Review
        from models.base_model import BaseModel, Base
        from models.city import City
        from models.amenity import Amenity
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = Session()

    def close(self):
        """Close session."""
        self.__session.close()
