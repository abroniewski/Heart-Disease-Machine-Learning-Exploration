# Heart Disease Machine Learning Exploration

![Current Version](https://img.shields.io/badge/version-v1.0-blue)
![GitHub contributors](https://img.shields.io/github/contributors/abroniewski/IdleCompute-Data-Management-Architecture)
![GitHub stars](https://img.shields.io/github/stars/abroniewski/IdleCompute-Data-Management-Architecture?style=social)

## Table of contents

[](https://)

- [Getting Started](#getting-started)
- [Development](#development)
  - [Dataset Background](#dataset-background)
  - [Pre-processing](#pre-processing)
  - [Predictive Modeling](#predictive-modeling)
  - [Conclusions](#conclusions)
  - [Extensions and Limitations](#extensions-and-limitations)
- [Authors](#authors)
  - [Adam Broniewski](#adam-broniewski)
  - [Khushnur Binte](https://github.com/khushnur)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

The project was complete in 2022 as part of the Big Data Management and Analytics (BDMA) program for the Machine Learning course at Universitat Politecnic de Catalunya (UPC) in Barcelona.

**Are you a current BDMA student?** Don't be shy! [Reach out](mailto:abroniewski@gmail.com?subject=[GitHub]%20ML%20Project) for insights and tips!


The project is small and will follow the structure below:

```
Heart-Disease-Machine-Learning-Exploration
	├── README.md
	├── .gitignore
	└── src
		├── all executbale script files
	└── docs
		├── support documentation and project descriptions
	└── data
		├── raw
		└── processed
```

## Development

This project applies the machine learning techniques to a real-world dataset. The project covers all aspects of modeling methodology from preprocessing, exploratory data analysi to generating a final predictive model together with an assessment of its prediction quality.

The steps taken the complete the work include

1. Pre-processing
   * Reformatting
   * Encoding
   * Test and Train Data Split
   * Missing Values
   * Treating Outliers
2. Exploratory Data Analysis
   * Visualizations
   * Data CLustering
   * Feature Selection
3. Predictive Models
   * Parameter Tuning
   * Model Validation
     * with feature selection
     * without feature selection
   * Results Analysis and Model Selection
   * Final Model Estimated Performance
  
<img src="doc/Data Project Overview.jpg" width="500"/>

### Dataset Background

The goal of this project is to explore the [UCI - Heart Disease Data Set](https://archive.ics.uci.edu/ml/datasets/Heart+Disease) to discover trends in the data and predict whether a patient would have heart disease based on medical attributes.

The dataset has 303 instances and 14 attributes that are a combination of categorical and real values, which provides room for experimentation with different models and approaches to data pre-processing. There are also 61 other relevant papers that make use of this dataset as identified by UCI website.

### Pre-processing

#### Reformatting

The dataset column names were renamed from the originally abbreviated version to a full naming to make it more understandable during the exploratory phase.

#### Encoding

8 of the attributes are categorical and were encoded in the
original dataset with integer values. All the categorical variables originally
used label encoding. Nominal categorical variables (where no order exists) were
one-hot encoded to prevent models from applying an artificial ordering during
prediction. One-hot encoding was applied to:

* Sex
* Fasting blood sugar
* Exercise induced angina

Remaining categorical variables were deemed to be ordinal
and were not altered. This included:

* Chest pain type
* Resting electrocardiographic results
* Slope of the peak exercise ST segment
* Thalium stress result

The target variable was modified to only differentiate between "has heart disease" and "does not have heart disease". This was done by replacing the previously ordinal values of heart disease severity with “1” and no heart disease with “0”

#### Test and Train Data Set Split

The data set was split at the early stage of pre-processing to eliminate the risk of data leakage. All transformations to the training dataset will be applied to the test dataset independently. To test/train split is stratified to preserve that same proportion of target category examples as observed in the original data set.

It’s important to note that the only step of the process that could introduce data leakage is during scaling before the model is trained. This is mitigated with the use of a standard scaler made from the training data set.

#### Missing Values

The data set is quite clean, without missing values. 6 values in major vessel count and thalassemia were found with a “?”. Given the small number of missing values, the rows were dropped.

#### Outliers

To detect outliers, data that was outside of 150% of the interquartile range (1.5*IQR) was identified. Based on analysis, there were very few values that fell outside of the 1.5*IQR. Given box plot visualizations, only the cholesterol value above 450 was deemed to be noise and was removed from the dataset.

#### Visualizations and Interpretation

Boxplots show that the data is in different ranges and will need to be normalized before training models. It also clearly shows the categorical variables that were label encoded. Resting blood pressure appears right skewed, and max heart rate achieved appears left skewed. Although this skew would not impact tree-based models, we will apply a square root and square on the right and left skewed data respectively for our other models.

Figures show there are lots of individuals that had no ST depression induced by exercise (value of 0). We can explore to see if there is an issue in the data, and see the impact this attribute has on the target. This may be a good attribute to use for clustering individuals for a final predictive model.

ST depression induced by exercise is a measure of change in an ECG reading after exercise. Subjects with a "0" are subjects that did not have any ST depression, where subjects with a non-zero value had some ST depression present. Thus, the "0" values will not be removed and will be considered correct. It could be interesting to come back and bin the data into a "yes/no" categorical for use in model building.

Data also generally shows that males are more likely to have heart disease, however the data set is too small and there are much more instances in the data of males than females.

#### Feature Selection

Initial data exploration comparing numerical data against sex and the target category showed potential trends summarized in Figure 3‑6 below:

* age seems correlated with heart disease,
  especially with men
* higher max heart rate is associated with
  individuals without heart diseases
* cholesterol doesn't have a significant impact on
  heart disease
* when a participant had ST depression that is
  seen after exercise, they were more likely to suffer from heart disease

We can see from the correlations matrix that thalassemia looks to be well correlated with the target, and ST depression is correlated with peak exercise at ST slope. The cut-off for correlation in academic literature tends to range between 0.6 - 0.9. Based on this, there is not a strong case to remove any of the features.

For model testing, we will compare datasets where fasting blood sugar, cholesterol and resting blood pressure are removed to compare performance. These attributes do not show strong direct correlation to the target and may be introducing some noise in the predictions.

### Predictive Modeling

Functions are used to implement data cleaning and pre-processing identified during the EDA. Feature scaling will be completed by creating a transformation based on the training dataset for any train/test splits. This will ensure there is no data leakage, and that the way training and test data sets are treated is consistent. The models tested include:

* Logistic Regression
* Decision Tree
* Random Forest
* Neural Network

#### Parameter Choice

Each model is tested with various parameters. The models are built first using defaults, then with cross fold validation, and then applying hyper tuning. Models that require more computation time for hyper tuning (like random forest and neural net) are first tuned using a random search to approximate the correct parameters, followed by a full grid search to confirm them.

#### Feature Selection

Top scoring models that went through hyper parameter tuning were also run against a dataset that had feature selection applied, where three attributes were removed:

* Fasting blood-sugar
* Cholesterol
* Resting blood-pressure

These attributes were removed due to low correlation with the target as seen during the exploratory data analysis. Low correlation was evaluated during exploratory data analysis and confirmed with the correlation matrix (see 3.4 Feature Selection)

#### Validation Protocol

Validation of the selected model was completed using a stratified test/train split. 20% of the data (61 samples) were removed from the dataset to be used for a final test of the selected model. The remaining 80% of data (242 samples) were used for model testing, tuning and selection. The split was stratified on the target parameter to ensure that there was a representative number of samples in both the test and training datasets. The testing and training dataset respectively had 45.9% and 45.8% samples with heart disease present and were both representative.

During model validation, both test/split and k-Fold cross-validation were used. When test/train was used, the training dataset was again split into a subset of 20% and 80% respectively for testing and training respectively. Given the limited sample size, cross-validation was chosen as the final validation method. This provided more robust accuracy measures as each test/train split was completed multiple times and an average accuracy was provided as a result metric.

For logistic regression and decision tree models, a 10-fold cross-validation was used as it provided a good balance between computation time and accuracy. Given the relatively small size of the training data set a smaller test instance was not deemed reasonable as it would result in many similar iterations training the model. A 5-fold cross validation was used for random forest and neural network, driven primarily by computation time.

* Test/train split validation: 48 test, 194 train (single model validation)
* 5-fold cross validation: 48 test, 194 train (average of 5 models validation)
* 10-fold cross validation: 24 test, 218 train (average of 10 models validation)

#### Results

Each of the metrics was evaluated and considered when determining which model was the best choice. Given the potential impact of undiagnosed heart disease, specificity is an important metric, as we do not want to incorrectly classify an individual that has heart disease. Accuracy was deemed a good balance between true positives and true negatives.
The model chosen for use scored highest in all metrics considered: f-score, precision, recall and accuracy.

The neural network looked to perform well. Most surprisingly, the simple neural network with a single layer and single node operating on the full dataset did extremely well. The hyper tuned and simple neural network using the dataset with feature selection also ranked very well in comparison. Although neural network was performing well, the issue with using it as the final model introduced some issues in this field as the model would not be easily explainable and understandable by subject matter experts.

The hyper-tuned random forest model has a depth of 1 with 600 estimators. This is an unexpected result, but it means that each of the estimators is using a different attribute to predict the target.

The next best model was the logistic regression model with hyper tuned parameters trained on the dataset with feature selection applied. Since this model can be more easily understood and explained by professionals with semantic knowledge, this was the model that was chosen for final deployment.

#### Final Model Estimation and Performance

The final model was run using Logistic Regression with feature selection applied on the dataset. The F-score and accuracy metrics of the final model were very similar to the training accuracy. The precision of the final test was lower than the training model (78.1% vs 82.6%). The recall of the final model was higher than the training model (89.3% vs 82.6%). This means our model may have been a bit overfit for the data. The F-score does not reflect this change as it is taking an average of the other metrics.

Looking at the coefficients of the model, the major vessels count is the most important indicator of heart disease (coefficient=1.03). This makes sense with the semantic meaning of the data, as the attribute is a measure of the number of unobstructed blood vessels in the heart. Thalassemia (coefficient=0.77), chest pain type (coefficient=0.50), and sex (coefficient=0.26) were the next most important factors in predicting heart disease.

Using the linear regression model makes interpretation and explanation simple and can be used to help diagnosing physicians tune in and look at certain factors in their patients with more weight. The feature importance in this linear regression model is generally similar to the random forest feature importance, with some slight differences. It is not surprising that there is some difference as the models and parameters are different.

### Conclusions

Exploratory data analysis and predictive models were built for a heart disease dataset with 13 attributes and 303 instances. The data was generally clean (6 missing values) and need some adjustment to account for data skewness on continuous numerical values. There were trends seen in the impact of age, ST depression and max heart rate achieved during exercise on and individuals’ likelihood to have heart disease.

Decision tree, logistic regression, random forest, and neural networks were trained and tested with a variety of parameters. Additionally, high performing models were tested using a dataset with feature selection performed. The best performing model was a hyper tuned neural network with 8 hidden layers of size 3, however a logistic regression model with feature selection was chosen for the final implementation. The model had a precision of 78.1%, recall of 89.3% and accuracy of 83.6%.

Based on the trained model, the count of unobstructed major blood vessels is the most significant factor in predicting heart disease.

### Extensions and Limitations

A major limitation of this work was the limited size of the data set. Models were trained and tuned on ~250 instances, which increased the risk of over fitting or bias. Additionally, there was a significant difference in the amount of data from males and females. This could have been a result of how the study was conducted, or potentially a natural representation of the fraction of the population suffering from heart disease. In either case, the model for females would be improved if there was more data for them.

The use of 5-fold cross validation for neural net and random forest meant the model had fewer instances to use for training. This could have led to a model that was not well fit to the data. Using a different number of cross folds and monitoring performance with a convergence curve could help strike a balance between computation time and model performance.

Given the improvements of models with feature selection, as well as the potential improvements that could be gained in neural networks with fewer parameters, a future focus would be to continue tuning feature selection to improve model performance. The use of one-hot encoding on ordinal attributes would be interesting to explore, as the change in severity between steps of each label could be unequal.

Applying a programmatic manner for feature extraction would also be a good next focus. Feature selection can be done making use of the important features from the random forest model or using another method to identify the most important attributes and create a subset of data with those selected features.

Another natural extension of this work would be to apply an ensemble method to combine the performance of multiple models. This could allow the use of both logistic regression and neural networks to provide a model that can be generally understood and explained by experts using the coefficient weights, with additional tuning and boosting coming from a neural network to “tweak” the model.

## Authors

#### Adam Broniewski

* [GitHub](https://github.com/abroniewski)
* [LinkedIn](https://www.linkedin.com/in/abroniewski/)
* [Website](https://adambron.com)

#### Khushnur Binte Jahangir

* [GitHub](https://github.com/khushnur)

## License

`Heart-Disease-Machine-Learning-Exploration` is open source software [licensed as MIT](https://github.com/abroniewski/LICENSE.md).

## Acknowledgments

#### Bernat Coma-Puig

* [Google Scholar](https://scholar.google.es/citations?user=s3_djFwAAAAJ&hl=en)
