# **What is classification?**

**Classification** is a supervised machine learning task where a model learns to assign items to different categories or classes based on their features.

To do this, the model is trained with a labeled dataset, meaning examples with their respective categories. Once trained, the model can predict the class of a new sample based on the learned patterns.

Classification is applied in multiple areas, such as:
- **Spam detection** (spam/not spam).
- **Image recognition** (identification of objects or faces).
- **Medical diagnosis** (classification of diseases based on symptoms).

# **Random Forest Classifier**

## **Description**

The **`RandomForestClassifier`** is a machine learning model based on the **random forests** method. It works by training multiple decision trees and combining their predictions to improve accuracy and reduce the risk of overfitting.

Each tree is trained with a random sample of the data, and in the end, the model decides the classification of a new data point by taking the **majority vote** of all the trees.

## **Syntax**

```python
class sklearn.ensemble.RandomForestClassifier(
  n_estimators=100, criterion='gini', max_depth=None, min_samples_split=2, 
  min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='sqrt', 
  max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=True, 
  oob_score=False, n_jobs=None, random_state=None, verbose=0, 
  warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None, 
  monotonic_cst=None
)
```

## **Main Parameters**

### **1. Forest Control**
- **`n_estimators=100`**
  Number of trees in the forest. A higher value usually improves accuracy but also increases computation time.

- **`max_depth=None`**
  Maximum depth of each tree. If `None`, the trees grow until all leaves are pure or have very few data points.

- **`max_features='sqrt'`**
  Maximum number of features considered for each node split. Options:
  - `'sqrt'` (default): uses the square root of the total number of features.
  - `'log2'`: uses the logarithm base 2.
  - `None`: uses all features.

### **2. Node and Split Control**
- **`criterion='gini'`**
  Criterion for splitting nodes (`'gini'` or `'entropy'`).

- **`min_samples_split=2`**
  Minimum number of samples required to split a node. If the node has fewer data points than this value, it will not split.

- **`min_samples_leaf=1`**
  Minimum number of samples required in a leaf (final node of a tree). A higher value helps prevent overfitting.

### **3. Advanced Options**
- **`bootstrap=True`**
  Indicates whether to use *bootstrap sampling*, meaning the trees are trained with subsets of data selected with replacement. This improves the model's generalization.

- **`oob_score=False`**
  Evaluates the model with out-of-bag data (`True`/`False`).

- **`n_jobs=None`**
  Number of processors used in parallel to train the model. If `-1`, uses all available processors.

- **`random_state=None`**
  Seed for reproducibility of results.

- **`verbose=0`**
  Controls the amount of information printed during execution. If `0`, prints nothing; if higher, prints more details.

### **4. Fine-Tuning and Pruning**
- **`min_weight_fraction_leaf=0.0`**
  Minimum fraction of the total sample weight required in a leaf node. Useful when samples have unequal weights.

- **`max_leaf_nodes=None`**
  Maximum number of leaf nodes. If set, limits the growth of the trees.

- **`ccp_alpha=0.0`**
  Pruning parameter to reduce model complexity. Higher values remove irrelevant branches and simplify the model.

- **`max_samples=None`**
  Maximum number of samples used if `bootstrap=True`.

- **`min_impurity_decrease=0.0`**
  Minimum impurity decrease required to split a node.

- **`class_weight=None`**
  Assigns weights to classes to handle imbalanced data. Can be:
  - `None`: all classes have the same weight.
  - `'balanced'`: adjusts weights based on class frequencies.

- **`monotonic_cst=None`**
  Defines monotonic constraints on features, useful in applications like financial risk prediction.

## **Model Functioning**

1. `n_estimators` decision trees are generated, each trained with different subsets of data.
2. Each tree makes predictions independently.
3. The final classification is obtained by **majority vote** among all the trees.

This approach improves accuracy compared to a single decision tree and **reduces the risk of overfitting**.


# Decision Tree

## **Syntax**

```python
class sklearn.tree.DecisionTreeClassifier(
  criterion='gini', splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, class_weight=None, ccp_alpha=0.0, monotonic_cst=None
)
```

### **Explanation of `DecisionTreeClassifier` and its parameters**

The **`DecisionTreeClassifier`** from `scikit-learn` is a machine learning model based on decision trees. It works like a decision-making process: from the data, the model builds a tree with questions at each node that split the information until reaching a final classification.

For example, if we want to classify fruits, the tree might ask questions like *"Is it red?"* or *"Does it have a hard shell?"* until it reaches the correct answer, such as *"It's an apple"*.

### **Parameters and their explanation**

#### **1. Main Parameters**
- **`criterion='gini'`**  
  Measures the quality of a split in the tree. Options:  
  - `'gini'`: Uses the Gini index (measures the purity of the classes in a node).  
  - `'entropy'`: Uses entropy (related to information theory).

- **`splitter='best'`**  
  Controls how the split points are chosen at the nodes:  
  - `'best'` (default): selects the best split.  
  - `'random'`: chooses the split randomly, which can make the trees more diverse.

- **`max_depth=None`**  
  Maximum depth of the tree. If `None`, the tree grows until all leaves are pure or have very few data points.

- **`min_samples_split=2`**  
  Minimum number of samples required to split a node. A higher value prevents overfitting.

- **`min_samples_leaf=1`**  
  Minimum number of samples in a leaf (final node of the tree). Increasing this value prevents the creation of nodes with very few data points.

- **`max_features=None`**  
  Maximum number of features considered at each split. Options:  
  - `None`: uses all features.  
  - `'sqrt'`: uses the square root of the total number of features.  
  - `'log2'`: uses the logarithm base 2 of the total number of features.

#### **2. Advanced Parameters**
- **`random_state=None`**  
  Sets a seed for the random number generator, useful for obtaining reproducible results.

- **`max_leaf_nodes=None`**  
  Maximum number of leaf nodes in the tree. Limiting this can make the model simpler and prevent overfitting.

- **`min_impurity_decrease=0.0`**  
  A node will only split if the impurity decrease is greater than this value.

- **`min_weight_fraction_leaf=0.0`**  
  Minimum fraction of the total sample weight in a leaf node, useful if samples have different weights.

- **`class_weight=None`**  
  Adjusts the weights of the classes to handle imbalanced data. Options:  
  - `None`: all classes have the same weight.  
  - `'balanced'`: adjusts the weights based on class frequencies.

- **`ccp_alpha=0.0`**  
  Pruning parameter to simplify the tree. Higher values remove irrelevant branches and simplify the model.

- **`monotonic_cst=None`**  
  Allows defining monotonic constraints on features, useful in applications like financial risk prediction.


# SVC

## **Syntax**

```python
class sklearn.svm.SVC(
  C=1.0, kernel='rbf', degree=3, gamma='scale', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', break_ties=False, random_state=None)
```
### **Explanation of `SVC` (Support Vector Classifier) and its parameters**

The **`SVC`** (Support Vector Classifier) is a machine learning model based on **Support Vector Machines (SVM)**. It is used for classification and works by finding an **optimal hyperplane** that separates the data into different categories with the largest possible margin.

For example, if we want to classify emails as *spam* or *not spam*, `SVC` finds the best line (in 2D) or surface (in higher dimensions) that divides both categories. If the data is not directly separable, the model uses **mathematical tricks called "kernels"** to project them into a space where they can be separated.

### **Parameters and their explanation**

#### **1. Main Parameters**
- **`C=1.0`**  
  Controls the trade-off between accuracy and margin of separation:  
  - Low values (e.g., `C=0.1`) allow a larger margin, even if some points are misclassified.  
  - High values (e.g., `C=10`) force the model to classify most points correctly, but with a smaller margin (risk of overfitting).

- **`kernel='rbf'`**  
  Defines the function that transforms the data to make them separable. Options:  
  - `'linear'`: uses a linear separation.  
  - `'poly'`: applies a polynomial of degree `degree`.  
  - `'rbf'` (default): transforms the data non-linearly, useful for complex problems.  
  - `'sigmoid'`: uses the sigmoid function, similar to a neural network.

- **`gamma='scale'`**  
  Controls the influence of each point in the classification when using a non-linear kernel:  
  - `'scale'` (default): automatically adjusts based on the data.  
  - `'auto'`: uses `1/n_features`.  
  - Can also be a number (e.g., `gamma=0.1`) to manually define its effect.

#### **2. Advanced Parameters**
- **`shrinking=True`**  
  If `True`, uses a technique to speed up training without losing accuracy.

- **`probability=False`**  
  If `True`, allows obtaining probabilities in the classification (`.predict_proba()`). Enabling it increases training time.

- **`decision_function_shape='ovr'`**  
  Defines how to handle multi-class classification problems:  
  - `'ovr'` (One-vs-Rest, default): trains one classifier per class against the others.  
  - `'ovo'` (One-vs-One): trains classifiers for each pair of classes (better for small datasets).

# KNeighborsClassifier

## **Syntax**

```python
class sklearn.neighbors.KNeighborsClassifier(
  n_neighbors=5, *, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=None)
```

## **Explanation of `KNeighborsClassifier` and its parameters**

The **`KNeighborsClassifier`** is a classification model based on the **k-Nearest Neighbors (k-NN)** algorithm. It is a supervised learning method that classifies a new instance based on its **k nearest neighbors** within the training set.

For example, if we want to classify a point as a *dog* or *cat*, the algorithm will look for the **k closest points** in the training data and assign the most common class among them.

This model is intuitive and easy to implement, but it can become inefficient when the data volume is very large.

## **Parameters and their explanation**

### **1. Main Parameters**

- **`n_neighbors=5`**
  Defines how many close neighbors are considered for classification.
  - Low values (`n_neighbors=1`) can make the model very sensitive to noise.
  - High values (`n_neighbors=20`) smooth the classification but may lose precision in details.

- **`weights='uniform'`**
  Determines how neighbors are weighted:
  - `'uniform'` (default): all neighbors have the same weight.
  - `'distance'`: closer neighbors have more weight.
  - A custom function can also be defined.

- **`algorithm='auto'`**
  Defines the method to find the nearest neighbors:
  - `'auto'` (default): chooses the best algorithm based on the data.
  - `'ball_tree'`: uses tree structures for efficient searches.
  - `'kd_tree'`: another tree variant for fast searches.
  - `'brute'`: compares all distances directly (slower but useful for small data).

- **`leaf_size=30`**
  Only used if `algorithm='ball_tree'` or `algorithm='kd_tree'`. Affects search speed and memory usage.
  - Small values make the search more precise but slower.
  - Large values reduce memory usage but may lose precision.

### **2. Advanced Parameters**

- **`p=2`**
  Defines the distance used to find the nearest neighbors:
  - `p=1` → Manhattan distance (sum of absolute differences).
  - `p=2` → Euclidean distance (default, measures the straight line between points).
  - Other values can define custom metrics.

- **`metric='minkowski'`**
  Specifies the distance metric used:
  - `'minkowski'` (default): generalizes Manhattan and Euclidean with `p`.
  - Other metrics like `'cosine'`, `'hamming'`, or `'mahalanobis'` can be used.

- **`metric_params=None`**
  Allows passing additional parameters for some custom distance metrics.

- **`n_jobs=None`**
  Controls the number of processors used to calculate distances:
  - `None` → Uses a single core.
  - `-1` → Uses all available cores (speeds up calculations for large data volumes).

## **How does `KNeighborsClassifier` work?**

1. **Stores the training data**: Unlike other models, `k-NN` does not learn explicit rules but **stores** the data to compare with new instances.
2. **Calculates distances**: When it receives new data, it calculates its distance to all training points.
3. **Finds the `k` nearest neighbors**: Uses the defined distance metric (like Euclidean) to select the closest neighbors.
4. **Assigns the most common class**: The new instance receives the most frequent category among its neighbors.

## **When to use `KNeighborsClassifier`?**

- If the data has a clear and well-separated structure.
- If a **simple and no prior training** model is needed (the model only stores data).
- If the data is not too large, as `k-NN` can become **inefficient with large data volumes**.

- It is not recommended if there are too many features (dimensions), as distance calculation becomes less effective.

## **Comparison with other classifiers**

- **`DecisionTreeClassifier`**: Learns explicit rules, while `k-NN` only stores and compares data.
- **`RandomForestClassifier`**: More accurate and robust in complex problems but slower to train.
- **`SVC`**: Better for problems with non-linear boundaries but can be harder to optimize.

# General Concepts

## 1. Classification and Supervised Models

### Classification
A supervised learning task where a model assigns a label or category to a new instance based on previous data.

### Supervised Model
A model that learns from labeled examples, meaning data where the correct answer is already known.

## 2. Model Parameters and Tuning

### Hyperparameters
Model configurations set before training that affect its performance. Some examples include:
- Number of neighbors in `k-NN`.
- Depth in a decision tree.

### Bias-Variance Tradeoff
The balance between:
- **Variance**: A model that is too complex and overlearns.
- **Bias**: A model that is too simple and underlearns.

## 3. Problems in Learning Models

### Overfitting
Occurs when a model learns the training data too well, capturing noise instead of general patterns. It is recognized when the model performs well on training data but poorly on new data.

### Underfitting
Happens when the model is too simple and does not capture the real patterns in the data. This occurs when accuracy is low on both training and test data.

## 4. Data Representation

### Feature Space
The mathematical representation of data in multiple dimensions, where each dimension represents a feature of the dataset (e.g., weight and height in a classification of people).

# Algorithm-Specific Terms

## 1. Decision Tree Classifier

### Node
Decision point in the tree where the dataset is split according to a criterion (e.g., Is the person taller than 1.75 m?).

### Leaf
The last node of a branch in a decision tree that represents a final classification.

### Criterion (`criterion`)
Defines how data is split in a decision tree:
- `gini`: measures the purity of the nodes.
- `entropy`: uses information theory to split the nodes.

## 2. Random Forest Classifier

### Ensemble Learning
Technique that combines multiple models (like decision trees) to improve accuracy and stability.

### Bootstrap
Technique that selects random samples from the training data with replacement to train each tree in the random forest.

### OOB Score (Out-of-Bag Score)
Internal validation method in `RandomForestClassifier` that uses the samples not selected in the `bootstrap` to evaluate the model's performance.

## 3. Support Vector Classifier (SVC)

### SVM (Support Vector Machine)
Classification algorithm that finds the best line or hyperplane that separates the classes in the feature space.

### Margins
Areas around the hyperplane where the closest points define the separation of the classes.

### Kernel
Mathematical function that transforms data into a higher-dimensional space to facilitate class separation:
- `'linear'`: uses a straight line.
- `'rbf'`: transforms data to a higher dimension to improve separation.

## 4. K-Nearest Neighbors (k-NN)

### Neighbors (`n_neighbors`)
Number of closest points considered to determine the class of a new point.

### Distance Metric
Formula used to calculate how close two points are:
- **Euclidean Distance** (`p=2`): measures the straight-line distance.
- **Manhattan Distance** (`p=1`): sum of absolute differences in each dimension.

### Curse of Dimensionality
Phenomenon where **k-NN** and other distance-based algorithms become inefficient in high-dimensional spaces because all instances end up appearing equally distant.

