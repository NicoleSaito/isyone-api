from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./isyone.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ScriptModel(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    filename = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    parameters = Column(Text, nullable=True)   # ex: "client_id, client_name"
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class LogModel(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    script_name = Column(String(100), nullable=False)
    parameters = Column(Text, nullable=True)
    status = Column(String(20), nullable=False)   # success | error
    output = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    executed_at = Column(DateTime, default=datetime.utcnow)


class TokenModel(Base):
    __tablename__ = "api_token"

    id = Column(Integer, primary_key=True)
    token = Column(String(200), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Token padrão se não existir
        if not db.query(TokenModel).first():
            db.add(TokenModel(token="544c5787-613a-4ac2-8e61-9e6486f8d74a"))
            db.commit()

        # Scripts de exemplo se não existirem
        if not db.query(ScriptModel).first():
            exemplos = [
                ScriptModel(
                    name="provision_client",
                    filename="provision_client.sh",
                    description="Provisiona ambiente para um novo cliente",
                    parameters="client_id, client_name",
                    active=True,
                ),
                ScriptModel(
                    name="deprovision_client",
                    filename="deprovision_client.sh",
                    description="Remove ambiente de um cliente",
                    parameters="client_id",
                    active=True,
                ),
                ScriptModel(
                    name="check_service",
                    filename="check_service.sh",
                    description="Verifica status de um serviço systemd",
                    parameters="service_name",
                    active=True,
                ),
                ScriptModel(
                    name="cleanup_logs",
                    filename="cleanup_logs.sh",
                    description="Remove logs antigos do servidor",
                    parameters="days",
                    active=True,
                ),
            ]
            db.add_all(exemplos)
            db.commit()
    finally:
        db.close()
