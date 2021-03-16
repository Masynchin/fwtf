"""city_from param to User

Revision ID: 2e0cc5669ef4
Revises: 7b40e3f1b909
Create Date: 2021-03-13 00:43:52.333565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e0cc5669ef4'
down_revision = '7b40e3f1b909'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_jobs_category_id_job_category'), 'job_category', ['category_id'], ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_users_email'), ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_users_email'), type_='unique')

    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_jobs_category_id_job_category'), type_='foreignkey')

    # ### end Alembic commands ###