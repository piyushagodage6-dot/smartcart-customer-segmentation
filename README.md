# 🛒 SmartCart - E-commerce Customer Segmentation

An interactive customer segmentation system that groups e-commerce customers based on their income, spending patterns, purchasing behaviour, website activity, and other customer characteristics.

The project uses **Agglomerative Clustering** to identify distinct customer segments and provides an interactive **Streamlit dashboard** for exploring the resulting segments.

## 🚀 Live Demo

👉 [Open SmartCart Live Demo](https://smartcart-customer-segmentation-jsv5dvfk5rgxf5ctoxtohf.streamlit.app/)

## 📌 Project Overview

Customer segmentation helps businesses understand different groups of customers and their purchasing behaviour.

In this project, customer data was cleaned, transformed, encoded, scaled, and reduced using PCA before applying **Agglomerative Clustering**.

The resulting customer segments are presented through an interactive Streamlit dashboard.

## 🎯 Objectives

- Segment customers based on their characteristics and purchasing behaviour
- Identify differences between customer groups
- Analyze spending and purchasing patterns across segments
- Visualize customer segments interactively
- Provide a simple dashboard for exploring the clustering results

## 🧠 Machine Learning Approach

### 1. Data Preprocessing

The dataset was prepared by:

- Handling missing values
- Feature engineering
- Encoding categorical features
- Scaling numerical features
- Removing selected irrelevant features

### 2. Feature Encoding

Categorical features such as:

- Education
- Living With

were transformed using **One-Hot Encoding**.

### 3. Dimensionality Reduction

**Principal Component Analysis (PCA)** was used to reduce the feature space to three principal components.

### 4. Clustering

**Agglomerative Clustering** was applied using:

- Number of clusters: **4**
- Linkage: **Ward**

The clustering was performed on the PCA-transformed data.

## 📊 Dashboard Features

The Streamlit dashboard provides:

- 👥 Customer distribution by segment
- 💰 Average spending analysis
- 💵 Average income analysis
- 🛍️ Purchase behaviour comparison
- 📈 PCA-based customer segment visualization
- 📋 Cluster profile summary
- 🔎 Interactive segment filtering
- 📥 Customer data download

## 🛠️ Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **Plotly**
- **Streamlit**
- **Jupyter Notebook**

## 📂 Project Structure

```text
smartcart-customer-segmentation/
│
├── app.py
├── customer_segments.csv
├── requirements.txt
└── README.md
