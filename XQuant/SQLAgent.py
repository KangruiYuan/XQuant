from sqlalchemy import create_engine
from .Utils import Tools
import psycopg2


class SQLAgent:
    engine = None
    conn = None

    @classmethod
    def postgres_connection(cls, config: dict = None, **kwargs):
        """
        :param config: should be a dictionary, organized as the following structure
            {
                host = ***
                database = ***
                user = ***
                password = ***
                port = ***
            }
        :param kwargs:
        :return:
        """
        if config is None:
            try:
                config = Tools.get_config(section=kwargs.get("section", "postgresql"))
            except KeyError as ke:
                raise ke
        try:
            conn = psycopg2.connect(**config)
            cls.conn = conn
            return conn
        except psycopg2.DatabaseError as dbe:
            raise dbe

    @classmethod
    def postgres_engine(cls, config: dict = None, **kwargs):
        """
        :param config: should be a dictionary, organized as the following structure
            {
                host = ***
                database = ***
                user = ***
                password = ***
                port = ***
            }
        :param kwargs:
        :return:
        """
        if config is None:
            try:
                config = Tools.get_config(section=kwargs.get("section", "postgresql"))
            except KeyError as ke:
                raise ke
        engine = create_engine(
            "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                config["user"],
                config["password"],
                config["host"],
                config["port"],
                config["database"],
            )
        )
        cls.engine = engine
        return engine

