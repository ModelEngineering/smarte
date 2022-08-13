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
    
    def __str__(self):
        """
        Creates a name based on the keys and values.

        Returns
        -------
        str
        """
        names = [k + cn.KEY_VALUE_SEP + str(v) for k, v in self.items()]
        return cn.KEY_SEP.join(names)

    def equals(self, other):
        """
        Checks for equal dictionaries. Works for simple types.

        Parameters
        ----------
        ExtendedDict
        
        Returns
        -------
        bool
        """
        return str(self) == str(other)

    @classmethod
    def get(cls, stg):
        """
        Decodes the string as a representation of the dictionary.

        Parameters
        ----------
        stg: str (string representation)
        
        Returns
        -------
        ExtendedDict
        """
        dct = {}
        key_values = condition_str.split(cn.KEY_SEP)
        for key_value in key_values:
            key, value = key_value.split(cn.KEY_VALUE_SEP)
            try:
                new_value = int(value)
            except ValueError:
                try:
                    new_value = float(value)
                except ValueError:
                    new_value = value
            dct[key] = new_value
        return cls(**dct)
