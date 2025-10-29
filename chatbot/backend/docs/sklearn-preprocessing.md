# **What is preprocessing?**

Data preprocessing is the set of techniques and methods used to prepare and transform data before applying machine learning models or statistical analyses. The goal is to ensure that the data is in an appropriate, clean, and consistent format, allowing models to learn and make predictions efficiently and accurately. This process can include tasks such as normalizing values, removing incomplete or erroneous data, transforming categorical variables into numerical variables, and reducing the dimensionality of the data.

Proper preprocessing is crucial for obtaining good results from models, as poor quality or poorly formatted data can lead to erroneous conclusions or poor model performance.

# Min Max Scaler

## **Syntax**

```python
class sklearn.preprocessing.MinMaxScaler(
    feature_range=(0, 1), *, copy=True, clip=False)
```

## **Description**
**MinMaxScaler** is a preprocessing technique used to **scale** the features of the data, transforming them to a specific range, usually between 0 and 1. This method is useful when it is necessary for all features to have the same scale, such as in models that are sensitive to the magnitude of the variables, for example, in distance algorithms like KNN or neural networks.

## **Parameters:**

- **`feature_range`** (default: `(0, 1)`):  
    Specifies the range to which the data should be scaled. The default value is `(0, 1)`, but it can be changed to any other range, for example, `(-1, 1)`.

- **`copy`** (default: `True`):  
    Determines whether a copy of the data is created or if it is modified in place. If set to `True`, a copy of the input data is created, while if it is `False`, the data is modified directly.

- **`clip`** (default: `False`):  
    If set to `True`, any value outside the range specified by **feature_range** is clipped to the limits of that range. For example, if a feature value is 1.5 and the range is `(0, 1)`, it would be adjusted to the value 1.

## **Functioning:**
The **MinMaxScaler** works by calculating the **minimum value** and the **maximum value** of each feature in the data and then applying the formula for each value \( x \) of the feature.

This process ensures that all feature values are within the desired range, improving the model's ability to learn from the variables.

## **Common Uses:**
The **MinMaxScaler** is especially useful when features have different units or scales, such as in the case of data with measurements in meters and kilograms. Additionally, it is useful when using algorithms like **SVM**, **neural networks**, or **KMeans**, which depend on the distance between data points.

# Target encoding

**TargetEncoder** is a preprocessing technique used to **transform categorical features** into numerical values, using the relationship between those features and the target variable. Instead of simply assigning an arbitrary number to each category (as in One-Hot or Label Encoding), the **TargetEncoder** replaces each category with an average of the target value corresponding to that category. This can help capture patterns in the data and improve model performance in certain situations.

## **Parameters:**

- **`min_samples_leaf`** (default: 1):  
    Minimum number of samples that each category must have to be used in the calculation of the target mean. If a category has fewer than **`min_samples_leaf`** samples, its value is replaced by the global target mean, rather than the mean of that category.

- **`smoothing`** (default: 1.0):  
    Factor that controls the balance between the global target mean and the mean of each category. A higher **smoothing** value reduces the impact of specific category means and makes the **TargetEncoder** closer to the global mean, while a lower value increases the influence of specific category means.

- **`min_samples_split`** (default: 2):  
    Minimum number of samples that must be present in a group for the encoding to be performed. This parameter helps avoid overfitting by controlling how many samples of each category must be available for the calculation.

- **`max_iters`** (default: 100):  
    Maximum number of iterations allowed for the optimization algorithm used in the encoding process. This parameter controls how many times the means of each category are adjusted.

- **`random_state`** (default: `None`):  
    Seed for the random number generator, allowing for reproducibility of results.

- **`drop_invariant`** (default: `False`):  
    If set to **True**, automatically removes features that have no variance, i.e., those that have a single value in all samples.

## **Functioning:**

The **TargetEncoder** replaces each value of a categorical feature with the **mean of the target variable** for that category. However, to avoid overfitting or over-influence of categories with few samples, the mean value is smoothed using the **global mean** of the target variable and the **smoothing** parameter. This process helps to generalize better and avoid categories with few data having an excessive impact on the model.

## **Common Uses:**

The **TargetEncoder** is very useful when working with categorical variables that have a direct relationship with the target variable and is especially valuable in models that do not handle categorical variables well, such as **logistic regression**, **support vector machines (SVM)**, or **tree models**. Additionally, it is mainly used when there are categories with a low number of samples, making traditional encoding methods unsuitable.

This technique can improve performance in models that capture relationships between features and the target, although care must be taken with **overfitting**, as category means can be influenced by extreme values if adequate smoothing is not used.

# Normalizer

## **Syntax**

```python
class sklearn.preprocessing.Normalizer(norm='l2', *, copy=True)
```

## **Description**
The **Normalizer** is a preprocessing technique used to **normalize** data, adjusting the features of the data so that they have the same magnitude. Unlike other scaling methods that transform data to a specific range (such as MinMaxScaler), the **Normalizer** adjusts each row (sample) so that its norm (vector length) is equal to a specific value. This is useful, for example, when using distance-based models, such as **KNN** or **SVM**, where the magnitude of the samples should not influence the distance calculation.

## **Parameters:**

- **`norm`** (default: `'l2'`):  
    Specifies the norm to use for normalization. It can take the following values:
    - `'l2'`: Normalizes the data according to the L2 (Euclidean) norm, ensuring that the sum of the squares of the elements of each row is equal to 1.
    - `'l1'`: Normalizes the data according to the L1 norm, ensuring that the sum of the absolute values of the elements of each row is equal to 1.
    - `'max'`: Normalizes according to the infinity norm, ensuring that the maximum absolute value of each row is equal to 1.

- **`copy`** (default: `True`):  
    If set to **True**, a copy of the input data is made. If **False**, the input data is modified directly.

## **Functioning:**
The **Normalizer** transforms each row of the data so that its norm is equal to a specific value, depending on the selected norm.

## **Common Uses:**
The **Normalizer** is useful when working with data that represents vectors, such as in the case of texts (using vector representations like **TF-IDF** or **word embeddings**), images, or data representing high-dimensional features. By normalizing, it ensures that each sample has the same weight, regardless of the magnitude of its original values.

It is commonly used in models that depend on the **distance** between samples, such as **KNN**, **SVM**, and **neural network models**. This method is especially useful when samples have different scales and it is desired that all features contribute equally.

# StandardScaler

## **Syntax**

```python
class sklearn.preprocessing.StandardScaler(*, copy=True, with_mean=True, with_std=True)
```

## **Description**
**StandardScaler** is a preprocessing technique used to **scale** data, transforming features to have a mean of 0 and a standard deviation of 1. This transformation helps ensure that features are on the same scale, which can improve the performance of machine learning models, especially those sensitive to the magnitude of data, such as **linear models** or **SVM**.

## **Parameters:**

- **`copy`** (default: `True`):  
    If set to **True**, a copy of the input data is made. If **False**, the input data is modified directly.

- **`with_mean`** (default: `True`):  
    If **True**, the data is centered by subtracting the mean of each feature. That is, for each feature, the mean of the column is calculated and subtracted from each value in that column.

- **`with_std`** (default: `True`):  
    If **True**, the data is scaled by dividing by the standard deviation of each feature. This ensures that the data has a standard deviation of 1 after transformation.

## **Functioning:**
**StandardScaler** transforms each feature (column) of the data.

The result is that each feature will have a mean of 0 and a standard deviation of 1. If the **with_mean** parameter is **False**, the mean is not subtracted. If **with_std** is **False**, the data is not divided by the standard deviation.

## **Common Uses:**
**StandardScaler** is commonly used in models that assume data is normally distributed or in models that rely on distances or gradients. These models include:
- **Linear regression**,
- **Logistic regression**,
- **Support vector machines (SVM)**,
- **K-means clustering**,
- **Neural networks**.

When features have different units (e.g., one measures temperature in degrees Celsius and another measures distance in meters), normalization ensures that each feature contributes equally to the model, preventing some features from dominating others due to their larger values.

Using **StandardScaler** is especially important when using **distance-based algorithms** or **optimization algorithms** (such as gradient descent), as these methods can be affected if one feature has a larger magnitude than another.


# OneHotEncoder

## **Syntax**

```python
class sklearn.preprocessing.OneHotEncoder(
    categories='auto', drop=None, sparse_output=True, dtype=<class 'numpy.float64'>, handle_unknown='error', min_frequency=None, max_categories=None, feature_name_combiner='concat')
```

## **Description**
**OneHotEncoder** is a preprocessing technique used to **convert categorical variables** into a format that can be interpreted by machine learning algorithms. Since many machine learning models can only handle numerical data, this technique transforms categories into **binary vectors** (i.e., 0s and 1s). Each category in the original variable is represented as a new column, and in each row, only one of these columns has a value of 1, while the rest have values of 0.

## **Parameters:**

- **`categories`** (default: `'auto'`):  
    Defines which categories to use for encoding. If set to **'auto'**, the encoder will attempt to determine the unique categories from the data. If set to a list of lists, the categories for each feature can be specified manually.

- **`drop`** (default: `None`):  
    If specified, this parameter allows **dropping** one of the categories for each feature, reducing the total number of columns created by the encoder. If set to `'first'`, the first category is dropped; if set to `'if_binary'`, one column is dropped in binary variables.

- **`sparse_output`** (default: `True`):  
    If **True**, the encoder returns a sparse matrix (only stores non-zero elements, saving memory). If **False**, it returns a dense matrix, which includes all values, even those that are 0.

- **`dtype`** (default: `numpy.float64`):  
    Specifies the data type of the encoded result. It can be adjusted to another numeric type (such as `numpy.int32`), depending on memory or performance needs.

- **`handle_unknown`** (default: `'error'`):  
    Specifies how to handle categories that were not seen during the fitting (training) of the encoder. It can take the following values:
    - **'error'**: If an unknown category is encountered during prediction, an error is raised.
    - **'ignore'**: If an unknown category is encountered during prediction, the encoding for that category will be filled with zeros.

- **`min_frequency`** (default: `None`):  
    If set, it is used to remove infrequent categories, i.e., those whose frequency in the training data is less than the specified value.

- **`max_categories`** (default: `None`):  
    Limits the maximum number of categories to be encoded. If set, only the most frequent categories are kept, and the rest are grouped under an "other" category.

- **`feature_name_combiner`** (default: `'concat'`):  
    This parameter specifies how to combine feature names when performing transformations on categories. It can take the following values:
    - **'concat'**: Combines the original feature name with the category name.
    - **'named'**: Keeps the original feature name, with the category suffix.

## **Functioning:**
**OneHotEncoder** takes a categorical variable and converts it into a set of binary columns, where each column represents a possible category of the variable. For example, if we have a column with the values `["Red", "Green", "Blue"]`, OneHotEncoder will create three columns: one for "Red", one for "Green", and one for "Blue". If a row has the value "Red", its encoded representation will be `[1, 0, 0]`; if it has the value "Green", it will be `[0, 1, 0]`.

In this process:
- **'Red'** will be encoded as `[1, 0, 0]`,
- **'Green'** as `[0, 1, 0]`,
- **'Blue'** as `[0, 0, 1]`.

## **Common Uses:**
**OneHotEncoder** is commonly used in data preprocessing for machine learning models when there are **categorical variables** that do not have a logical order or cannot be interpreted as numbers. It is especially useful for models that cannot work directly with categorical data, such as **linear regression**, **decision trees**, **SVM**, among others.

This process allows the model to understand and use the information contained in categorical variables without losing the data structure, preventing the model from interpreting categories as numbers with order or hierarchy (e.g., we do not want "Red", "Green", and "Blue" to be interpreted as 1, 2, and 3).

# SelectKBest

## **Syntax**

```python
class sklearn.feature_selection.SelectKBest(
    score_func=<function f_classif>, *, k=10)
```

## **Description**
**SelectKBest** is a **feature selection** method used to choose the **best features** (or variables) from a dataset based on a specific scoring function. This process is crucial in selecting the most relevant variables for a machine learning model, which can help improve its performance and reduce overfitting by eliminating irrelevant variables.

## **Parameters:**

- **`score_func`** (default: `f_classif`):  
    Specifies the **scoring function** to be used to evaluate the relevance of the features. Several scoring functions are available:
    - **`f_classif`**: Uses the ANOVA F-test to compare the means of the groups in the features, suitable for classification problems.
    - **`f_regression`**: Uses Pearson correlation for the features, suitable for regression problems.
    - Other custom functions can also be defined to calculate the score based on a specific metric.

- **`k`** (default: `10`):  
    Determines the number of **features to select**. It can be set to an integer value to choose the `k` best features based on the obtained score. If set to **`'all'`**, all features will be selected, meaning no reduction will be performed.

## **Functioning:**
**SelectKBest** evaluates the importance of each feature in the dataset using the provided scoring function. It then selects the **`k` most relevant features** and retains them, eliminating the less important ones.

For example, if you have a dataset with 100 features, you can use **SelectKBest** with a scoring function and set **k=10** to select the 10 most relevant features for your model. This approach helps reduce the dimensionality of the dataset and thus improves the model's efficiency and performance.

## **Process:**
1. Calculate the score of each feature using the chosen scoring function (e.g., **ANOVA F** or **Pearson correlation**).
2. Rank the features based on their scores.
3. Select the `k` best features with the highest scores.

## **Common Uses:**
- **Dimensionality reduction**: When there are many features in the dataset, the model can become slower and prone to overfitting. **SelectKBest** selects only the most relevant features, reducing the amount of data and potentially improving the model's performance.
- **Improving accuracy**: By eliminating irrelevant or redundant features, the model can focus only on the most important features, enhancing its ability to generalize and make accurate predictions.
- **Preprocessing in complex models**: It is widely used in models like support vector machines, logistic regression, and neural networks to ensure that the model is trained only with the most important features.

## **Conclusion:**
**SelectKBest** is a powerful tool in feature selection that helps reduce dimensionality and improve the performance of machine learning models by ensuring that only the most relevant features are used for prediction.


# PCA

## **Syntax**

```python
class sklearn.decomposition.PCA(
    n_components=None, *, copy=True, whiten=False, svd_solver='auto', tol=0.0, iterated_power='auto', n_oversamples=10, power_iteration_normalizer='auto', random_state=None)
```

## **Description**
**PCA (Principal Component Analysis)** is a **dimensionality reduction** technique that aims to identify the principal components of a dataset. In other words, it reduces the number of features in a dataset while retaining as much information as possible. This can help improve model efficiency, eliminate redundancies, and facilitate data visualization.

## **Parameters:**

- **`n_components`** (default: `None`):  
    Specifies the number of **principal components** to retain after transformation. If set to an integer, that number of components will be retained. If set to a value between 0 and 1, enough components will be retained to explain that proportion of the total variance. If left as `None`, all components will be retained.

- **`copy`** (default: `True`):  
    If set to **True**, the input matrix `X` will be copied before performing the transformation. If set to **False**, the transformation will be performed in-place (modifying the input directly).

- **`whiten`** (default: `False`):  
    If **True**, the obtained principal components will be scaled to have unit variance. This can be useful if you want to ensure that the components are independent and have the same scale. However, this step can negatively affect performance in some cases.

- **`svd_solver`** (default: `'auto'`):  
    Specifies the method used to compute the singular value decomposition (SVD). Possible values are:
    - **`'auto'`**: Chooses the best available algorithm based on the size of the data.
    - **`'full'`**: Uses the full SVD, suitable for smaller datasets.
    - **`'arpack'`**: Uses the Arnoldi method for large and sparse matrices.
    - **`'randomized'`**: Faster approximation for large datasets.

- **`tol`** (default: `0.0`):  
    Specifies a tolerance threshold for singular values. A smaller value will consider more principal components, while a larger value will reduce the number of retained components.

- **`iterated_power`** (default: `'auto'`):  
    Determines the number of iterations in the power algorithm used in the SVD computation. This parameter only applies when using the **`'randomized'`** solver. A higher value can improve the approximation but also increases computation time.

- **`n_oversamples`** (default: `10`):  
    Used with the **`'randomized'`** solver and specifies the number of additional samples generated to improve the decomposition approximation.

- **`power_iteration_normalizer`** (default: `'auto'`):  
    Controls how the power iteration method is normalized. This can help improve the stability of the approximation when using the **`'randomized'`** solver.

- **`random_state`** (default: `None`):  
    Specifies the seed for the random number generator, allowing for reproducible results. If left as `None`, the global random number generator of Python will be used.

## **Functioning:**

**PCA** transforms a dataset into a new coordinate system, where the **first principal components** are the directions with the highest variance. The **principal components** are linear combinations of the original features of the dataset. By projecting the data onto these new axes, dimensionality is reduced without losing too much important information.

For example, if we have a dataset with many features, PCA will help identify the features that best describe the variability in the data and combine them to form new features (principal components), reducing the number of necessary dimensions.

## **Process:**

1. Calculate the **covariance matrix** of the data to see how the variables relate to each other.
2. Perform **singular value decomposition (SVD)** on the covariance matrix to identify the axes (components) of highest variance.
3. Select the **`n_components`** best principal components that represent the most variance in the data.
4. Project the original data onto the selected components, reducing dimensionality.

## **Common Uses:**

- **Dimensionality reduction**: In datasets with many features, PCA helps reduce the number of variables while retaining essential information, making models faster and more efficient.
- **Data visualization**: Often used to reduce data to 2 or 3 dimensions for plotting and visualizing complex patterns.
- **Preprocessing**: By eliminating redundant features, PCA can help improve the performance of machine learning models while decreasing the risk of overfitting.
- **Data compression**: In areas like image or audio processing, PCA can be used to reduce data size by retaining only the most important components.

## **Conclusion:**

**PCA** is a powerful and commonly used technique for **reducing the dimensionality** of data, facilitating analysis, visualization, and improving the performance of machine learning models by eliminating irrelevant or redundant features.


# SimpleImputer

## **Syntax**

```python
class sklearn.impute.SimpleImputer(*, missing_values=nan, strategy='mean', fill_value=None, copy=True, add_indicator=False, keep_empty_features=False)
```

## **Description**
**SimpleImputer** is a preprocessing technique used to **handle missing values** in a dataset. Instead of removing rows or columns with missing data, this method allows **filling in missing values** with a defined strategy, which can improve the quality of analysis and the efficiency of machine learning models.

## **Parameters:**

- **missing_values** (default: `nan`):  
    This parameter defines what value is considered as missing. The default value is **`nan`** (Not a Number), but it can be set to use other values, such as `None` or any other specific marker for missing data in a dataset.

- **strategy** (default: `'mean'`):  
    Specifies the strategy used to fill in the missing values. The most common options are:
    
    - **`'mean'`**: Fills in missing values with the **mean** of the column (for numerical data).
    - **`'median'`**: Fills in with the **median** of the column.
    - **`'most_frequent'`**: Fills in with the **most frequent** value (mode) of the column.
    - **`'constant'`**: Fills in with a **constant** value defined by the `fill_value` parameter.

- **fill_value** (default: `None`):  
    If the `'constant'` strategy is selected, this parameter specifies the constant value to be used to fill in the missing values. If `strategy` is not `'constant'`, this parameter is ignored.

- **copy** (default: `True`):  
    If set to **True**, the imputer will make a **copy** of the data before making any changes. If set to **False**, the imputation will be done directly on the original data, which can save memory but will also modify the data directly.

- **add_indicator** (default: `False`):  
    If set to **True**, a new binary column will be added for each feature with missing values. In this column, **1** indicates that the value was missing, and **0** indicates that the value was present.

- **keep_empty_features** (default: `False`):  
    If **True**, columns with all missing values will be kept in their original form (without imputing). If set to **False**, columns with all missing values will be discarded.

## **Functioning:**

**SimpleImputer** replaces missing values in a dataset with a value calculated according to the defined strategy. The process is carried out column by column, meaning each column can have a different imputation strategy, and it adjusts to the missing data based on the characteristics of each column (mean, median, etc.).

For example, in a dataset with numerical features, **SimpleImputer** can replace missing values with the mean of the column. For categorical data, it can use the mode or the most frequent value.

## **Common Uses:**

- **Handling missing data**: It is especially useful when working with datasets where missing values are common, as avoiding the removal of these data can improve model performance.
- **Preprocessing for machine learning models**: Many machine learning algorithms cannot handle missing data directly, so imputation is a crucial step in data preparation.

## **Considerations:**

- Imputing missing values can introduce **bias** in the data if the appropriate strategy is not chosen or if the amount of missing data is very large.
- Imputing data is not always the best option, especially if the missing values are random and not related to other data in the dataset.

## **Conclusion:**

**SimpleImputer** is a valuable tool in data preprocessing, as it allows **filling in missing values** in the data efficiently, without the need to remove entire rows or columns, preserving as much information as possible for analysis and the creation of machine learning models.


# Ffill

## **Forward Fill (ffill) - Imputation in Pandas**

**Forward Fill** (or **ffill**) is a technique used to handle missing values in time series or any dataset with an ordered structure. Instead of using a calculated statistic (such as mean or median), **Forward Fill** imputes missing values using the last known value in the column.

## **What is Forward Fill?**

**Forward Fill** (ffill) is an imputation technique that consists of replacing missing values (NaN) in a dataset with the nearest **previous** value in the column. It is a form of imputation that propagates valid data forward, filling in empty values with the last available observation.

## **When to use Forward Fill?**

This technique is mainly useful when working with time series or sequential data, where missing values can be **replaced** by the most recent value. It assumes that the previous value is a good approximation of the missing value in the context of those data.

For example, if we are working with a time series of daily sales and some days have missing data, we can assume that the sales for the missing day will be the same as the previous day (unless there are drastic changes).

## **Functioning:**

When **Forward Fill** is applied, missing values in a column are replaced by the last known (non-null) value in that same column. This process is carried out row by row.

## **Parameters of Forward Fill:**

The **ffill()** method in Pandas does not have many additional parameters, but there are options that can be useful in some situations:

- **axis:**  
    You can specify whether to apply **Forward Fill** along rows (`axis=0`, default) or along columns (`axis=1`).

- **limit:**  
    Allows setting a limit on the number of values that will be filled forward. For example, if `limit=1` is set, only one missing value will be filled with the previous value, even if there are more missing values.

## **Considerations:**

- **Forward Fill** is suitable when it is believed that the missing values are small measurement errors or when there is a **logical continuity** between values (for example, in temporal data where changes are not drastic between consecutive records).

- However, if the data is very sporadic or if there are large changes between records, **Forward Fill** could **introduce bias** into the model, as it assumes that values do not change much between two consecutive instances.

### **Conclusion:**

**Forward Fill** is a simple and effective technique for handling missing values in sequential or temporal data. By propagating the last valid value forward, it ensures that no information is lost, although it is important to ensure that this technique is suitable for the type of data being handled.


# Bfill

## **Backward Fill (bfill) - Imputation in Pandas**

**Backward Fill** (or **bfill**) is another technique used to handle missing values in time series or any dataset with an ordered structure. Unlike **Forward Fill**, **Backward Fill** imputes missing values using the next known value in the column, i.e., it fills missing values with the subsequent value.

## **What is Backward Fill?**

**Backward Fill** (bfill) is an imputation technique that consists of replacing missing values (NaN) in a dataset with the nearest **subsequent** value in the column. Unlike **Forward Fill**, which uses the previous value, **Backward Fill** uses the next value to fill the empty spaces.

## **When to use Backward Fill?**

**Backward Fill** is mainly used when it is believed that missing values can be appropriately replaced by the next available value in the data. This technique is useful in situations where missing values may reflect a pattern or context that is better approximated by the subsequent data rather than the previous ones.

## **Functioning:**

When **Backward Fill** is applied, missing values in a column are replaced by the next known (non-null) value in that same column. This process is carried out row by row, but instead of using the previous value as in **Forward Fill**, the next value is used.

## **Parameters of Backward Fill:**

The **bfill()** method in Pandas has some additional parameters:

- **``axis``:**  
    Similar to **Forward Fill**, you can specify whether to apply **Backward Fill** along rows (`axis=0`, default) or along columns (`axis=1`).

- **``limit``:**  
    Allows setting a limit on the number of values that will be filled backward. For example, if `limit=1` is set, only one missing value will be filled with the next value, even if there are more missing values.

## **Considerations:**

- **Backward Fill** is suitable when it is believed that the next value is a better approximation for the missing value, or when there is a closer relationship between subsequent values than previous ones.

- However, if the data is very sporadic or if the changes between consecutive records are significant, **Backward Fill** could introduce bias, as it assumes that the next value is representative of the missing value.

### **Conclusion:**

**Backward Fill** is a useful technique for handling missing values, especially when it is believed that subsequent values in the data are more appropriate for replacing the missing ones. Like **Forward Fill**, this technique should be applied with caution, as it assumes that subsequent values are representative of the missing ones. It is ideal for sequential or temporal data where future values can help fill gaps effectively.


# Important Definitions

Here is a better organization of important definitions about data preprocessing:

## Standardization
**Standardization** transforms data to have a mean of 0 and a standard deviation of 1. This is useful when data has different scales and needs to be brought to a common scale for certain models, such as those that depend on distances (e.g., KNN or PCA).

## Normalization
**Normalization** rescales data to be within a specific range, usually between 0 and 1. This is especially useful when working with models that require inputs in a specific range, such as neural networks or SVM with RBF kernel.

## Min-Max Scaling
**Min-Max Scaling** is a normalization technique that adjusts feature values within a specific range, usually between 0 and 1.

## Imputation
**Imputation** is the process of replacing missing values (NaN) in a dataset with estimated values. Common methods include replacing with the mean, median, or mode of the values present in the column, or using more advanced techniques like regression or machine learning algorithms.

## Feature Selection
**Feature Selection** is the process of choosing a subset of relevant features for a model, reducing dimensionality and eliminating noise. Common methods include **SelectKBest**, which selects the best \( k \) features based on a scoring criterion, and **Recursive Feature Elimination (RFE)**, which recursively eliminates features based on model performance.

## Dimensionality Reduction
**Dimensionality Reduction** aims to decrease the number of features in a dataset while retaining as much information as possible. Common techniques include:
- **PCA (Principal Component Analysis)**, which transforms features into principal components ordered by their explained variance.
- **t-SNE**, useful for visualizing high-dimensional data.

## One-Hot Encoding
**One-Hot Encoding** converts categorical variables into a binary format suitable for machine learning models. Each category of a feature is converted into a column with binary values (0 or 1), indicating the presence or absence of a category.

## Feature Scaling
**Feature Scaling** rescales features to have a common scale, which is especially important for algorithms like KNN or SVM that depend on distances between data points. This ensures that all features influence the model equally.

## Variable Categorization
**Variable Categorization** converts continuous variables into categories. This process can be done through **binning** or **quantiles**, where continuous values are divided into intervals or groups, and each group is represented as a category.

## Dummies
The term **dummies** refers to the binary variables created through **One-Hot Encoding**, where each category is represented as a column with values 0 or 1.

## Handle Unknown
In preprocessing, **handle unknown** refers to how to manage categories that were not seen during training but appear in the test data. Some encoding techniques, like **One-Hot Encoding**, allow setting a specific value to handle these cases.

## Mean Imputation
**Mean Imputation** replaces missing values in a feature with the average value of the present values in that column. This is a simple approach but may not always be suitable if the data has a skewed distribution.

## Median Imputation
**Median Imputation** replaces missing values with the median of the present values in the feature. It is useful when data has outliers or skewed distributions, as the median is not as affected by extreme values.

## Robust Scaler
A **Robust Scaler** uses robust statistics like the median and interquartile range instead of the mean and standard deviation, making it less sensitive to outliers. It is useful when data contains extreme values that could distort scaling.

## Polynomial Features
**Polynomial Features** create new features by raising existing ones to powers or multiplying them together, allowing capturing non-linear relationships between variables. This technique is used in regression or classification models to improve performance.

## Norm Scaling
**Norm Scaling** transforms data so that its norm (e.g., L2 norm) is equal to 1. It is useful when working with models that depend on the magnitude of feature vectors, such as distance-based classification methods.

This set of definitions covers the most common preprocessing methods in machine learning and explains how each is used to prepare data before training models.
