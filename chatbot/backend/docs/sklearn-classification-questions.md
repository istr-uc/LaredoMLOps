# Questions and Answers about Classification in Machine Learning

## What is classification in machine learning?

-   Classification is a supervised machine learning task.
-   A model assigns elements to categories or classes based on their features.
-   It is trained with labeled data to predict the class of new data.

## What is a Random Forest Classifier?

-   It is a model based on decision trees.
-   It uses multiple trees trained with subsets of data.
-   It combines predictions to improve accuracy and reduce overfitting.

## What does the `n_estimators` parameter do in the RandomForestClassifier?

-   It determines how many trees will be trained in the model.
-   Higher values improve accuracy but increase computation time.

## What is the difference between `DecisionTreeClassifier` and `RandomForestClassifier`?

-   `DecisionTreeClassifier`: Uses a single tree, can overfit.
-   `RandomForestClassifier`: Uses multiple trees, reduces overfitting and improves accuracy.

## What is an `SVC` and how does it work?

-   `SVC` (Support Vector Classifier) uses Support Vector Machines (SVM).
-   It finds a hyperplane that separates categories with the largest margin.
-   It uses "kernels" for non-linearly separable data.

## What does the `kernel='rbf'` parameter mean in SVC?

-   It uses the radial basis function kernel.
-   Useful for non-linearly separable data.
-   Transforms data into a higher-dimensional space.

## Why is the `C` parameter important in SVC?

-   It controls the balance between accuracy and separation margin.
-   Low values: larger margin, flexibility.
-   High values: attempts to classify correctly, risk of overfitting.

## What does the `max_depth` parameter do in `DecisionTreeClassifier`?

-   It controls the maximum depth of the tree.
-   `None`: grows until pure leaves or few data.
-   Limits depth to avoid overfitting.

## What is the `class_weight` parameter used for in classifiers?

-   Adjusts class weights for imbalanced data.
-   `'balanced'`: adjusts weights based on class frequency.

## What is decision tree pruning and how is it controlled?

-   Removes irrelevant branches to simplify the model.
-   Avoids overfitting.
-   Controlled by the `ccp_alpha` parameter.
-   `ccp_alpha`: sets how much impurity must be reduced in each split.