
from langsmith import Client
from src.utils.key_manager import KeyManager

KeyManager()

example_inputs = [
## classification
("What is classification in machine learning?", 
 """Classification is a supervised machine learning task where a model learns to assign items to different categories or classes based on their features. To do this, the model is trained with a labeled dataset, meaning examples with their respective categories. Once trained, the model can predict the class of a new sample based on the learned patterns. Classification is applied in multiple areas, such as:

*   Spam detection (spam/not spam).
*   Image recognition (identification of objects or faces).
*   Medical diagnosis (classification of diseases based on symptoms)."""),

("What is a Random Forest Classifier?", 
 """-   It is a model based on decision trees.
-   It uses multiple trees trained with subsets of data.
-   It combines predictions to improve accuracy and reduce overfitting."""),

("What is the difference between `DecisionTreeClassifier` and `RandomForestClassifier`?", 
 """-   `DecisionTreeClassifier`: Uses a single tree, can overfit.
-   `RandomForestClassifier`: Uses multiple trees, reduces overfitting and improves accuracy."""),

("What is an `SVC` and how does it work?", 
 """-   `SVC` (Support Vector Classifier) uses Support Vector Machines (SVM).
-   It finds a hyperplane that separates categories with the largest margin.
-   It uses "kernels" for non-linearly separable data."""),

("What is decision tree pruning and how is it controlled?", 
 """-   Removes irrelevant branches to simplify the model.
-   Avoids overfitting.
-   Controlled by the `ccp_alpha` parameter.
-   `ccp_alpha`: sets how much impurity must be reduced in each split."""),

("What is the `class_weight` parameter used for in classifiers?", 
 """-   Adjusts class weights for imbalanced data.
-   `'balanced'`: adjusts weights based on class frequency."""),

# regression
("What is regression in supervised learning?", 
 """Regression is a type of supervised learning where a model learns to predict a numerical value instead of a category.

Unlike classification, where the goal is to assign labels like "cat" or "dog," regression aims to predict continuous values, such as:

*   The price of a house
*   Tomorrow's temperature
*   A person's monthly income

The regression model learns patterns from past data and uses them to make predictions on new data. This is done by fitting a mathematical function that best represents the relationship between the input variables (factors influencing the prediction) and the output variable (the value to be predicted).

For example, if we want to predict the price of a house based on its size, the regression model will identify how the size influences the price and create an equation that allows us to make predictions for new houses."""),

("What is a RandomForestRegressor?", 
 """-   Machine learning model that uses random forests.
-   Trains multiple decision trees and averages their predictions.
-   Improves model accuracy and stability."""),

("What is a DecisionTreeRegressor?", 
 """-   Regression model based on decision trees.
-   Divides data into subgroups and makes predictions based on input data"""),

("When is it appropriate to use KNeighborsRegressor?", 
 """-   When the exact form of the relationship between variables is unknown.
-   When non-linear relationships are complicated."""),

("What is R^2 and how is it interpreted?", 
 """-   R² (Coefficient of Determination): measures how well the model explains data variability.
-   1: model completely explains variability.
-   0: model explains nothing."""),

# preprocessing
("What is data preprocessing?", 
 """-   Set of techniques to prepare and transform data before applying machine learning models or statistical analysis.
-   Objective: ensure data is in an appropriate, clean, and coherent format."""),

(" When is `MinMaxScaler` useful?", 
 """-   Models sensitive to the magnitude of variables: KNN, neural networks, SVM, and KMeans."""),

("What is `Normalizer` used for?", 
 """-   Adjusts values of each row so its norm is 1.
-   Allows each sample to have the same magnitude.
-   Useful in distance-based models: KNN and SVM."""),

("What happens if a new category is not seen during `OneHotEncoder` training?", 
 """-   `handle_unknown='ignore'`: encodes the new category as a vector of zeros.
-   `handle_unknown='error'`: generates an error."""),

("Why is feature selection important?", 
 """-   Reduces overfitting.
-   Improves interpretability.
-   Speeds up models by removing irrelevant variables"""),

("How does `PCA` work?", 
 """-   Reduces dimensionality by finding linear combinations of original variables that maximize variance."""),

# user guide
("How do I configure the dataset columns?", 
 """1. Select the data type for each column:
    - Integer, float, text string, or date.
2. Mark the target column for prediction.
"""),

("What preprocessing methods are available?", 
 """You can:

- Delete irrelevant columns.
- Scale features.
- Encode categories.
- Fill in missing values."""),

("What do I do if model training fails?", 
 """Review:

- Dataset compatibility.
- Previous steps in the configuration."""),

("What file formats does Laredo accept for the dataset?", 
 """The application accepts files in CSV format."""),

("How do I verify if my dataset is correct?", 
 """1. Ensure it has the appropriate format (CSV).
2. Check that the dates are in year-month-day format.
3. Take care of the decimal notation (Spanish or English)."""),

("How can I view the metrics of a trained model?", 
 """The metrics are displayed in a table after completing model training. They include:

- Precision.
- Recall.
- F1 Score.
- Other metrics depending on the model type."""),

("What do I do if the model takes too long to train?", 
 """If the model takes too long to train:

- Check that the dataset size is not excessive.
- Try to reduce the model complexity or use a smaller dataset.
- Remember that there are models with a large number of parameters that require more time to train."""),

("What happens if I select an incompatible algorithm with my problem type?", 
 """If you select an incompatible algorithm, the system will display an error message indicating that you must choose another algorithm that is compatible with the selected problem type."""),
]

client = Client()
dataset_id = "2b731ede-7648-46eb-94e7-1c0971287606"

# Prepare inputs and outputs for bulk creation
inputs = [{"question": input_prompt} for input_prompt, _ in example_inputs]
outputs = [{"answer": output_answer} for _, output_answer in example_inputs]

client.create_examples(
  inputs=inputs,
  outputs=outputs,
  dataset_id=dataset_id,
)