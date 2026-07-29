# Advanced creation mode

This guide shows a detailed example of creating a model with the advanced creation mode for a credit card fraud detection case study.

## Example case study: credit card fraud detection

The example uses the Kaggle dataset "Credit card fraud detection dataset" to build a binary classification model that predicts whether a transaction is fraudulent.

This scenario is useful for advanced mode because it usually requires careful preprocessing, class imbalance handling, and model tuning.

### 1. Start a new project

Open the Laredo web interface and create a new project in Advanced mode.

- Select the Advanced creation mode.
- Choose the problem type as Classification.
- Name the project clearly, for example "credit-card-fraud-advanced".

=== "Home screen"

    ![Laredo home screen](assets/images/common/00-Home.png)

=== "Model creation"

    ![Model creation screen](assets/images/advanced/01-Model_creation.png)

### 2. Upload and validate the dataset

Upload the CSV file containing the credit card transaction data and review the detected columns.

- Confirm that the target column represents the fraud label.
- Review the dataset preview to verify that the transaction features and labels are loaded correctly.
- Check the inferred data types for the numeric and categorical columns.

=== "Upload"
    
    ![Dataset upload step](assets/images/common/02-Upload_dataset.png)

=== "Preview"

    ![Dataset preview](assets/images/common/03-Dataset_preview.png)

=== "Data types"
    
    ![Detected data types](assets/images/common/04-Data_types.png)

### 3. Configure a preprocessing pipeline

For a fraud detection use case, it is common to adjust the preprocessing pipeline to handle class imbalance and to prepare the transaction features for model training.

- Remove unneeded columns if necessary.
- Add preprocessing methods such as scaling or transformations.
- Combine the preprocessing steps into a pipeline that can be reused during training.

=== "Drop columns"

    ![Drop unnecessary columns](assets/images/advanced/05-Drop_cols.png)

=== "Preprocessing"

    ![Add preprocessing method](assets/images/advanced/06-Add_preprocessing_method.png)

=== "Pipeline"

    ![Preprocessing pipeline](assets/images/advanced/07-Preprocessing_pipeline.png)

### 4. Select the model and tune it

Choose the machine learning algorithm and configure the training parameters for the fraud classification task.

- Select a model family such as a tree-based classifier or another suitable algorithm.
- Tune the hyperparameters to balance sensitivity and precision.
- Start the training run and review the training progress.

=== "Algorithm"

    ![Configure the machine learning algorithm](assets/images/advanced/08_Configure_ml_algorithm.png)

=== "Training"

    ![Training in progress](assets/images/common/09_Training.png)

### 5. Review the evaluation and deploy the best model

After training, review the evaluation report and compare candidate models before deploying one.

- Inspect the evaluation metrics to assess fraud detection performance.
- Review the model details and version information.
- Deploy the selected version to make it available for inference.

=== "Evaluation"

    ![Evaluation results](assets/images/advanced/10-Evaluation.png)

=== "Models"

    ![Model list](assets/images/common/11_Model_list.png)

=== "Details"

    ![Model details](assets/images/advanced/12-Model_details.png)

=== "Details 2"

    ![Model details continued](assets/images/advanced/13-Model_details_2.png)

=== "Deploy"

    ![Deploy the model](assets/images/advanced/14-Deploy_model.png)

=== "Endpoints"

    ![Swagger endpoint view](assets/images/common/15-Swagger.png)

## When to use this mode

Choose Advanced mode when you need greater control over preprocessing, algorithm selection, and hyperparameter tuning, especially for complex tasks such as fraud detection, anomaly detection, or other imbalanced classification problems.
