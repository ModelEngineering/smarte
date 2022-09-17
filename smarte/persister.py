"""Simple interface to Pickle"""

import os
import pickle


class Persister:

    def __init__(self, path):
        """
        Parameters
        ----------
        path: str (path to file used to save data)
        """
        self.path = path

    def dump(self, data):
        """
        Dump data to file.

        Parameters
        ----------
        data: obejct (what to save)
        """
        with open(self.path, "wb") as fd:
            pickle.dump(data, fd, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        """
        Retrieves data that was saved previously.
        
        Returns
        -------
        object
        """
        with open(self.path, "rb") as fd:
            data = pickle.load(fd)
        return data

    def isExist(self):
        """
        Tests if a file of saved data exists.
        
        Returns
        -------
        bool
        """
        return os.path.isfile(self.path)

    def delete(self):
        """
        Deletes the saved file if it exists.
        """
        if os.path.isfile(self.path):
            os.remove(self.path)
