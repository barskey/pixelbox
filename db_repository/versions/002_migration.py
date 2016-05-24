from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
pixel = Table('pixel', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('img_id', Integer),
    Column('row', Integer),
    Column('col', Integer),
    Column('hexvalue', String(length=6)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['pixel'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['pixel'].drop()
