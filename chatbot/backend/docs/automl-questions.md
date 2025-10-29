# AutoML and AutoGluon: Questions and Answers

## What is AutoML?

- AutoML stands for Automated Machine Learning.
- It automates the process of applying machine learning to real-world problems.
- Tasks automated include data preprocessing, feature engineering, model selection, training, and hyperparameter tuning.
- Aimed at making ML accessible to non-experts while improving productivity for experts.

## Does Laredo support AutoML?

- Laredo applies AutoML when training models using the easy mode
- The AutoML framework used by Laredo is AutoGluon

## What is AutoGluon?

- AutoGluon is an open-source AutoML toolkit developed by AWS.
- It supports tabular data, text, image, and multimodal problems.
- Provides simple APIs for training and deploying machine learning models.
- Designed to work well with minimal user input and strong performance out-of-the-box.

## What AutoGluon tasks can Laredo handle?

- At the moment Laredo only includes support for tabular prediction (classification and regression).

## What is TabularPredictor?

- The main interface for training models on tabular data in AutoGluon.
- Takes care of:
  - Feature processing
  - Model training
  - Hyperparameter tuning
  - Ensembling
- Allows easy evaluation and prediction.

## What models does AutoGluon use?

- Uses a variety of models including:
  - LightGBM
  - CatBoost
  - XGBoost
  - Neural networks (PyTorch-based)
  - Random forests and extra trees
  - k-nearest neighbors
- Supports custom model integration via plugins.

## What is model ensembling in AutoGluon?

- Combines predictions from multiple models to improve accuracy.
- AutoGluon uses multi-layer stacking and bagging.
- Helps reduce overfitting and improve generalization.

## Can I customize the models AutoGluon uses?

- Yes, you can provide a list of models to include or exclude.
- You can also define hyperparameter search spaces.
- Example:

  ```python
  predictor = TabularPredictor(label='target').fit(
      train_data, 
      hyperparameters={'GBM': {}, 'RF': {}, 'NN_TORCH': {}}
  )
  ```
## How does AutoGluon handle missing data?

- Automatically detects and fills missing values.
- Chooses strategies based on data type and distribution.
- No need for manual imputation before training.

## Does AutoGluon support model interpretability?

- Yes, includes built-in SHAP-based feature importance.
- Use:

  ```python
  predictor.feature_importance(data)
  ```

- Helps identify key drivers in your predictions.

## What performance metrics does AutoGluon use?

- Automatically selects a metric based on the task:
  - Classification: accuracy, log-loss, F1 score, etc.
  - Regression: RMSE, MAE, R², etc.
- You can specify a custom evaluation metric.

## How does AutoGluon evaluate model performance?

- Uses cross-validation and hold-out validation to estimate generalization error.
- Evaluation metrics are logged for each model and ensemble.
- Leaderboard available using `predictor.leaderboard()`.

## How reliable are the models produced by AutoGluon?

- AutoGluon emphasizes robustness through:
  - Extensive model ensembling
  - Cross-validation
  - Automatic feature handling
- Models are generally competitive with hand-tuned pipelines.

## What algorithms does AutoGluon favor in practice?

- Gradient Boosted Trees (like LightGBM and CatBoost) often dominate for tabular data.
- Neural networks are also included and can be strong in high-dimensional or large datasets.
- Final ensemble typically includes the top models based on validation scores.

## How does AutoGluon choose the best model?

- Tracks validation performance during training.
- Models are ranked by a specified or default evaluation metric.
- Final predictions are made using the top-performing ensemble.

## Can I inspect the individual models in the ensemble?

- Yes, use:

  ```python
  predictor.get_model_names()
  ```

- You can also access:
  - Individual model scores
  - Model training times
  - Feature importances per model

## How does AutoGluon handle overfitting?

- Uses:
  - Cross-validation
  - Early stopping
  - Model ensembling
  - Bagging
- Encourages generalization rather than optimizing only for training data.

## How does AutoGluon compare to manual model tuning?

- AutoGluon matches or outperforms typical manual pipelines in many cases.
- Significantly faster for prototyping and baseline models.
- Manual tuning may still outperform in highly specialized domains or production-optimized systems.

## Can I trust AutoGluon’s results on small datasets?

- AutoGluon performs well even on small datasets due to its conservative training and ensembling.
- On very small data, simpler models or higher bias models (e.g., logistic regression) may be selected.
- Users can inspect model choices and adjust if needed.

## Is AutoGluon suitable for scientific or regulated applications?

- Supports transparency via feature importance and model inspection.
- However, users should still validate models using domain-specific knowledge.
- Regulatory compliance may require manual documentation beyond AutoGluon’s automatic logs.



