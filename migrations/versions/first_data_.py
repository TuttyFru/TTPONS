"""empty message

Revision ID: first_data
Revises: 1ab28272caaa
Create Date: 2022-12-11 16:34:06.626121

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm

from src.models import Overall, Workshop, Worker, Reciving


# revision identifiers, used by Alembic.
revision = 'first_data'
down_revision = '1ab28272caaa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    kitchen = Workshop(
        name="Kitchen",
        full_name="Petrov Petr Petrovich")
    sewing = Workshop(
        name="sewing factory",
        full_name="Antonova Karolina Malorovna")

    session.add_all([kitchen, sewing])
    session.flush()

    ivanov = Worker(
        full_name="Ivanov Ivan Ivanovich",
        job_title="cook",
        discount=30,
        job_id=kitchen.id)
    noskov = Worker(
        full_name="Noskov Arsen Artyomovich",
        job_title="weaver",
        discount=30,
        job_id=sewing.id)

    session.add_all([ivanov, noskov])
    session.flush()

    apron = Overall(
        kind="Food industry",
        wear_time=6,
        cost=3000)
    slippers = Overall(
        kind="Other",
        wear_time=12,
        cost=400)

    session.add_all([apron, slippers])
    session.flush()

    reciving1 = Reciving(
        date="10.03.2022",
        signature="Iva",
        worker_id=ivanov.id,
        overall_id=apron.id)
    reciving2 = Reciving(
        date="04.09.2022",
        signature="Nos",
        worker_id=noskov.id,
        overall_id=slippers.id
        )
    
    session.add_all([reciving1, reciving2])
    session.commit()


def downgrade() -> None:
    pass
