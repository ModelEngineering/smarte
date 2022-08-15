"""Container for the results of experiments."""

import smarte.constants as cn
from smarte.extended_dict import ExtendedDict


UNNAMED = "Unnamed:"


class ExperimentResult(ExtendedDict):

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        dct: dict (partial experiment information)
        """
        super().__init__(kwargs)
        # Cleanup possible DataFrame
        for key in cn.SD_ALL:
            if not key in self.keys():
                self.is_complete = False
                self[key] = None

    def isComplete(self):
        """
        Checks that result has all fields assigned.

        Returns
        -------
        bool
        """
        return all([not v is None for k, v in self.items()])

    @classmethod
    def makeAggregateResult(cls, df=None):
        """
        Creates a result for aggregating other results.

        Parameters
        ----------
        df: DataFrame

        Returns
        -------
        ExperimentResult
        """
        if df is None:
            result = cls(**{k: [] for k in cn.SD_ALL})
        else:
            result = cls()
            for column in df.columns:
                if not UNNAMED in column:
                    result[column] = list(df[column].values)
        return result
