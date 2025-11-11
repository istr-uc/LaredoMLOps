# Frequently Asked Questions about the Laredo Application

This document answers the most common questions about using the Laredo application.

## Application Access

### How do I access the Laredo application?

1. Open your favorite web browser.
2. Enter the URL provided by the administrator.

### What do I do if I can't access the application?

Check the following:

- That the entered URL is correct.
- That you have an internet connection.
- If the problem persists, contact the administrator.

## Main Page and Models

### What options does the main page have?

From the main page, you can:

- Create a model to start the creation process.
- Explore available models to view and use already created models.

### How can I view the available models?

1. Click the **Show available models** button.
2. Review the table that shows:
    - Model name.
    - Version.
    - Creation date.
    - Representative image.

### What information is displayed when selecting a model?

When selecting a model, you will be able to see:

- Interactive pipeline that shows how the model was created.
- Evaluation metrics to review its performance.
- A button to deploy the model.

### How do I deploy a model?

1. Access the details of the desired model.
2. Click the **Deploy** button.
3. Follow the on-screen instructions.

## Model Creation and Configuration

### How do I start creating a model?

1. Click the **Create a model** button on the main page.
2. Complete the requested fields:
    - Model name.
    - Problem type from the dropdown menu.

### What do I do if an error message appears when creating a model?

Verify that:

- All required fields are completed.
- The entered values are valid.

### How do I upload a dataset?

1. Use the file explorer or drag and drop the file into the corresponding section.
2. Indicate if the file has a header.
3. Verify the dataset content in the preview table.

### How do I configure the dataset columns?

1. Select the data type for each column:
    - Integer, float, text string, or date.
2. Mark the target column for prediction.

### What do I do if I don't select a target column?

The system will display an error message requesting to configure it before continuing.

### What preprocessing methods are available?

You can:

- Delete irrelevant columns.
- Scale features.
- Encode categories.
- Fill in missing values.

### What happens if I misconfigure the preprocessing parameters?

The system will display an error message indicating which parameter is incorrect.

### How do I select an algorithm to train my model?

1. Select an algorithm based on the type of problem you solved.
2. Adjust the parameters if necessary.
3. Consult the help icons for more information.

### What do I do if the algorithm parameters are invalid?

The system will notify you with an error message. Adjust the values according to the suggestions provided.

## Model Training and Usage

### How do I start model training?

1. After configuring everything, click the button to start training.
2. Monitor progress through the loading animation.

### What do I do if model training fails?

Review:

- Dataset compatibility.
- Previous steps in the configuration.

### What do I do after training the model?

1. Review the performance metrics displayed in a table.
2. If the model is satisfactory, click **Finish** to save it.

### Can I modify a model after training it?

Yes, you can adjust parameters and retrain it if the metrics are not satisfactory.

### How do I use a saved model?

1. Use the API endpoints to make predictions.
2. Integrate the model with other tools as needed.

## Data Formats and Validation

### What file formats does Laredo accept for the dataset?

The application accepts files in CSV format.

### How do I verify if my dataset is correct?

1. Ensure it has the appropriate format (CSV).
2. Check that the dates are in year-month-day format.
3. Take care of the decimal notation (Spanish or English).
4. Make sure it contains a column with the label that you want to predict.

## Model Editing and Optimization

### How can I modify the parameters of a model after creating it?

1. Access the model from the model list.
2. Click the **Edit** button.
3. Change the desired parameters and save the changes.

### What happens if the trained model does not perform well?

If the model does not perform well, you can:

- Adjust the model parameters.
- Try another algorithm.
- Ensure the dataset is well preprocessed.
- Consider using another dataset if necessary.
- Change the model evaluation strategy (k-folds cross-validation, leave one out).

### Can I train multiple models at the same time?

No, you can currently only train one model at a time. However, you can start training another model once the current one has finished.

### How are trained models saved?

Trained models are automatically saved when you click **Finish** after training. You can find them in the **Saved Models** section.

### Can a model be deleted?

No, for now all models are saved for viewing.

### How can I view the metrics of a trained model?

The metrics are displayed in a table after completing model training. They include:

- Precision.
- Recall.
- F1 Score.
- Other metrics depending on the model type.

### Can I integrate the model with other platforms?

Yes, you can integrate your model using the APIs provided in the Laredo documentation.

### How does the model evaluation process work?

The evaluation process is performed automatically after training the model. The system calculates the performance metrics and displays them in a table, allowing you to see how well the model is performing.

### What happens if I upload a dataset with incomplete data?

If you upload a dataset with missing values, preprocessing techniques, such as filling in the missing values, can be used, depending on the selected configuration.

### Can I use a previously trained model to make predictions?

Yes, after training and saving a model, you can use it to make predictions through the API endpoints or through the system interface.

### Can I cancel an ongoing model training?

Yes, you can cancel model training at any time by clicking the **Cancel** button on the training interface.

### What do I do if the model takes too long to train?

If the model takes too long to train:

- Check that the dataset size is not excessive.
- Try to reduce the model complexity or use a smaller dataset.
- Remember that there are models with a large number of parameters that require more time to train.

### Does Laredo offer support for classification and regression models?

Yes, Laredo supports both types of models, classification and regression. Choose the problem type when creating the model and select the appropriate algorithm.

### What happens if I select an incompatible algorithm with my problem type?

If you select an incompatible algorithm, the system will display an error message indicating that you must choose another algorithm that is compatible with the selected problem type.
