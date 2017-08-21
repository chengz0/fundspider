# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from models import db_connect, create_table, AddFundItem, AddHoldingStackItem
from sqlalchemy.orm import sessionmaker
from items import FundspiderItem, HoldingStackItem

class FundspiderPipeline(object):

    def __init__(self):
        engine =  db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        session = self.Session()
        if isinstance(item, FundspiderItem):
            data = AddFundItem(**item)
        elif isinstance(item, HoldingStackItem):
            data = AddHoldingStackItem(**item)

        try:
            session.add(data)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item