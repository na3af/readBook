import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))



class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

# We added this serialize function to be able to send JSON objects in a
# serializable format

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class CategoryItem(Base):
    __tablename__ = 'category_item'

    id = Column(Integer, primary_key = True)
    title = Column(String(80), nullable = False)
    description = Column(String(250))
    categoryId = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)
    picture = Column(String(250))
    author = Column(String(80), nullable = False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

# We added this serialize function to be able to send JSON objects in a
# serializable format

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'cat_id': self.categoryId,
            'author': self.author,
        }

engine = create_engine('sqlite:////var/www/FlaskApp/FlaskApp/readBook/catalog.db')
Base.metadata.create_all(engine)
