"""Dictionary of elemental types with pre-specified attributes"""

from smarte.types.elemental_type import isList, isStr, isInt, isBool, isFloat,  \
      isElemental

import copy


# Separators
KEY_VALUE_SEP = "__"  # Separates key-value pairs
VALUE_SEP = "--" # Separates the key from its value and values from one another
MAX_LIST_LEN = 5  # Maximum length of a list in a string
LIST_BREAK = "..."  # Indicates a break in the list


class ElementalDict(dict):

    default_dct = {}  # Override to specify keywords and default values

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        kwargs: dict
        """
        super().__init__(**kwargs)
        # Validatation checks
        self._validate(kwargs)
        # Assign defaults
        for key, value in self.default_dct.items():
            if not key in self.keys():
                self[key] = copy.deepcopy(value)

    def _validate(self, dct):
        """
        Checks that values are correct types and have correct keys.
 
        Parameters
        ----------
        dct: dict
        """
        # Validate keys
        diff = set(dct.keys()).difference(self.default_dct.keys())
        if len(diff) > 0:
            raise ValueError("Invalid keys: %s" % str(diff))
        # Validate values
        trues = [isElemental(v) for v in dct.values()]
        if not all(trues):
            raise ValueError("Not elemental type in %s" % str(dct))

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

    def equals(self, other):
        """
        Checks for equal dictionaries. Works for simple types.

        Parameters
        ----------
        ElementalDict

        Returns
        -------
        bool
        """
        return str(self) == str(other)

    @classmethod
    def makeFromStr(cls, stg):
        """
        Decodes the string as a representation of the dictionary.

        Parameters
        ----------
        stg: str (string representation)

        Returns
        -------
        ElementalDict
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
            if isStr(value):
                if len(value) == 0:
                    raise ValueError("Invalid value for element instance.")
                # bool
                if isBool(eval(value)):
                    new_value = eval(value)
                # int
                elif isInt(eval(value)):
                    new_value = int(value)
                # float
                elif isFloat(eval(value)):
                    new_value = float(value)
                # str
                else:
                    new_value = value
            else:
                new_value = value
            return new_value
        #
        if LIST_BREAK in stg:
            raise ValueError("Cannot convert a string with a list break: %s" % stg)
        # Construct the dictionary from the string
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
        Creates a deep object of the same class. Handles simple data types:
            int, str, float, bool, list
        
        Returns
        -------
        self.__class__
        """
        return copy.deepcopy(self)
