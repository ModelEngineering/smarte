"""Extensions to Dictionary type"""


# Separators
KEY_VALUE_SEP = "__"  # Separates key-value pairs
VALUE_SEP = "--" # Separates the key from its value and values from one another


class ExtendedDict(dict):

    def __init__(self, *pargs, is_elemental=True, **kwargs):
        """
        Parameters
        ----------
        is_elemental: bool (values are elemental types or list)

        Returns
        -------
        """
        super().__init__(*pargs, **kwargs)
        self.is_elemental = is_elemental

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

    def extend(self, dct, is_duplicates=False):
        """
        Extends values in dictionary.

        Parameters
        ----------
        dct: dict
            key: key to use
            value: value to append
        is_duplicates: allow duplicates
        """
        if len(self) == 0:
            for key in dct.keys():
                self[key] = []
        for key, value in dct.items():
            if is_duplicates:
                self[key].extend(value)
            else:
                result = set(self[key]).union(value)
                self[key] = list(result)

    def __str__(self):
        """
        Creates a name based on the keys and values. Works
        for elementary types.

        Returns
        -------
        str
        """
        def stringify(key, value):
            return key + VALUE_SEP + str(value)
        #
        if self.is_elemental:
            names = []
            for key, value in self.items():
                if isinstance(value, str):
                    name = stringify(key, value)
                elif isinstance(value, list):
                    value_name = VALUE_SEP.join([str(v) for v in value])
                    name = stringify(key, value_name)
                else:
                    name = stringify(key, value)
                names.append(name)
            return KEY_VALUE_SEP.join(names)
        return super().__str__()

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
    def getFromStr(cls, stg):
        """
        Decodes the string as a representation of the dictionary.

        Parameters
        ----------
        stg: str (string representation)

        Returns
        -------
        ExtendedDict
        """
        def convert(value):
            """
            Converts to correct type.

            Parameters
            ----------
            value: str

            Returns
            -------
            int, bool, float, str
            """
            # bool
            if str(value) in ["True", "False"]:
                new_value = eval(value)
            # int
            elif isinstance(eval(value), int):
                new_value = int(value)
            # float
            elif isinstance(eval(value), float):
                new_value = float(value)
            # str
            else:
                new_value = value
            return new_value
        #
        dct = {}
        key_values = stg.split(KEY_VALUE_SEP)
        for key_value in key_values:
            # Parse the key and value(s)
            parts = key_value.split(VALUE_SEP)
            if len(parts) == 2:
                key, values = parts
            elif len(parts) < 2:
                raise RuntimeError("Wrong size.")
            else:
                key = parts[0]
                values = parts[1:]
            # Decode the types
            if isinstance(values, str):
                try:
                    dct[key] = convert(values)
                except NameError:
                    dct[key] = values
            elif isinstance(values, list):
                dct[key] = [convert(v) for v in values]
            else:
                dct[key] = values
        return cls(**dct)
