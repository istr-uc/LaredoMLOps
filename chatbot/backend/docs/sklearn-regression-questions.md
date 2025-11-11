# Questions and Answers about Regression in Supervised Learning

## What is regression in supervised learning?

-   A type of supervised learning where a model predicts a numerical value.
-   Learns patterns from past data to make predictions on new data.
-   Predicts continuous values, unlike classification which assigns labels.

## How does a regression model work?

-   Fits a mathematical function that represents the relationship between input and output variables.
-   Example: predicting house price based on its size.

## What is a RandomForestRegressor?

-   Machine learning model that uses random forests.
-   Trains multiple decision trees and averages their predictions.
-   Improves model accuracy and stability.

## What are the main parameters of RandomForestRegressor?

-   `n_estimators`: Number of trees in the forest.
-   `criterion`: Metric to measure the quality of a split.
-   `max_depth`: Maximum depth of each tree.
-   `min_samples_split`: Minimum samples to split a node.
-   `bootstrap`: If `True`, each tree is trained with a random sample of the data.

## In what situations is it appropriate to use RandomForestRegressor?

-   When a robust and accurate model is needed.
-   To avoid overfitting.
-   In problems with non-linear relationships between input and output variables.

## What is a DecisionTreeRegressor?

-   Regression model based on decision trees.
-   Divides data into subgroups and makes predictions based on input data.

## What main parameters are used in DecisionTreeRegressor?

-   `criterion`: Node splitting metric.
-   `splitter`: Strategy to choose the split point.
-   `max_depth`: Maximum depth of the tree.
-   `min_samples_split`: Minimum samples needed to split a node.

## When should a DecisionTreeRegressor be used?

-   When there is a non-linear relationship between variables.
-   When an interpretable model is desired.
-   For tasks requiring fast and simple predictions.

## What is SVR (Support Vector Regression)?

-   Regression model based on the support vector algorithm (SVM).
-   Seeks a "tolerance zone" and predicts continuous values within a margin of error.

## What are some important parameters of SVR?

-   `kernel`: Type of kernel used (e.g., `'rbf'`, `'linear'`).
-   `C`: Controls the balance between error and model complexity.
-   `epsilon`: Defines the "tolerance zone" for errors.
-   `gamma`: Controls the shape of the kernel function.

## When should SVR be used?

-   When data has non-linear relationships.
-   When precise control over the error margin is desired.
-   Ideal for complex and non-linear problems.

## What is a KNeighborsRegressor?

-   Regression model based on k-nearest neighbors.
-   Predicts a continuous value based on the average of its k neighbors' values.

## What are the main parameters of KNeighborsRegressor?

-   `n_neighbors`: Number of neighbors to consider.
-   `weights`: How to weight neighbors (`'uniform'` or `'distance'`).
-   `algorithm`: Algorithm to find nearest neighbors.
-   `metric`: Metric to calculate distances between points.

## When is it appropriate to use KNeighborsRegressor?

-   When the exact form of the relationship between variables is unknown.
-   When non-linear relationships are complicated.

## What is MSE and how is it used in regression?

-   MSE (Mean Squared Error): measures the average difference between predicted and actual values.
-   A low value indicates better model accuracy.

## What is R^2 and how is it interpreted?

-   R² (Coefficient of Determination): measures how well the model explains data variability.
-   1: model completely explains variability.
-   0: model explains nothing.

## What is overfitting in a model?

-   The model fits the training data too closely.
-   Affects the ability to generalize well to new data.

## What is underfitting in a model?

-   The model does not fit the training data closely enough.
-   Results in poor prediction performance.