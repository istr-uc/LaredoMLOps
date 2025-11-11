# Questions and Answers about Data Preprocessing in Scikit-Learn

## What is data preprocessing?

-   Set of techniques to prepare and transform data before applying machine learning models or statistical analysis.
-   Objective: ensure data is in an appropriate, clean, and coherent format.

## What does `MinMaxScaler` do?

-   Scales features to a specific range, by default 0 to 1.
-   Ensures all features have the same scale.

## When is `MinMaxScaler` useful?

-   Models sensitive to the magnitude of variables: KNN, neural networks, SVM, and KMeans.

## How does `TargetEncoder` work?

-   Replaces categorical values with the mean of the target for that category.
-   Uses smoothing to avoid overfitting.

## What is `Normalizer` used for?

-   Adjusts values of each row so its norm is 1.
-   Allows each sample to have the same magnitude.
-   Useful in distance-based models: KNN and SVM.

## What is the difference between `MinMaxScaler` and `StandardScaler`?

-   `MinMaxScaler`: scales values to a specific range (e.g., 0 to 1).
-   `StandardScaler`: adjusts values to have mean 0 and standard deviation 1.

## What is `StandardScaler` used for?

-   Models sensitive to data scale: logistic regression, SVM, neural networks, and clustering.

## How does `OneHotEncoder` work?

-   Converts categorical variables into binary columns.
-   Each category is represented with a 1 in a specific column.

## What happens if a new category is not seen during `OneHotEncoder` training?

-   `handle_unknown='ignore'`: encodes the new category as a vector of zeros.
-   `handle_unknown='error'`: generates an error.

## What is `SelectKBest` and what is it used for?

-   Selects the best `k` features based on a scoring function.
-   Reduces dimensionality and improves efficiency.

## How does `PCA` work?

-   Reduces dimensionality by finding linear combinations of original variables that maximize variance.

## What is the difference between `PCA` and `SelectKBest`?

-   `PCA`: transforms data into new orthogonal variables.
-   `SelectKBest`: selects the most relevant original variables without transforming them.

## How is missing data handled with `SimpleImputer`?

-   Fills missing values using strategies such as mean, median, mode, or a constant value.

## What is the difference between `ffill` and `bfill` in Pandas?

-   `ffill` (Forward Fill): replaces missing values with the last known previous value.
-   `bfill` (Backward Fill): replaces missing values with the next known value.

## What is the difference between normalization and standardization?

-   **Normalization**: rescales values within a specific range (e.g., 0 to 1).
-   **Standardization**: adjusts values to have mean 0 and standard deviation 1.

## What is Min-Max scaling?

-   Type of normalization that adjusts variable values within a range, generally 0 to 1.

## What is the function of `PolynomialFeatures`?

-   Generates new features by combining original ones through polynomials.
-   Allows capturing non-linear relationships.

## What is the risk of `TargetEncoder`?

-   Can overfit if proper smoothing is not used.
-   Means can be affected by extreme values.

## What is `RobustScaler` used for?

-   Scales data using median and interquartile range.
-   Less sensitive to outliers.

## How does `SimpleImputer` handle completely empty columns?

-   `keep_empty_features=False`: removes completely empty columns.
-   `True`: keeps columns without imputation.

## How is the number of components chosen in `PCA`?

-   Can be a fixed number or a percentage of total variance to retain.

## Why is feature selection important?

-   Reduces overfitting.
-   Improves interpretability.
-   Speeds up models by removing irrelevant variables.