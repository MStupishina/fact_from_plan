from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class HistoryPredictions(Base):
    __tablename__ = "history_predictions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type_product: Mapped[str] = mapped_column(String(255), nullable=False)
    project: Mapped[str] = mapped_column(String(255), nullable=False)
    division_name: Mapped[str] = mapped_column(String(255), nullable=False)
    standart_name: Mapped[str] = mapped_column(String(255), nullable=False)
    doc_type_name: Mapped[str] = mapped_column(String(255), nullable=False)
    type_work_name: Mapped[str] = mapped_column(String(255), nullable=False)
    functional_name: Mapped[str] = mapped_column(String(255), nullable=False)
    type_doc_new: Mapped[str] = mapped_column(String(255), nullable=False)
    view_doc_new: Mapped[str] = mapped_column(String(255), nullable=False)
    operplan_labor: Mapped[float] = mapped_column(Float, nullable=False)
    standart_labor: Mapped[float] = mapped_column(Float, nullable=False)
    plan_labor: Mapped[float] = mapped_column(Float, nullable=False)
    cash: Mapped[float] = mapped_column(Float, nullable=False)
    fact_labor_true: Mapped[float] = mapped_column(Float, nullable=True)
    fact_labor_predict: Mapped[float] = mapped_column(Float, nullable=False)
    error: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
