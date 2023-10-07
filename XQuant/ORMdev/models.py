import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from XQuant.Utils import Tools

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Enum,
    DECIMAL,
    DateTime,
    Boolean,
    UniqueConstraint,
    Index,
)

# 通过其构造一个基类，这个基类和它的子类，可以将Python类和数据库表关联映射起来
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

try:
    config = Tools.get_config(section="root")
except KeyError as ke:
    raise ke
engine = create_engine(
    "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        config["user"],
        config["password"],
        config["host"],
        config["port"],
        config["database"],
    ),
    # 超过链接池大小外最多创建的链接
    max_overflow=0,
    # 链接池大小
    pool_size=5,
    # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
    pool_timeout=10,
    # 多久之后对链接池中的链接进行一次回收
    pool_recycle=1,
    # 查看原生语句（未格式化）
    echo=True,
)

# 绑定引擎
Session = sessionmaker(bind=engine)
# 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# 内部会采用threading.local进行隔离
ScopedSession = scoped_session(Session)


class InternshipMember(Base):
    """必须继承Base"""

    # 数据库中存储的表名
    __tablename__ = "InternshipMember"

    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    name = Column(String(32), index=True, nullable=False, comment="姓名")
    age = Column(Integer, nullable=False, comment="年龄")
    # 对于非必须插入的字段，不用采取nullable=False进行约束
    gender = Column(Enum("male", "female", name="gender"), default="male", comment="性别")
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    last_update_time = Column(
        DateTime, onupdate=datetime.datetime.now, comment="最后更新时间"
    )
    delete_status = Column(Boolean(), default=False, comment="是否删除")

    __table__args__ = (
        UniqueConstraint("name", "age", "phone"),  # 联合唯一约束
        Index("name", "addr", unique=True),  # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} name:{self.name}>"


if __name__ == "__main__":
    # # 删除表
    # Base.metadata.drop_all(engine)
    # 创建表
    Base.metadata.create_all(engine)
