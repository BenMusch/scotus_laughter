from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
transcript = Table('transcript', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String(length=256)),
    Column('docket_num', String(length=10)),
    Column('question_num', Integer, default=ColumnDefault(1)),
    Column('processed', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['transcript'].columns['processed'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['transcript'].columns['processed'].drop()
