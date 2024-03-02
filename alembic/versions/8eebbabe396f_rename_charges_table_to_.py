"""Rename charges table to NonstandardizedCharges

Revision ID: 8eebbabe396f
Revises: 0d23c3645d33
Create Date: 2023-12-19 16:08:45.104558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8eebbabe396f'
down_revision: Union[str, None] = '0d23c3645d33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charges',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('charge_description', sa.String(), nullable=True),
    sa.Column('charge_class', sa.String(), nullable=True),
    sa.Column('degree', sa.String(), nullable=True),
    sa.Column('incident_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['incident_id'], ['public.incidents.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('charge_description', 'charge_class', 'degree', name='unique_charge_combination'),
    schema='public'
    )
    op.drop_constraint('PersonAddress_PersonID_fkey', 'PersonAddress', type_='foreignkey')
    op.drop_constraint('PersonAddress_AddressID_fkey', 'PersonAddress', type_='foreignkey')
    op.create_foreign_key(None, 'PersonAddress', 'addresses', ['AddressID'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'PersonAddress', 'persons', ['PersonID'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('incident_persons_person_id_fkey', 'incident_persons', type_='foreignkey')
    op.drop_constraint('incident_persons_incident_id_fkey', 'incident_persons', type_='foreignkey')
    op.create_foreign_key(None, 'incident_persons', 'persons', ['person_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'incident_persons', 'incidents', ['incident_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('incidents_article_id_fkey', 'incidents', type_='foreignkey')
    op.create_foreign_key(None, 'incidents', 'article', ['article_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('incidents_from_pdf_accused_person_id_fkey', 'incidents_from_pdf', type_='foreignkey')
    op.create_foreign_key(None, 'incidents_from_pdf', 'persons', ['accused_person_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('incidents_with_errors_article_id_fkey', 'incidents_with_errors', type_='foreignkey')
    op.create_foreign_key(None, 'incidents_with_errors', 'article', ['article_id'], ['id'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'incidents_with_errors', schema='public', type_='foreignkey')
    op.create_foreign_key('incidents_with_errors_article_id_fkey', 'incidents_with_errors', 'article', ['article_id'], ['id'])
    op.drop_constraint(None, 'incidents_from_pdf', schema='public', type_='foreignkey')
    op.create_foreign_key('incidents_from_pdf_accused_person_id_fkey', 'incidents_from_pdf', 'persons', ['accused_person_id'], ['id'])
    op.drop_constraint(None, 'incidents', schema='public', type_='foreignkey')
    op.create_foreign_key('incidents_article_id_fkey', 'incidents', 'article', ['article_id'], ['id'])
    op.drop_constraint(None, 'incident_persons', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'incident_persons', schema='public', type_='foreignkey')
    op.create_foreign_key('incident_persons_incident_id_fkey', 'incident_persons', 'incidents', ['incident_id'], ['id'])
    op.create_foreign_key('incident_persons_person_id_fkey', 'incident_persons', 'persons', ['person_id'], ['id'])
    op.drop_constraint(None, 'PersonAddress', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'PersonAddress', schema='public', type_='foreignkey')
    op.create_foreign_key('PersonAddress_AddressID_fkey', 'PersonAddress', 'addresses', ['AddressID'], ['id'])
    op.create_foreign_key('PersonAddress_PersonID_fkey', 'PersonAddress', 'persons', ['PersonID'], ['id'])
    op.drop_table('charges', schema='public')
    # ### end Alembic commands ###