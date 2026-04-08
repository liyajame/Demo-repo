#!/usr/bin/env python3

"""
File: perceptronmodel.py
------------------------
This file implements the PerceptronModel.  The PerceptronModel can be trained on a Dataset using
the Batch Perceptron Pocket algorithm.  The trained model is simply a set of weights that
are multiplied against the respective input features of a data instance to generate a prediction.
PerceptronModels can also be written to and read from files.

When training a PerceptronModel on a Dataset, the user can choose to only consider a particular set
of input features from the training data.  In that case, the PerceptronModel will not update weights
for any of the unused features, leaving them at 0 so they will not impact the predictions made on
any data.

Note: We did not use numpy in this implementation because it is not covered in CS106A and we wanted
the code to be understandable for students who do not have familiarity with numpy.  We recognize that
the Python code is slower to run than if we tried to optimize the implementation.  This is was an
explicit design decision.  If you are familiar with numpy and want a faster implementation, feel free
to change the implementation to use numpy arrays instead of lists.
"""

from dataset import Dataset


class PerceptronModel:

    # Constants

    # Number of epochs to train the model
    EPOCHS = 2000

    # Initial learning rate
    INITIAL_LEARNING_RATE = 10

    # Factor by which we multiply the learning rate after training for EPOCHS_PER_REDUCTION epochs
    LEARNING_RATE_REDUCTION = 0.95

    # Number of epochs of training in between a reduction in learning rate
    EPOCHS_PER_REDUCTION = 100

    def __init__(self, data, features_to_use=None):
        """
        Creates a Perceptron model.  If the first parameter is a Dataset, then we create the model
        by training on the given data using the Batch Perceptron Pocket algorithm.  If the first
        parameter is a string, then we assume this string is a filename of a file containing weights
        of the model and initialize the model with those weights.  If the first parameter is neither
        a Dataset nor a string, then we just create an empty model (i.e., no weights).
        """
        # Create the list of weights for the model as well as the "pocket" weights
        self.weights = []

        # Use the type of the first parameter to determine how to set weights of the model
        # This is a simple way to create an "overloaded" constructor in Python since it does
        # not natively support overloading.
        if isinstance(data, Dataset):                   # Check for Dataset as first parameter
            self.train_with_data(data, features_to_use)
        elif isinstance(data, str):                     # Check for string as first parameter
            self.load_from_file(data)                   # Here, assume data is really a file name

    def train_with_data(self, data, features_to_use):
        """
        Trains a Perceptron model (using the Batch Perceptron Pocket algorithm), which is
        trained on the data passed in, but only using the input features whose indexes
        are included in the list features_to_use.  The weights for any features not
        included in features_to_use will not be updated during training, leaving them at 0
        when training is completed.  If the list features_to_use is not passed in (i.e., it
        is set to None by default), then all input features in the data are used during training.
        """

        # Create the list of "pocket" weights
        pocket = []

        # Initialize the weights and the "pocket" weights to 0
        for i in range(data.get_input_dimensions()):
            self.weights.append(0)
            pocket.append(0)

        max_correct = 0             # Used to determine the best set of weights to put in our "pocket"

        learning_rate = self.INITIAL_LEARNING_RATE

        # Make EPOCHS passes through the data to train the model
        for epoch in range(self.EPOCHS):

            # Create and initialize the list of differences used to update weights in the model
            difference = []
            for i in range(data.get_input_dimensions()):
                difference.append(0)

            correct = 0             # For each epoch, keep track of the number of correct predictions

            # Make a pass through the data passed in
            for i in range(data.get_size()):

                # For each data instance, make a prediction and determine if it is correct or not
                instance = data.get_instance(i)
                prediction = self.predict(instance)
                actual_output = data.get_output(i)
                error = actual_output - prediction

                # If actualOutput and prediction don't match, error will be 1 or -1.
                # If actualOutput and prediction match, then error is 0.
                if error == 0:                                  # Correct prediction
                    correct += 1
                else:                                           # Incorrect prediction
                    for j in range(len(difference)):
                        difference[j] += error * instance[j]    # Update differences based on error

            # After making a pass through all the data, see if our current set of weights
            # produced more correct predictions than the weights in our "pocket".  If it
            # did, then store the current set of weights in our "pocket"
            if correct > max_correct:
                for i in range(len(self.weights)):
                    pocket[i] = self.weights[i]

                max_correct = correct
                print("Updated pocket on epoch", epoch)

            # Update all the weights based on the average difference (multiplied by the learning rate)
            for j in range(len(self.weights)):
                if (features_to_use is None) or (j in features_to_use):
                    self.weights[j] += (learning_rate * difference[j])/data.get_size()

            # After every EPOCHS_PER_REDUCTION epochs, lower the learning rate by multiplying it
            # by the LEARNING_RATE_REDUCTION.  Gradually lower the learning rate in this way helps
            # to stabilize the weights over time by reducing the amount of change.  We also print
            # a diagnostic message to the console to show the progress of the algorithm.
            if ((epoch + 1) % self.EPOCHS_PER_REDUCTION) == 0:
                learning_rate *= self.LEARNING_RATE_REDUCTION
                print("Completed epoch #" + str(epoch + 1) + ", Learning rate =", learning_rate)

        # Store the weights in our "pocket" as a final model.
        self.weights = pocket

    def load_from_file(self, filename):
        """
        Creates a new PerceptronModel by reading the weights for the model from the given file
        (rather than training using data).  Assumes the format of the file has one line per weight,
        where each line has the form:
        <feature name>: <weight>
        Note that feature names should not include a ':' character as that is the delimiter
        between the feature name and the weight.
        """

        # Create the list of weights for the model
        self.weights = []

        # Read the file containing the weights for the model
        with open(filename, "r") as input_file:
            for line in input_file:                 # Assume there is one line per weight
                entries = line.strip().split(':')   # Assume ':' separates feature name from weight value
                self.weights.append(float(entries[1]))  # Second entry on each line should be weight

        input_file.close()

    def save_model_weights(self, filename, names=None):
        """
        Save the model weights to a file with the given filename.  The output file will have one
        weight per line.  The names list should provide descriptive names for the features
        that will be included in the file for readability.  The names list should be at least
        as long as the number of weights in the model.  If the names list is not specified then
        the weights in the file will just be given the generic names "Feature #<x>"
        If the names list is provided then the format for each line weight will be:
          <names[x]>: <weight>
        If the names list is not provided then the format for each line weight will be:
          Feature #x: <weight>
        where (in either case) x represents the index number of the feature, and <weight> is the
        numeric weight value
        """

        # Create output file
        with open(filename, "w") as output:
            # Write one line per feature
            for i in range(len(self.weights)):
                feature_name = "Feature #" + str(i)     # Set default feature name
                if names is not None:
                    feature_name = names[i]             # Overwrite feature name if we are given list of names
                line = feature_name + ": " + str(self.weights[i]) + "\n"
                output.write(line)
        output.close()

    def get_model_weights(self):
        """
        Returns a list containing the weights in the model
        """
        return self.weights

    def predict(self, instance):
        """
        Returns a prediction (0 or 1) that the model would make on the given data instance
        """
        total = self.weighted_sum(instance)
        if total >= 0:
            return 1
        else:
            return 0

    def weighted_sum(self, instance):
        """
        Returns the weighted sum of the model weights multiplied by the respective features in the
        given data instance
        """
        total = 0
        for i in range(len(self.weights)):
            total += instance[i] * self.weights[i]
        return total
