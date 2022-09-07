"""Extensions to Dictionary type"""


# Separators
KEY_VALUE_SEP = "__"  # Separates key-value pairs
VALUE_SEP = "--" # Separates the key from its value and values from one another
MAX_LIST_LEN = 5  # Maximum length of a list in a string
LIST_BREAK = "..."  # Indicates a break in the list


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
            keys = list(self.keys())
            keys.sort()
            for key in keys:
                value = self[key]
                if isinstance(value, str):
                    name = stringify(key, value)
                elif isinstance(value, list):
                    if len(value) > MAX_LIST_LEN:
                        # List is too long. Add list break
                        value.sort()
                        value_name = VALUE_SEP.join(
                              str(v) for v in value[0:MAX_LIST_LEN-1])
                        value_name = value_name + LIST_BREAK + str(value[-1])
                    else:
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
        if LIST_BREAK in stg:
            raise ValueError("Cannot convert a string with a list break: %s" % stg)
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

    def copy(self):
        """
        Creates a new object of the same class. Handles simple data types:
            int, str, float, bool, list
        
        Returns
        -------
        self.__class__
        """
        dct = dict(self)
        for key, value in self.items():
            if not isinstance(value, str):
                if isinstance(value, list):
                    dct[key] = list(value)
        return self.__class__(**dct)
 
