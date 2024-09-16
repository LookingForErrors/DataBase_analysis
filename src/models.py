import datetime
from typing import Annotated
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, text, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256
import enum


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.now(datetime.timezone.utc))]



class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str] 

    resumes: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
    )

    resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')",
        order_by="ResumesOrm.id.desc()",

    )

class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"

class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int] = mapped_column(nullable=True)
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at] 
    updated_at: Mapped[updated_at] 
    
    worker: Mapped["WorkersOrm"] = relationship(
        back_populates="resumes",
    )

    # Вывод первых 4х столбцов + столбец created_at
    repr_cols_num = 4
    repr_cols = ("created_at", )

    __table_args__ = (
        Index("title_index", "title"),
        CheckConstraint("compensation > 0", name="check_compensation_positive")
    )










metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

