# Problem Statement: Pneumonia Detection

## Business Context:

Pneumonia is one of the leading causes of morbidity and mortality worldwide, particularly affecting children under five years and elderly populations. According to the World Health Organization (WHO), pneumonia accounts for a significant percentage of deaths caused by infectious diseases. Early detection and timely treatment are critical to improving patient outcomes, yet current diagnostic methods present challenges.

The most common method for diagnosing pneumonia is through clinical evaluation combined with chest X-ray imaging. However, accurate interpretation of X-rays requires skilled radiologists, whose availability is limited in many regions, especially in rural or resource-constrained healthcare settings. Even when radiologists are available, factors such as fatigue, high patient load, and human error can affect the accuracy and consistency of diagnosis. This may lead to delayed treatment, misdiagnosis, or unnecessary use of antibiotics, worsening patient outcomes and straining healthcare systems.

With the advancement of machine learning and deep learning, automated image analysis has emerged as a promising solution to support medical imaging tasks. Leveraging large datasets of chest X-ray images, AI-driven approaches can be trained to recognize pneumonia-related abnormalities in the lungs with high accuracy and consistency. Such systems can serve as decision-support tools for healthcare professionals, reducing diagnostic workload, improving accuracy, and providing timely interventions, particularly in areas with limited medical expertise.

## Objective:

The main objective of this project is to develop an intelligent, automated system capable of detecting pneumonia from chest X-ray images using machine learning and deep learning techniques. The system should aim to:

1. **Accurately classify** chest X-ray images into pneumonia-positive and pneumonia-negative cases.
2. **Assist healthcare professionals** by providing a reliable second opinion that reduces diagnostic errors and variability.
3. **Improve efficiency** by delivering faster diagnoses, enabling timely treatment, and reducing the burden on radiologists.
4. **Enhance accessibility** by offering a scalable solution that can be deployed in hospitals, clinics, or rural healthcare centers with limited resources.
5. **Support global health efforts** by contributing to early detection, lowering pneumonia-related mortality rates, and optimizing antibiotic usage.

Ultimately, the solution aims to bridge the gap between limited medical expertise and growing healthcare demands, making pneumonia diagnosis more accurate, efficient, and accessible worldwide.

## Data Description:

In the dataset, some of the features are labeled “Not Normal No Lung Opacity”. This extra third class indicates that while pneumonia was determined not to be present, there was nonetheless some type of abnormality on the image and oftentimes this finding may mimic the appearance of true pneumonia. Dicom original images: - Medical images are stored in a special format called DICOM files (*.dcm). They contain a combination of header metadata as well as underlying raw image arrays for pixel data

## Evaluation Rubrics for Interim Report

| Section | Description | points | 
| ------- | ----------- | ------ |
| Data Overview | - Import the data - Check the shape of the data | 6 |
| Exploratory Data Analysis | - Plot random images from each class and print their corresponding labels - Check for class imbalance - Key meaningful observations from EDA | 8 |
| Data Preprocessing | - Convert the RGB images to Grayscale - Plot the images before and after the pre-processing steps - Split the data into train, validation and test - Apply the normalization | 10 |
| Model Building | - Define a CNN model from scratch - Train the Model - Check and comment on the performance of the model | 10 |
| Business Report Quality | - Adhere to the business report checklist | 6 |
| Total |  | 40 |

## Evaluation Rubrics for Final Report
| Section | Description | points | 
| ------- | ----------- | ------ |
| Data Overview | - Import the data - Check the shape of the data | 3 |
| Exploratory Data Analysis |- Plot random images from each class and print their corresponding labels - Check for class imbalance - Key meaningful observations from EDA | 3 |
| Data Preprocessing | - Convert the RGB images to Grayscale - Plot the images before and after the pre-processing steps - Split the data into train, validation and test - Apply the normalization | 4 |
| Model Building | - Define a CNN model from scratch | - Train the Model - Check and comment on the performance of the model | 5 |
| Transfer Learning | - Apply transfer learning using pre-trained CNN models (at least 2) - Check and comment on the performance of the models - Create new architectures using the above pre-trained CNNs and adding additional layers - Check and comment on the performance of the models - Compare and comment on the performance of all models built - Choose the best model with a proper rationale - Serialize the best model, re-load it, and make Inferences on a few images | 30 |
| Model Deployment | - Build a Streamlit or Gradio app where users can upload an image and see predicted class + probability. - Package app + model inside a Docker container for portability. - Deploy to a Hugging Face platform and make an inference | 5 |
| Actionable Insights and Recommendations | - Key takeaways for the business | 4 |
| Business Report Quality | - Adhere to the business report checklist | 6 |
| Total |  | 60 |
