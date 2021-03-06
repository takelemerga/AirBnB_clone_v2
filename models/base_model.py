#!/usr/bin/python3
'''
    This module defines the BaseModel class
'''
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    '''
        Base class for other classes to be used for the duration.
    '''
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        '''
            Initialize public instance attributes.
        '''
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            from models import storage
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
                    
            if kwargs.get("created_at") is not None:
                setattr(self, 'created_at', datetime.strptime(
                                  kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f'))
            else:
                self.created_at = datetime.now()
            if kwargs.get("updated_at") is not None:
                setattr(self, 'updated_at', datetime.strptime(
                                  kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f'))
            else:
                self.updated_at = datetime.now()
            if kwargs.get("id") is not None:
                setattr(self, 'id', kwargs["id"])
            else:
                self.id = str(uuid.uuid4())        
            storage.new(self)
    def __str__(self):
        '''
            Return string representation of BaseModel class
        '''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def __repr__(self):
        '''
            Return string representation of BaseModel class
        '''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        '''
            Update the updated_at attribute with new.
        '''
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        '''
            Return dictionary representation of BaseModel class.
        '''
        cp_dct = dict(self.__dict__)
        cp_dct['__class__'] = self.__class__.__name__
        cp_dct['updated_at'] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        cp_dct['created_at'] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        if '_sa_instance_state' in cp_dct:
            del cp_dct['_sa_instance_state']
        return cp_dct

    def delete(self):
        models.storage.delete(self)
