# **What is Regression?**

Regression is a type of supervised learning where a model learns to predict a numerical value instead of a category. Unlike classification, where the goal is to assign labels like "cat" or "dog," regression aims to predict continuous values, such as the price of a house, tomorrow's temperature, or a person's monthly income.

The regression model learns patterns from past data and uses them to make predictions on new data. This is done by fitting a mathematical function that best represents the relationship between the input variables (factors influencing the prediction) and the output variable (the value to be predicted).

For example, if we want to predict the price of a house based on its size, the regression model will identify how the size influences the price and create an equation that allows us to make predictions for new houses.


# Random Forest Regressor

## **Syntax**

```python
class sklearn.ensemble.RandomForestRegressor(
    n_estimators=100, *, criterion='squared_error', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=1.0, max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False, n_jobs=None, random_state=None, verbose=0, warm_start=False, ccp_alpha=0.0, max_samples=None, monotonic_cst=None)
```

## **Description**
The **`RandomForestRegressor`** from `scikit-learn` is a machine learning model based on the **random forests** method. It works by training multiple decision trees and combining their predictions to improve the model's accuracy and stability. Instead of classifying data into categories, like in a classifier, this model predicts numerical values (regression).

Each tree is trained on a random subset of the data, and to make a prediction, the model averages the predictions of all the trees, reducing variability and avoiding overfitting.

## **Parameters**

### **Main Parameters**

- **`n_estimators=100`**  
    Number of trees in the forest. More trees can improve accuracy but also increase training time.

- **`criterion='squared_error'`**  
    Metric used to measure the quality of a split in the tree nodes. `'squared_error'` minimizes the mean squared error (MSE), which favors more accurate predictions.

- **`max_depth=None`**  
    Maximum depth of each tree. If `None`, the trees will grow until all leaves are pure or contain very few data points. Limiting depth helps prevent overfitting.

- **`min_samples_split=2`**  
    Minimum number of samples required to split a node. A higher value produces simpler trees and reduces the risk of overfitting.

- **`min_samples_leaf=1`**  
    Minimum number of samples required in a leaf (end node). Higher values reduce model complexity.

- **`min_weight_fraction_leaf=0.0`**  
    Similar to `min_samples_leaf`, but in terms of the weight of the samples instead of the count.

- **`max_features=1.0`**  
    Maximum number of features considered for each split. Can be:  
    - A number (exact count of features).  
    - A percentage of the total (`1.0` uses all).  
    - `'sqrt'` (square root of the total number of features).  
    - `'log2'` (logarithm base 2 of the total features).

- **`max_leaf_nodes=None`**  
    Maximum number of leaves in the tree. Controls model complexity.

### **Fine-Tuning Parameters**

- **`min_impurity_decrease=0.0`**  
    A node will split only if the impurity decrease is greater than this value.

- **`bootstrap=True`**  
    If `True`, each tree is trained on a random sample of the dataset (with replacement). This improves model stability.

- **`oob_score=False`**  
    If `True`, uses out-of-bag samples to evaluate model performance.

- **`n_jobs=None`**  
    Number of CPU cores to use in parallel. `-1` uses all available cores.

- **`random_state=None`**  
    Controls randomness. If a fixed number is assigned, results will be reproducible.

- **`verbose=0`**  
    Level of detail in messages during training.

- **`warm_start=False`**  
    If `True`, reuses previous models to add more trees instead of training from scratch.

- **`ccp_alpha=0.0`**  
    Controls tree pruning. Higher values remove less relevant branches.

- **`max_samples=None`**  
    Maximum number of samples used to train each tree. If `None`, uses all available samples.

### **When to Use `RandomForestRegressor`?**

- When a robust and accurate regression model is needed.
- To avoid overfitting, as it combines multiple models into one.
- In problems where the relationship between variables is not completely linear.
- To handle data with missing values or noise, as it is less sensitive than other models.

This model is ideal for tasks like predicting house prices, product demand estimates, or any other problem requiring numerical value prediction.


# DecisionTreeRegressor

## **Syntax**

```python
class sklearn.tree.DecisionTreeRegressor(
    criterion='squared_error', splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, ccp_alpha=0.0, monotonic_cst=None)
```

## **Description**
The **`DecisionTreeRegressor`** from `scikit-learn` is a regression model based on decision trees. This model repeatedly splits the dataset into smaller subgroups based on the feature that best divides the data at each step. In the end, it makes a prediction about the target variable's value based on the input data's features. It is a flexible model that can handle non-linear relationships between variables.

## **Parameters**

### **Main Parameters**

- **`criterion='squared_error'`**  
    Metric used to measure the quality of the split in the tree nodes. `'squared_error'` minimizes the mean squared error (MSE), which helps obtain more accurate predictions.

- **`splitter='best'`**  
    Specifies the strategy to choose the split point at each node. `'best'` chooses the best split according to the criterion, while `'random'` selects a random split.

- **`max_depth=None`**  
    Maximum depth of the tree. If `None`, the tree will grow until all leaves are pure or contain very few data points. Limiting depth helps prevent overfitting.

- **`min_samples_split=2`**  
    Minimum number of samples required to split a node. If higher, the tree will be simpler, as fewer splits will be made.

- **`min_samples_leaf=1`**  
    Minimum number of samples required in a leaf (end node). A higher value leads to simpler trees with fewer decision nodes.

- **`min_weight_fraction_leaf=0.0`**  
    Similar to `min_samples_leaf`, but refers to the weight of the samples instead of their count. Used when data has weights associated with the samples.

- **`max_features=None`**  
    Maximum number of features to consider for each split. Can be an integer (exact number of features), a percentage of available features, or `'auto'`, `'sqrt'`, or `'log2'`, which are common settings.

- **`random_state=None`**  
    Controls the model's randomness. If a fixed value is specified, results will be reproducible, making it easier to compare models or experiment.

- **`max_leaf_nodes=None`**  
    Maximum number of leaves in the tree. If set, the tree will be pruned to limit the number of leaves, thus reducing complexity.

### **Fine-Tuning Parameters**

- **`min_impurity_decrease=0.0`**  
    A node will split only if the impurity reduction is greater than this value. This allows controlling the amount of splitting done in the tree and avoiding overfitting.

- **`ccp_alpha=0.0`**  
    Controls tree pruning. If set to a value greater than 0, less important branches are removed to avoid overfitting. This parameter is useful for simplifying the model.

- **`monotonic_cst=None`**  
    Allows specifying monotonic constraints for features. This ensures that predictions behave predictably, such as increasing or decreasing according to the features.

### **When to Use `DecisionTreeRegressor`?**

- When there is a non-linear relationship between input variables and the output, and an interpretable model is desired.
- For creating quick and simple predictions, as decision trees are easy to understand and visualize.
- For tasks where control over model complexity is needed, by adjusting parameters like `max_depth` and `min_samples_split`.
- When handling data with mixed types of features (categorical and continuous) or complex relationships.

This model is suitable for tasks like predicting house prices, income estimates, or any other type of numerical prediction based on input features.

# SVR

## **Syntax**

```python
class sklearn.svm.SVR(
    kernel='rbf', degree=3, gamma='scale', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1)
```

## **Description**

The **`SVR`** (Support Vector Regression) is a regression model based on the support vector machine (SVM) algorithm, which was originally designed for classification. Instead of finding a hyperplane that separates classes, as in classification, **SVR** seeks a "tolerance zone" where it tries to find a function that predicts continuous values while keeping errors within a specified margin.

In this model, the goal is to find a function that minimizes error while keeping the model as simple as possible. SVR is especially useful for problems where the data has non-linear behavior and there is a need to control the complexity of the model.

## **Main Parameters**

- **`kernel='rbf'`**  
    Specifies the type of kernel (transformation function) used to project the data into a higher-dimensional feature space. Common values are:  
    - `'linear'` (for a linear model),  
    - `'poly'` (for a polynomial model),  
    - `'rbf'` (radial basis function, which is common for SVR),  
    - `'sigmoid'` (sigmoid function).

- **`degree=3`**  
    This parameter is relevant only if the `'poly'` kernel is used. It defines the degree of the polynomial used for the transformation. A higher `degree` value makes the model more flexible but also more susceptible to overfitting.

- **`gamma='scale'`**  
    Controls the shape of the kernel function. `'scale'` uses `1 / (n_features * X.var())` for gamma calculation, which makes the model better adapt to the data. It can also be `'auto'`, which uses `1 / n_features`, or a specific numerical value that controls the influence of a single data point.

- **`coef0=0.0`**  
    This parameter controls the independent term in the kernel, only relevant for `'poly'` and `'sigmoid'` kernels. A higher `coef0` value makes the model more flexible in the shape of the function.

- **`tol=0.001`**  
    The tolerance value that controls the stopping criterion of the optimization process. When the change in the objective value is less than this threshold, the model stops. A smaller value makes the model take longer to train but be more precise.

- **`C=1.0`**  
    This parameter regulates the balance between minimizing error and model complexity. A higher `C` value penalizes errors more, which can make the model more accurate but also more susceptible to overfitting. A smaller `C` value favors a larger margin and more flexibility but may introduce more error.

- **`epsilon=0.1`**  
    Defines a "tolerance zone" where errors are not penalized. That is, if the predicted value is within this margin of the actual value, it is not considered an error. This parameter is useful for handling noise in the data.

- **`shrinking=True`**  
    If `True`, uses an optimization technique that speeds up the training process. If `False`, uses a more precise but slower method.

- **`cache_size=200`**  
    The size of the memory (in MB) used to store intermediate data during the training process. A larger value can speed up training but also consumes more memory.

- **`verbose=False`**  
    Determines whether the training process should print detailed messages. If `True`, the model shows more information about the training progress.

- **`max_iter=-1`**  
    The maximum number of iterations in the optimization process. If `-1`, there is no limit, and the process continues until convergence criteria are met.

### **When to Use `SVR`?**

- **SVR** is useful when the data has non-linear relationships and a regression function that is not too complex is desired.
- It is suitable when precise control over the error margin is needed, thanks to the `epsilon` parameter.
- It is used in tasks such as time series predictions, price estimates, or any other task where continuous values need to be predicted from independent variables.

**SVR** is especially effective when working with complex and non-linear data, as it efficiently handles a wide variety of relationships between input and output variables.


# KNeighborsRegressor

## **Syntax**

```python
class sklearn.neighbors.KNeighborsRegressor(
    n_neighbors=5, *, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=None)
```

## **Description**

The **`KNeighborsRegressor`** is a regression model based on the **k-nearest neighbors** (k-NN) algorithm, which predicts a continuous value for a new sample based on the mean (or similar weighting) of the values of its `k` nearest neighbors in the feature space. In other words, to make a prediction, it looks for the data points closest to the input and the model predicts the average value of those nearby samples.

This model is simple to understand and apply and is very useful when the relationships between variables are complex or non-linear but do not necessarily require a parametric model.

## **Parameters**

- **`n_neighbors=5`**  
    Specifies how many neighbors to consider when making the prediction. If the `k` value is small, the model can be more sensitive to noise in the data. A larger `k` value makes the model more robust but may lose precision if there is not enough differentiation between data points.

- **`weights='uniform'`**  
    Determines how neighbors are weighted when making the prediction. Possible values are:
    - `'uniform'`: All neighbors have the same weight, i.e., the mean of the values of the `k` nearest neighbors is used.
    - `'distance'`: Closer neighbors have more weight in the prediction, weighting according to the inverse of the distance. This allows closer points to influence the prediction more.

- **`algorithm='auto'`**  
    This parameter specifies the algorithm to use for finding the nearest neighbors. Possible values are:
    - `'auto'`: Automatically chooses the most efficient algorithm based on the data.
    - `'ball_tree'`: Uses the `BallTree` data structure, efficient for nearest neighbor queries in high-dimensional spaces.
    - `'kd_tree'`: Uses the `KDTree`, suitable for data with few attributes (dimensions).
    - `'brute'`: Performs a brute-force search.

- **`leaf_size=30`**  
    Controls the size of the leaves of the data structure used to store data points (when using `BallTree` or `KDTree`). A smaller value can increase precision but also increases computation time for finding the nearest neighbors. A larger value can make the model faster in searches but at the cost of precision.

- **`p=2`**  
    This parameter is used when calculating the distance between points. It specifies the type of distance to use. The most common value is `2`, which corresponds to the **Euclidean distance**, but other values can be used, such as `1` for the **Manhattan distance**.

- **`metric='minkowski'`**  
    Defines the metric used to calculate distances between points. `'minkowski'` is the most common, generalizing Euclidean and Manhattan distances. Custom or predefined metrics such as `'euclidean'` or `'manhattan'` can also be used.

- **`metric_params=None`**  
    Allows specifying additional parameters for the distance metric. In most cases, this value is not used, but if a custom metric is available, it can be passed through this parameter.

- **`n_jobs=None`**  
    Indicates the number of CPU cores to use during the calculation of the nearest neighbors. If `-1`, all available cores are used, speeding up the process for large data volumes.

### **When to Use `KNeighborsRegressor`?**

The **`KNeighborsRegressor`** is useful when there is a dataset that does not fit well into a parametric model or when the exact form of the relationship between variables is not known in advance. This model has several advantages:
- **Simplicity and flexibility**: It is easy to understand and apply.
- **No need for assumptions**: It does not require assuming a functional form of the relationship between variables.
- **Efficiency in non-linear relationships**: It works well with data where the relationships between features and the target value are non-linear.

However, it has some disadvantages:
- **Scalability**: Prediction time can be slow in large datasets, as it needs to calculate distances for each prediction point.
- **Sensitivity to noise**: The model is sensitive to noise in the data, especially if a small `k` value is used.

# General Concepts in Regression

## 1. Measurement and Evaluation Methods

### MSE (Mean Squared Error)
Measures the average difference between the values predicted by the model and the actual values, using the square of the differences. A lower value indicates better model accuracy.

- **R² (Coefficient of Determination):**  
    Measures how well a model explains the variability of the data. A value of 1 means the model fully explains the variability, while 0 indicates it explains nothing.

## **2. Model Phenomena:**

- **Overfitting:**  
    Occurs when the model fits too closely to the training data, negatively affecting its ability to generalize to new data.

- **Underfitting:**  
    Occurs when the model is too simple to capture the underlying relationships in the data, resulting in poor performance on both training and new data.

## **3. Model Methods and Parameters:**

- **Bootstrap:**  
    A technique in models like Random Forest, which creates subsets of the training data through sampling with replacement. Multiple models are used to improve overall accuracy.

- **Splitting Criterion:**  
    In decision trees, this is the criterion used to split nodes. For example, in **DecisionTreeRegressor**, **'squared_error'** is used to minimize the mean squared error at each split.

- **Regularization:**  
    A technique to prevent overfitting by penalizing model complexity. The **C** parameter in **SVR** controls the degree of regularization applied.

- **Feature Importance:**  
    In models like decision trees and Random Forest, it indicates how important each feature (variable) is for the prediction.

## **4. Techniques and Parameters of Specific Regressors:**

- **Distance (in KNeighborsRegressor):**  
    Neighbor models (KNeighborsRegressor) use distances, such as **Euclidean** or **Minkowski**, to determine the closeness of data points and, consequently, their influence on the prediction.

- **Kernel (in SVR):**  
    A function that transforms input data to facilitate the prediction of non-linear relationships. The **RBF (Radial Basis Function)** is the most commonly used kernel, but others like **polynomial** and **linear** also exist.

- **Gamma (in SVR):**  
    Controls the influence of each data point. A low **gamma** value implies a broader influence, while a high value means only nearby points impact the prediction.

- **Weights (in KNeighborsRegressor):**  
    Determines how neighbors influence the prediction. Parameters can be **'uniform'** (all neighbors have the same weight) or **'distance'** (closer neighbors have more weight).

## **5. Scaling and Preprocessing Concepts:**

- **Scaling:**  
    Some models, like **KNeighborsRegressor**, are sensitive to the scale of the data, meaning **normalization** or **scaling** of features may be necessary to improve performance.

- **Sampling:**  
    The process of selecting subsets of the training data. In **RandomForestRegressor**, **sampling with replacement** is performed to create different data subsets and train different trees.

## **6. Parameter Tuning and Optimization:**

- **Max Depth (in DecisionTreeRegressor):**  
    Controls the maximum depth of the tree. A higher value can lead to a more complex model prone to overfitting, while a lower value can cause underfitting.

- **Min Samples Split (in DecisionTreeRegressor):**  
    Sets the minimum number of samples required to split a node. Increasing it can make the tree more general and less prone to overfitting.

- **Min Samples Leaf (in DecisionTreeRegressor):**  
    Specifies the minimum number of samples required in a leaf node. A higher value can make the tree simpler and reduce the risk of overfitting.

- **Min Impurity Decrease (in DecisionTreeRegressor):**  
    Controls the minimum change in impurity required to make a split. A higher value leads to a simpler model.

## **7. Other General Parameters:**

- **Random State:**  
    A parameter that ensures the reproducibility of the model results. Setting a fixed value for this parameter allows obtaining the same results in each run.

- **Verbose:**  
    Determines whether detailed information about the model training process is displayed. A higher value generally provides more information about the fitting progress.
