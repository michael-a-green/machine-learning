# Import libraries
import numpy as np
import pandas as pd
from time import time
from sklearn.metrics import f1_score

# Read student data
student_data = pd.read_csv("student-data.csv")
print "Student data read successfully!"

def preprocess_features(X):
    ''' Preprocesses the student data and converts non-numeric binary variables into
        binary (0/1) variables. Converts categorical variables into dummy variables. '''
    
    # Initialize new output DataFrame
    output = pd.DataFrame(index = X.index)

    # Investigate each feature column for the data
    for col, col_data in X.iteritems():
        
        # If data type is non-numeric, replace all yes/no values with 1/0
        if col_data.dtype == object:
            col_data = col_data.replace(['yes', 'no'], [1, 0])

        # If data type is categorical, convert to dummy variables
        if col_data.dtype == object:
            # Example: 'school' => 'school_GP' and 'school_MS'
            col_data = pd.get_dummies(col_data, prefix = col)  
        
        # Collect the revised columns
        output = output.join(col_data)
    
    return output


# Extract feature columns
feature_cols = list(student_data.columns[:-1])

# Extract target column 'passed'
target_col = student_data.columns[-1] 

# Show the list of columns
print "Feature columns:\n{}".format(feature_cols)
print "\nTarget column: {}".format(target_col)

# Separate the data into feature data and target data (X_all and y_all, respectively)
X_all = student_data[feature_cols]
y_all = student_data[target_col]

# for i in range(len(y_all)):
# 
#     if y_all.loc[i] == 'no':
#         y_all.set_value(i,0) 
#     else:
#         y_all.set_value(i,0)



# Show the feature information by printing the first five rows
print "\nFeature values:"
print X_all.head()


X_all = preprocess_features(X_all)
print "Processed feature columns ({} total features):\n{}".format(len(X_all.columns), list(X_all.columns))


# TODO: Import any additional functionality you may need here
from sklearn.cross_validation import train_test_split
    
# TODO: Set the number of training points
num_train = 300

# Set the number of testing points
num_test = X_all.shape[0] - num_train

# TODO: Shuffle and split the dataset into the number of training and testing points above
X_train = None
X_test = None
y_train = None
y_test = None

X_train, X_test, y_train, y_test = train_test_split(X_all, 
                                                    y_all, 
                                                    test_size = num_test, 
                                                    train_size = num_train,
                                                    random_state = 42
                                                   )

# Show the results of the split
print "Training set has {} samples.".format(X_train.shape[0])
print "Testing set has {} samples.".format(X_test.shape[0])

def train_classifier(clf, X_train, y_train):
    ''' Fits a classifier to the training data. '''
    
    # Start the clock, train the classifier, then stop the clock
    start = time()
    clf.fit(X_train, y_train)
    end = time()
    
    # Print the results
    print "Trained model in {:.4f} seconds".format(end - start)

    
def predict_labels(clf, features, target):
    ''' Makes predictions using a fit classifier based on F1 score. '''
    
    # Start the clock, make predictions, then stop the clock
    start = time()
    y_pred = clf.predict(features)
    end = time()
    
    # Print and return results
    print "Made predictions in {:.4f} seconds.".format(end - start)
    return f1_score(target.values, y_pred, pos_label='yes')


def train_predict(clf, X_train, y_train, X_test, y_test):
    ''' Train and predict using a classifer based on F1 score. '''
    
    # Indicate the classifier and the training set size
    print "Training a {} using a training set size of {}. . .".format(clf.__class__.__name__, len(X_train))
    
    # Train the classifier
    train_classifier(clf, X_train, y_train)
    
    # Print the results of prediction for both training and testing
    print "F1 score for training set: {:.4f}.".format(predict_labels(clf, X_train, y_train))
    print "F1 score for test set: {:.4f}.".format(predict_labels(clf, X_test, y_test))

# TODO: Import the three supervised learning models from sklearn
# from sklearn import model_A
from sklearn import tree

# from sklearn import model_B
from sklearn import neighbors

#KNN classifier initialization parameters
knnNeighbors = 5
knnWeights = "distance"

# from sklearn import model_C
from sklearn.ensemble import AdaBoostClassifier

#AdaBoost initialization parameters
abNoOfEstimators = 100

# TODO: Initialize the three models
clf_A = tree.DecisionTreeClassifier()
clf_B = neighbors.KNeighborsClassifier(knnNeighbors, knnWeights)
clf_C = AdaBoostClassifier(n_estimators=abNoOfEstimators,algorithm='SAMME')

# TODO: Set up the training set sizes
X_train_100 = None
y_train_100 = None

X_train_100, X_test, y_train_100, y_test = train_test_split(
                                                    X_all, 
                                                    y_all, 
                                                    test_size = (X_all.shape[0] - 100), 
                                                    train_size = 100,
                                                    random_state = 42
                                                   )

#for classifier A
train_predict(clf_A, X_train_100, y_train_100, X_test, y_test)

print "\n"

#for classifier B
train_predict(clf_B, X_train_100, y_train_100, X_test, y_test)

print "\n"

#for classifier C
train_predict(clf_C, X_train_100, y_train_100, X_test, y_test)

print "\n"
print "\n"


X_train_200 = None
y_train_200 = None

X_train_200, X_test, y_train_200, y_test = train_test_split(
                                                    X_all, 
                                                    y_all, 
                                                    test_size = (X_all.shape[0] - 200), 
                                                    train_size = 200,
                                                    random_state = 42
                                                   )

#for classifier A
train_predict(clf_A, X_train_200, y_train_200, X_test, y_test)

print "\n"


#for classifier B
train_predict(clf_B, X_train_200, y_train_200, X_test, y_test)

print "\n"


#for classifier C
train_predict(clf_C, X_train_200, y_train_200, X_test, y_test)

print "\n"
print "\n"


X_train_300 = None
y_train_300 = None

X_train_300, X_test, y_train_300, y_test = train_test_split(
                                                    X_all, 
                                                    y_all, 
                                                    test_size = (X_all.shape[0] - 300), 
                                                    train_size = 300,
                                                    random_state = 42
                                                   )

#for classifier A
train_predict(clf_A, X_train_300, y_train_300, X_test, y_test)

print "\n"

#for classifier B
train_predict(clf_B, X_train_300, y_train_300, X_test, y_test)

print "\n"

#for classifier C
train_predict(clf_C, X_train_300, y_train_300, X_test, y_test)

print "\n"
print "\n"



# TODO: Import 'GridSearchCV' and 'make_scorer'
from   sklearn.grid_search import GridSearchCV
from sklearn.metrics import explained_variance_score, make_scorer
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier


# TODO: Create the parameters list you wish to tune
parameters = {'base_estimator' : [
            DecisionTreeClassifier(max_depth=2),
            DecisionTreeClassifier(max_depth=5), DecisionTreeClassifier(max_depth=10)],
             'n_estimators' : [100,150,200]}

# TODO: Initialize the classifier
clf = AdaBoostClassifier(n_estimators=50,algorithm='SAMME')

# TODO: Make an f1 scoring function using 'make_scorer' 
#f1_scorer = make_scorer(explained_variance_score)
f1_scorer = make_scorer(f1_score, pos_label='yes')
# TODO: Perform grid search on the classifier using the f1_scorer as the scoring method
grid_obj = GridSearchCV(clf,parameters,f1_scorer)


#recreating training and testing sets
X_train_300, X_test, y_train_300, y_test = train_test_split(
                                                    X_all, 
                                                    y_all, 
                                                    test_size = (X_all.shape[0] - 300), 
                                                    train_size = 300,
                                                    random_state = 42
                                                   )
print "X_train_300 = \n"
print X_train_300

print "y_train_300 = \n"
print y_train_300

print "X_test = \n"
print X_test

print "y_test = \n"
print y_test

#print "old contents of y_train_300\n"
#print y_train_300

#for i in range(len(y_train_300)):
#    if y_train_300.loc[i] == 'yes':
#        y_train_300.set_value(i,1)
#    else:
#        y_train_300.set_value(i,0)

# y_train_300_2 = []
# 
# print "y_train_300_2", y_train_300_2
# 
# for col, col_data in y_train_300.iteritems():
#     
#     print "col_data = ", col_data
#     
#     if col_data == 'yes':
#         y_train_300_2.append(1)
#     else:
#         y_train_300_2.append(0)
# 
# print "new contents of y_train_300_2\n"
# print y_train_300_2
# 
# y_train_300_3 = np.asarray(y_train_300_2)
# 
# print "new contents of y_train_300_3\n"
# print y_train_300_3
# 
# #converting y_test into something digestable
# y_test_2 = []
# 
# for col, col_data in y_test.iteritems():
#     
#     print "col_data = ", col_data
#     
#     if col_data == 'yes':
#         y_test_2.append(1)
#     else:
#         y_test_2.append(0)
# 
# print "new contents of y_test_2\n"
# print y_test_2
# 
# 
# y_test_3 = np.asarray(y_test_2)
# 
# print "y_test_3 = \n"
# print y_test_3

# TODO: Fit the grid search object to the training data and find the optimal parameters
grid_obj = grid_obj.fit(X_train_300, y_train_300)

# Get the estimator
clf = grid_obj.best_estimator_

# Report the final F1 score for training and testing after parameter tuning
print "Tuned model has a training F1 score of {:.4f}.".format(predict_labels(clf, X_train_300, y_train_300))
print "Tuned model has a testing F1 score of {:.4f}.".format(predict_labels(clf, X_test, y_test))

