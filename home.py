import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.set_page_config(page_title="Distribution Mixer", layout="wide")

st.title("📊 Distribution Shape & Central Tendency")
st.markdown("""
Adjust the populations below to see how mixing two groups affects the **Mean**, **Median**, and **Mode**.
Can you find a setup where the Mode sits between the Mean and Median?
""")

# --- Sidebar Controls ---
st.sidebar.header("Population 1 (The Base)")
m1 = st.sidebar.slider("Mean 1", 0, 100, 40)
s1 = st.sidebar.slider("Std Dev 1", 1, 30, 10)
n1 = st.sidebar.slider("Size 1", 100, 5000, 1000)

st.sidebar.header("Population 2 (The Challenger)")
m2 = st.sidebar.slider("Mean 2", 0, 100, 70)
s2 = st.sidebar.slider("Std Dev 2", 1, 30, 10)
n2 = st.sidebar.slider("Size 2", 10, 5000, 500)

# --- Data Generation ---
pop1 = np.random.normal(m1, s1, n1)
pop2 = np.random.normal(m2, s2, n2)
combined = np.concatenate([pop1, pop2])

# --- Calculations ---
mean_val = np.mean(combined)
median_val = np.median(combined)

# For continuous data, the "mode" is the peak of the KDE or a fine-grained histogram
# We'll use a histogram approach for clarity
counts, bins = np.histogram(combined, bins=100)
mode_val = bins[np.argmax(counts)]

# --- Visualization ---
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(combined, kde=True, color="skyblue", ax=ax, alpha=0.4)

# Lines for Central Tendency
ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
ax.axvline(median_val, color='green', linestyle=':', linewidth=2, label=f'Median: {median_val:.2f}')
ax.axvline(mode_val, color='blue', linestyle='-.', linewidth=2, label=f'Mode (Peak): {mode_val:.2f}')

ax.set_title("Combined Population Distribution")
ax.legend()

# --- Display Results ---
col1, col2 = st.columns([2, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.subheader("Stats Summary")
    st.write(f"**Mean:** {mean_val:.2f}")
    st.write(f"**Median:** {median_val:.2f}")
    st.write(f"**Mode:** {mode_val:.2f}")
    
    # Logic to show the order
    vals = {"Mean": mean_val, "Median": median_val, "Mode": mode_val}
    sorted_vals = sorted(vals.items(), key=lambda x: x[1])
    order_str = " < ".join([v[0] for v in sorted_vals])
    
    st.info(f"**Current Order:** \n\n {order_str}")
    
    if (median_val < mode_val < mean_val) or (mean_val < mode_val < median_val):
        st.success("🎯 You've trapped the Mode in the middle!")
    else:
        st.warning("The Median is currently in the middle (Standard Skew).")
