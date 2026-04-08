#!/usr/bin/env python3

"""
File: dataset.py
----------------
The Dataset object reads a data file of data instances, stores the data internally, and allows
the user access to one row of the data at a time.

We assume the file is set-up as follows:
   - the data is formatted as comma separated values that are all integers
   - each row of the file contains one data instance and all rows have the same number of values
   - the last value (column) in each row is assumed to be the output feature for that data instance
   - all other columns (besides the last) are assumed to be the input features for that data instance
"""


class Dataset:

    def __init__(self, filename):
        """
        Creates a Dataset by reading in the file with the given filename.
        """
        self.data = []     # table (list of lists) of all input data, one row per data instance
        self.outputs = []  # list of output values, one per instance (in same order as rows in data)

        # Read the file line-by-line
        with open(filename, "r") as input_file:
            for line in input_file:                 # Each line represents one instance
                entries = line.strip().split(',')   # Assume comma separated values

                # Populate a list to represent data instance (features only) in data file
                instance = []
                for value in entries[:-1]:
                    instance.append(int(value))     # Assume all values are integers

                self.data.append(instance)          # Add data instance to the dataset

                # Keep track of corresponding output feature in outputs list
                self.outputs.append(int(entries[-1]))   # Assume output is last value in data instance

        input_file.close()

    def get_size(self):
        """
        Returns the number of data instances (rows) in the dataset.
        """
        return len(self.data)

    def get_input_dimensions(self):
        """
        Returns number of input dimensions (features) in each row in dataset.
        Note number returned does NOT count the output variable.
        """
        if not self.data:   # Check for empty data
            return 0
        else:
            return len(self.data[0])

    def get_instance(self, index):
        """
        Returns the data instance (input features) at the specified index.
        """
        return self.data[index]

    def get_output(self, index):
        """
        Returns the output feature/value for the data instance at the specified index.
        """
        return self.outputs[index]
