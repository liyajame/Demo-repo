#!/usr/bin/env python3

"""
File: constants.py
------------------
The file contains sets of constants that are relevant for the recidivism data that
is used for training and testing our Perceptron algorithm.  This file can be imported
by any module that wants to access these constants.

Enumeration of the index numbers of input features in recividism data files.
Each constant refers to the index number for a particular input feature in the data. 
The constants below are grouped by input feature type (i.e., set of binary features
that provide a "one hot" encoding of the underlying value of the feature).
"""

# Indexes of input features based on:
# number of prior juvenile felony convictions (bucketed into 4 categories)
JUVENILE_FELONY_COUNT_0 = 0
JUVENILE_FELONY_COUNT_1 = 1
JUVENILE_FELONY_COUNT_2 = 2
JUVENILE_FELONY_COUNT_3_OR_MORE = 3

# Indexes of input features based on:
# number of prior juvenile misdemeanor convictions (bucketed into 4 categories)
JUVENILE_MISDEMEANOR_COUNT_0 = 4
JUVENILE_MISDEMEANOR_COUNT_1 = 5
JUVENILE_MISDEMEANOR_COUNT_2 = 6
JUVENILE_MISDEMEANOR_COUNT_3_OR_MORE = 7

# Indexes of input features based on:
# number of prior non-felony/non-misdemeanor juvenile convictions (bucketed into 4 categories)
JUVENILE_OTHER_COUNT_0 = 8
JUVENILE_OTHER_COUNT_1 = 9
JUVENILE_OTHER_COUNT_2 = 10
JUVENILE_OTHER_COUNT_3_OR_MORE = 11

# Indexes of input features based on:
# number of prior (adult) criminal convictions (bucketed into 4 categories)
PRIOR_CONVICTIONS_COUNT_0 = 12
PRIOR_CONVICTIONS_COUNT_1 = 13
PRIOR_CONVICTIONS_COUNT_2 = 14
PRIOR_CONVICTIONS_COUNT_3_OR_MORE = 15

# Indexes of input features based on:
# degree of criminal charge (felony or misdemeanor)
CHARGE_DEGREE_FELONY = 16
CHARGE_DEGREE_MISDEMEANOR = 17

# Indexes of input features based on:
# criminal charge (bucketed into 12 categories)
CHARGE_DESC_NO_CHARGE = 18
CHARGE_DESC_LICENSE_ISSUE = 19
CHARGE_DESC_PUBLIC_DISTURBANCE = 20
CHARGE_DESC_NEGLIGENCE = 21
CHARGE_DESC_DRUG_RELATED = 22
CHARGE_DESC_ALCOHOL_RELATED = 23
CHARGE_DESC_WEAPONS_RELATED = 24
CHARGE_DESC_EVADING_ARREST = 25
CHARGE_DESC_NONVIOLENT_HARM = 26
CHARGE_DESC_THEFT_FRAUD_BURGLARY = 27
CHARGE_DESC_LEWDNESS_PROSTITUTION = 28
CHARGE_DESC_VIOLENT_CRIME = 29

# Indexes of input features based on:
# age (bucketed into 3 categories)
AGE_LESS_THAN_25 = 30
AGE_25_TO_45 = 31
AGE_GREATER_THAN_45 = 32

# Indexes of input features based on:
# gender (bucketed into 2 categories)
GENDER_FEMALE = 33
GENDER_MALE = 34

# Indexes of input features based on:
# race (bucketed into 6 categories)
"""

RACE_OTHER = 35
RACE_ASIAN = 36
RACE_NATIVE_AMERICAN = 37
RACE_CAUCASIAN = 38
RACE_HISPANIC = 39
RACE_AFRICAN_AMERICAN = 40
"""


"""
Names of input features in the recidivism data files.  The strings in this list
are in the same order as the corresponding input features in the file.
For example: feature_names[GENDER_FEMALE] == "Female"
This list is provided simply for making programmatic output involving features easier to read.
"""
feature_names = [
    "Juvenile felony count = 0",
    "Juvenile felony count = 1",
    "Juvenile felony count = 2",
    "Juvenile felony count >= 3",
    "Juvenile misdemeanor count = 0",
    "Juvenile misdemeanor count = 1",
    "Juvenile misdemeanor count = 2",
    "Juvenile misdemeanor count >= 3",
    "Juvenile other offense count = 0",
    "Juvenile other offense count = 1",
    "Juvenile other offense count = 2",
    "Juvenile other offense count >= 3",
    "Prior conviction count = 0",
    "Prior conviction count = 1",
    "Prior conviction count = 2",
    "Prior conviction count >= 3",
    "Charge degree = felony",
    "Charge degree = misdemeanor",
    "Charge description = no charge",
    "Charge description = license issue",
    "Charge description = public disturbance",
    "Charge description = negligence",
    "Charge description = drug related",
    "Charge description = alcohol related",
    "Charge description = weapons related",
    "Charge description = evading arrest",
    "Charge description = nonviolent harm",
    "Charge description = theft/fraud/burglary",
    "Charge description = lewdness/prostitution",
    "Charge description = violent crime",
    "Age < 25",
    "Age >= 25 and <=45",
    "Age > 45",
    "Gender = Female",
    "Gender = Male"
    #"Race = Other",
    #"Race = Asian",
    #"Race = Native American",
    #"Race = Caucasian",
    #"Race = Hispanic",
    #"Race = African American"
]
