from sqlalchemy.orm import Mapped, mapped_column, declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Banco(Base):
    __tablename__ = 'banco'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    email: Mapped[str]
    idade: Mapped[int]
    senha: Mapped[str]


class Cliente(Base):
    __tablename__ = 'cliente'
    id: Mapped[int] = mapped_column(primary_key=True)
    id_conta: Mapped[int]
    valor: Mapped[float]
    tipo: Mapped[str]
    categoria: Mapped[str]
    descricao: Mapped[str]
    data: Mapped[str]  

class Emails_bloqueado(Base):
    __tablename__ = 'emails_bloqueado' 
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    idade: Mapped[str]
    ano: Mapped[int]

engine = create_engine("sqlite:///gestor.db")
Base.metadata.create_all(engine)      

Session = sessionmaker(bind=engine)
sessao = Session()