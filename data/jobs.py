import sqlalchemy
from .database_session import SqlAlchemyBase
from sqlalchemy import orm


class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    collaboration = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
    user = orm.relation('User')

    def __repr__(self):
        return " ".join([self.team_leader, self.job, self.work_size,
                         self.collaboration, self.is_finished])

