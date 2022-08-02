"""Extensions to Dictionary type"""

class ExtendedDict(dict):

    def append(self, dct):
        """
        Appends values in dictionary.

        Parameters
        ----------
        dct: dict
            key: key to use
            value: value to append
        """
        if len(self) == 0:
            for key in dct.keys():
                self[key] = []
        for key, value in dct.items():
            self[key].append(value)
