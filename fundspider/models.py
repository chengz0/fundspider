# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import fundspider.settings

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**fundspider.settings.DATABASE))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class AddFundItem(DeclarativeBase):
    __tablename__ = "fund_test"

    id = Column(Integer, primary_key=True)
    ts = Column('ts', DateTime, nullable=True)
    index = Column('index', Integer, nullable=False)
    code = Column('code', String, nullable=False)
    name = Column('name', String, nullable=True)
    type = Column('type', Integer, nullable=True)
    value = Column('value', Float, nullable=True)
    value_sum = Column('value_sum', Float, nullable=True)
    day_rate = Column('day_rate', Float, nullable=True)
    week_rate = Column('week_rate', Float, nullable=True)
    month_rate = Column('month_rate', Float, nullable=True)
    season_rate = Column('season_rate', Float, nullable=True)
    half_year_rate = Column('half_year_rate', Float, nullable=True)
    year_rate = Column('year_rate', Float, nullable=True)


'''
    index = scrapy.Field()
    fund_code = scrapy.Field()
    stack_code = scrapy.Field()
    name = scrapy.Field()
    count = scrapy.Field()
    value = scrapy.Field()
    ratio = scrapy.Field()
'''
class AddHoldingStackItem(DeclarativeBase):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True)
    index = Column('index', Integer, nullable=False)
    fund_code = Column('fund_code', String, nullable=False)
    stack_code = Column('stack_code', String, nullable=False)
    name = Column('name', String, nullable=True)
    count = Column('count', Integer, nullable=True)
    value = Column('value', Float, nullable=True)
    ratio = Column('ratio', Float, nullable=True)
