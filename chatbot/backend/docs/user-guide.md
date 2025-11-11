# Guide to Using the Laredo Application

This guide describes step by step how to use the Laredo application effectively.


## 1. Accessing the Application

1.  Open your web browser of choice.
2.  Navigate to the Laredo application URL.


## 2. Initial Navigation and Main Functionalities

### 2.1 Main Page

Upon accessing the application, the main page will be displayed with the following main options:

-   **Create a model**: Allows the user to initiate the process of creating a new model.
-   **Explore available models**: Displays a list of already created models.

### 2.2 Key Interface Elements

Upon opening the tool, the user will first see a **prominent title** that says the name of the tool, "Laredo". Just below this title is a **subtitle** that briefly explains what the application is for.

In the central part of the page, there are **two buttons**. These buttons allow the user to access the main functionalities of the application. On the right side of the page, there is an image of a **robot**, purely decorative.

-   **Title**: "Laredo" (indicates the tool's name).
-   **Subtitle**: Briefly explains the application's function.
-   **Buttons**: Allow access to the main functionalities.
-   **Robot image**: Decorative element.


## 3. Exploring Available Models

### 3.1 Accessing the Model List

1.  Click the **Show available models** button.
2.  Explore the table with models organized by:
    -   Model name.
    -   Version.
    -   Creation date.
    -   Representative image.
3.  Click on a model to view its details.

### 3.2 Model Details

-   **Interactive pipeline**: Shows the model creation process.
-   **Evaluation metrics**: Presents information about the model's performance.
-   **Deployment button**: Allows putting the model into operation.

### 3.3 Deploying a Model

1.  On the model details page, click the **Deploy** button.
2.  Follow the additional instructions to complete the process.


## 4. Creating a New Model

### 4.1 Initiating Creation

1.  Click the **Create a model** button on the main page.
2.  Complete the following fields:
    -   **Model name**: Enter a descriptive name.
    -   **Problem type**: Select an option from the dropdown menu (classification, regression, etc.).

**Note**: If data is missing, an error message will be displayed.

### 4.2 Upload and Review the Dataset

1.  Upload your data file using:
    -   The file explorer.
    -   The drag and drop functionality.
2.  Specify if the file has a header.
3.  Verify the dataset content in the preview table.
4.  If the file is incorrect, reload the appropriate file.

### 4.3 Main Data Upload Functionalities

-   **Header selector**: Indicates if the dataset has headers.
-   **Preview**: Displays the first rows of the dataset in JSON format for validation.

### 4.4 Configuring Dataset Columns

1.  Select the data type for each column (integer, float, text string, date).
2.  Mark the target column for prediction.
3.  Ensure all columns are configured correctly.

**Note**: If a data type is not selected or the target column is not marked, an error message will be displayed.

### 4.5 Data Preprocessing

1.  Delete unwanted columns.
2.  Apply preprocessing methods such as:
    -   Feature scaling.
    -   Category encoding.
    -   Filling in missing values.
3.  Adjust the parameters of each method.

### 4.6 Preprocessing Tables

-   **Preprocessing methods**: Displays available methods, grouped by function. Depending on the category, only one preprocessing method may be selectable. Additionally, a help icon is provided for each preprocessing method.
    -   Feature Scaling and Encoding.
    -   Column Reduction.
    -   Filling Empty Rows.
-   **Preprocessing pipeline**: Displays the methods selected by the user.

### 4.7 Preprocessing Functionalities

Each method has its own **parameters** that the user can adjust. If the user makes an error in the parameters, an **error message** is displayed.
-   Column deletion.
-   Selection and configuration of preprocessing methods.
-   Error messages for incorrect configurations.

### 4.8 Algorithm Selection Mode

The user must **select the mode** of configuring the algorithm between easy and advanced. In **easy mode** the preprocessing, algorithm selection and evaluation is done **automatically** but the user has **less room for configuring and personalising** the paremeters and the training process **may take longer**. In **advanced mode** the preprocessing and model parameters are customisable but **requires a higher degree of understanding** from the user.

### 4.9 Algorithm Selection (Easy)

The user can run training directly or adjust some of the training paramentes. This parameters are:
- Preset: defines the level of predictive performance expected from the model. High level presets often requiere better hardware and more time to finish the training.
- Time limit: Defines a time limitation in seconds for the training process to make sure that the training of the models does not exceed the available time.
- Evaluation metric: Will be the main evaluation or scoring metric used to compare the different trained models and choose the better perfoming one. 

### 4.10 Algorithm Selection (Advanced)

The user must **select an algorithm** to train the model. Algorithms are grouped by the **type of problem** being solved. Each algorithm has a series of **parameters** that the user can modify. For each parameter, an **information icon** is displayed with a description and examples of values that can be entered.

1.  Choose an algorithm to train the model (advanced option).
2.  Modify the parameters as needed.
3.  Consult the parameter descriptions via the help icons.

In this option:
- The user must select an algorithm from those registered in the system for the previously chosen problem type.
- When the user specifies the algorithm, all its parameters are displayed along with their default values.
- If you want to change a parameter, you must set a **valid value**.

**Note**: If you enter invalid values, an error message will be displayed.

### 4.11 User Facilities in Algorithm Selection

-   **Information icon**: Description and examples of values for each parameter.
    -   It is displayed next to the input field where the user must enter the value.
    -   When you hover the mouse over the icon, a description of the parameter appears, in addition to the data type it accepts.
    -   If a parameter, for example, accepts the data type "String", the possible values are presented.

### 4.12 Model Training

Once the user has selected the algorithm, they can **start training** the model. While the model is training, the user will see a **progress animation**. The system also warns that the process can be **slow** and that, if preferred, the trained model can be consulted later.

1.  Start model training.
2.  Monitor progress via animation.
3.  Review metrics upon completion of training.

**Note**: If the model is not trained correctly, an **error message** is displayed indicating that something went wrong.

### 4.13 Common Training Errors

-   Dataset incompatibility.
-   Incorrect configurations in previous steps.

### 4.14 Model Saving and Usage

When training is complete, the user can see a **table with the trained model's metrics**. These metrics indicate how well the model has performed. If the model has not been satisfactory, the user can retrain it by changing some parameters. If satisfied, they can click the **"Finish"** button to complete the creation process.

1.  Save the trained model.
2.  Use the API endpoints to make predictions.

### 4.15 Model Evaluation

-   Review performance metrics in a summary table.
-   Adjust parameters and retrain if necessary.


## 5. Troubleshooting Tips

-   Ensure the file format is compatible (CSV, etc.).
-   Verify that all required fields are completed.
-   Contact technical support for persistent problems.
-   Check that the dates in the dataset are in the correct format.
-   Ensure the dataset file contains a target column.

Following this guide, you should be able to use the Laredo application efficiently.