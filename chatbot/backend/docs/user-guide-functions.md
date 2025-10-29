# Definitions for the Laredo Application

This document provides definitions and explanations of the key terms used in the Laredo application.


## 1. Models

### 1.1 Model Name

-   A name to identify the model once processed.

### 1.2 Classification

-   A machine learning task that predicts a category or class of an instance.
    -   Example: predicting whether an email is spam or not.

### 1.3 Regression

-   A machine learning task that predicts a continuous value.
    -   Example: predicting the price of a house based on features such as size and location.


## 2. Data Types

-   Refers to the category of data (e.g., numeric, categorical) that is processed in machine learning models.


## 3. Preprocessing

### 3.1 MinMaxScaler

-   Scaler that adjusts the data to be within a specific range, usually [0, 1].

### 3.2 TargetEncoder

-   Method that encodes categorical variables based on the mean of the target.

### 3.3 Normalizer

-   Scales the data so that each instance has a unit norm (normalizes the vector).

### 3.4 StandardScaler

-   Scaler that adjusts the data to have a mean of 0 and a standard deviation of 1.

### 3.5 OneHotEncoder

-   Converts categorical variables into a binary representation (one per category).


## 4. Reduce Columns

### 4.1 SelectKBest

-   Method that selects the most relevant features based on a statistical test.

### 4.2 PCA (Principal Component Analysis)

-   Dimensionality reduction technique that transforms data into a lower-dimensional space while maintaining the most variability.


## 5. Fill Empty Rows

### 5.1 SimpleImputer

-   Method to fill missing values in the data, using strategies such as mean or median.

### 5.2 Ffill

-   Forward fill of missing values, using the previous value.

### 5.3 Bfill

-   Backward fill of missing values, using the next value.


## 6. Pipeline

-   A sequence of chained preprocessing and modeling steps, which allows applying all transformations and the model in an orderly and efficient manner.


## 7. Classification

### 7.1 Random Forest

-   A set of decision trees that makes predictions based on the vote of multiple trees.

### 7.2 Decision Tree

-   Algorithm that makes decisions by dividing the data into subgroups using feature-based rules.

### 7.3 Support Vector Machine (SVM)

-   Algorithm that seeks a hyperplane that separates classes in the best possible way.

### 7.4 K-Nearest Neighbors (KNN)

-   Classifier that assigns a class to a point based on the nearest classes in the feature space.


## 8. Regression

### 8.1 Random Forest

-   Similar to classification, but instead of classes, it predicts continuous values.

### 8.2 Decision Tree

-   Decision tree that predicts continuous values by dividing the data into subgroups.

### 8.3 Support Vector Regression (SVR)

-   Variant of SVM for predicting continuous values.

### 8.4 K-Nearest Neighbors (KNN)

-   Regression based on the values of nearby points.