import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SmartCart - Customer Segmentation",
    page_icon="🛒",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("customer_segments.csv")


df = load_data()


# --------------------------------------------------
# CLUSTER NAMES
# --------------------------------------------------

cluster_names = {
    0: "Low Spending - Moderate Activity",
    1: "High Value - Multi-Channel Buyers",
    2: "Low Spending - Lower Activity",
    3: "High Value - High Response"
}


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🛒 SmartCart - Customer Segmentation")

st.subheader(
    "E-commerce Customer Segmentation using Agglomerative Clustering"
)

st.write(
    "An interactive dashboard for exploring customer segments "
    "generated using Agglomerative Clustering."
)

st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎯 Dashboard Filters")

clusters = sorted(df["cluster"].unique())

selected_cluster = st.sidebar.selectbox(
    "Select Customer Segment",
    ["All"] + clusters
)


if selected_cluster == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["cluster"] == selected_cluster]


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Customers",
        len(filtered_df)
    )

with col2:
    st.metric(
        "🔵 Clusters",
        df["cluster"].nunique()
    )

with col3:
    st.metric(
        "💰 Avg. Spending",
        f"₹{filtered_df['Total_Spending'].mean():,.0f}"
    )

with col4:
    st.metric(
        "💵 Avg. Income",
        f"₹{filtered_df['Income'].mean():,.0f}"
    )


st.divider()


# --------------------------------------------------
# CUSTOMER DISTRIBUTION
# --------------------------------------------------

st.header("📊 Customer Distribution")

cluster_counts = (
    df["cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

cluster_counts.columns = ["cluster", "customers"]

cluster_counts["Segment"] = cluster_counts["cluster"].map(
    lambda x: cluster_names.get(
        x,
        f"Cluster {x}"
    )
)

fig_distribution = px.bar(
    cluster_counts,
    x="Segment",
    y="customers",
    text="customers",
    title="Number of Customers in Each Segment"
)

fig_distribution.update_layout(
    xaxis_title="Customer Segment",
    yaxis_title="Number of Customers"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# --------------------------------------------------
# SPENDING & INCOME ANALYSIS
# --------------------------------------------------

st.header("💰 Customer Value Analysis")

col1, col2 = st.columns(2)


with col1:

    spending = (
        df.groupby("cluster")["Total_Spending"]
        .mean()
        .reset_index()
    )

    spending["Segment"] = spending["cluster"].map(
        lambda x: cluster_names.get(
            x,
            f"Cluster {x}"
        )
    )

    fig_spending = px.bar(
        spending,
        x="Segment",
        y="Total_Spending",
        text_auto=".0f",
        title="Average Spending by Segment"
    )

    fig_spending.update_layout(
        xaxis_title="Customer Segment",
        yaxis_title="Average Spending"
    )

    st.plotly_chart(
        fig_spending,
        use_container_width=True
    )


with col2:

    income = (
        df.groupby("cluster")["Income"]
        .mean()
        .reset_index()
    )

    income["Segment"] = income["cluster"].map(
        lambda x: cluster_names.get(
            x,
            f"Cluster {x}"
        )
    )

    fig_income = px.bar(
        income,
        x="Segment",
        y="Income",
        text_auto=".0f",
        title="Average Income by Segment"
    )

    fig_income.update_layout(
        xaxis_title="Customer Segment",
        yaxis_title="Average Income"
    )

    st.plotly_chart(
        fig_income,
        use_container_width=True
    )


# --------------------------------------------------
# PURCHASE BEHAVIOUR
# --------------------------------------------------

st.header("🛍️ Purchase Behaviour")

purchase_cols = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

available_purchase_cols = [
    col for col in purchase_cols
    if col in df.columns
]

if available_purchase_cols:

    purchase_summary = (
        df.groupby("cluster")[available_purchase_cols]
        .mean()
        .reset_index()
    )

    purchase_long = purchase_summary.melt(
        id_vars="cluster",
        var_name="Purchase Type",
        value_name="Average Purchases"
    )

    purchase_long["Segment"] = purchase_long["cluster"].map(
        lambda x: cluster_names.get(
            x,
            f"Cluster {x}"
        )
    )

    fig_purchase = px.bar(
        purchase_long,
        x="Segment",
        y="Average Purchases",
        color="Purchase Type",
        barmode="group",
        title="Average Purchase Behaviour"
    )

    st.plotly_chart(
        fig_purchase,
        use_container_width=True
    )


# --------------------------------------------------
# PCA VISUALIZATION
# --------------------------------------------------

if "PCA1" in df.columns and "PCA2" in df.columns:

    st.header("📈 Customer Segments Visualization")

    pca_df = df.copy()

    pca_df["Segment"] = pca_df["cluster"].map(
        lambda x: cluster_names.get(
            x,
            f"Cluster {x}"
        )
    )

    fig_pca = px.scatter(
        pca_df,
        x="PCA1",
        y="PCA2",
        color="Segment",
        hover_data=[
            "Income",
            "Total_Spending",
            "NumWebPurchases"
        ],
        title="Customer Segments in PCA Space"
    )

    fig_pca.update_layout(
        xaxis_title="PCA Component 1",
        yaxis_title="PCA Component 2"
    )

    st.plotly_chart(
        fig_pca,
        use_container_width=True
    )


# --------------------------------------------------
# CLUSTER PROFILE
# --------------------------------------------------

st.header("👥 Cluster Profiles")

summary_cols = [
    "Income",
    "Total_Spending",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumWebVisitsMonth",
    "Response",
    "Age"
]

available_summary_cols = [
    col for col in summary_cols
    if col in df.columns
]

summary = (
    df.groupby("cluster")[available_summary_cols]
    .mean()
    .round(2)
)

summary.insert(
    0,
    "Segment",
    summary.index.map(
        lambda x: cluster_names.get(
            x,
            f"Cluster {x}"
        )
    )
)

st.dataframe(
    summary,
    use_container_width=True
)


# --------------------------------------------------
# SELECTED SEGMENT INFORMATION
# --------------------------------------------------

if selected_cluster != "All":

    st.header("🔎 Selected Segment")

    segment_name = cluster_names.get(
        selected_cluster,
        f"Cluster {selected_cluster}"
    )

    st.subheader(segment_name)

    selected_data = df[
        df["cluster"] == selected_cluster
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Customers",
            len(selected_data)
        )

    with col2:
        st.metric(
            "Average Spending",
            f"₹{selected_data['Total_Spending'].mean():,.0f}"
        )

    with col3:
        st.metric(
            "Average Income",
            f"₹{selected_data['Income'].mean():,.0f}"
        )


# --------------------------------------------------
# CUSTOMER DATA
# --------------------------------------------------

st.header("📋 Customer Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)


# --------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Customer Data",
    data=csv_data,
    file_name="smartcart_customer_segments.csv",
    mime="text/csv"
)


# --------------------------------------------------
# ABOUT THE PROJECT
# --------------------------------------------------

st.divider()

st.header("ℹ️ About SmartCart")

st.write(
    """
    **SmartCart** is an e-commerce customer segmentation system.

    The project uses **Agglomerative Clustering** to group customers
    based on characteristics such as income, purchasing behaviour,
    spending, website activity and customer-related features.

    The dashboard allows users to explore the generated customer
    segments and compare their characteristics interactively.
    """
)

st.markdown(
    """
    **Machine Learning:** Agglomerative Clustering  
    **Linkage:** Ward  
    **Number of Clusters:** 4  
    **Dimensionality Reduction:** PCA  
    **Dashboard:** Streamlit  
    """
)