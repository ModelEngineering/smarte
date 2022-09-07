"""Provides information for simulating an arbitrary collection of conditions"""

import smarte as smt


class WorkunitInfo(object):

    def __init__(self, conditions=None, result_collection=None):
        """
        Parameters
        ----------
        conditions: list-ExperimentCondition
        result_collection: ExperimentResultCollection
        """
        self.conditions = conditions
        if self.conditions is None:
            self.conditions = []
        else:
            self.conditions = list(self.conditions)
        self.result_collection = result_collection
        if self.result_collection is None:
            self.result_collection = smt.ExperimentResultCollection()
        else:
            self.result_collection = self.result_collection.copy()

    def extend(self, workunit_info):
        """
        Combines another WorkunitInfo with this one.

        Parameters
        ----------
        workunit_info: WorkunitInfo
        is_duplicates: bool (allow duplicates)
        """
        self.conditions.extend(workunit_info.conditions)
        self.result_collection.extend(workunit_info.result_collection,
              is_duplicates=True)

    def clean(self):
        """
        Removes all conditions that are in the result_collection.
        """
        result_conditions = smt.ExperimentCondition.getFromResultCollection(
              self.result_collection)
        result_condition_strs = [has(str(c)) for c in result_conditions]
        conditions = [c for c in self.conditions
              if not hash(str(c)) in result_condition_strs]
        self.conditions = conditions

    def equals(self, workunit_info):
        """
        Checks if the WorkunitInfo have the same values.

        Parameters
        ----------
        workunit_info: WorkunitInfo
        
        Returns
        -------
        bool
        """
        condition_strs = [str(c) for c in self.conditions]
        is_same_condition = all([str(c) in condition_strs
              for c in result_collection.conditions])
        #
        return is_same_condition and  \
              self.result_collection.equals(workunit_info.result_collection)
