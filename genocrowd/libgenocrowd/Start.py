"""Contain the Start classe
"""
import os

from genocrowd.libgenocrowd.Database import Database
from genocrowd.libgenocrowd.Params import Params


class Start(Params):

    """Initialize the data directory and the database

    Attributes
    ----------
    data_directory : str
        Path to the data directory
    database_path : str
        Path to the database file
    """

    def __init__(self, app, session):
        """Get data directory and database paths from the genocrowd settings

        Parameters
        ----------
        app :
            flask app
        session :
            flask session
        """
        Params.__init__(self, app, session)

        self.data_directory = self.settings.get('genocrowd', 'data_directory')
        self.database_path = self.settings.get('genocrowd', 'database_path')

    def start(self):
        """Create the data diretory and initialize the database file
        """
        self.create_data_directory()
        self.create_database()

    def create_data_directory(self):
        """Create the data directory if it not exists
        """
        if not os.path.isdir(self.data_directory):
            os.makedirs(self.data_directory)

    def create_database(self):
        """Initialize the database file
        """
        database = Database(self.app, self.session)
        database.init_database()
