"""
House Price Prediction: EDA & Model Training Script
===================================================
This script performs:
1. Data loading and exploration
2. Cleaning and validation
3. Exploratory data analysis with visualizations
4. Train/test split with feature scaling
5. Linear Regression model training
6. Evaluation (RMSE, R2) and coefficient interpretation
7. Example predictions vs actuals
8. Model and scaler serialization
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PATHS
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'housing.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
PLOTS_DIR = os.path.join(BASE_DIR, 'notebook', 'plots')

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

# Set plot style
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.2
})
sns.set_style('whitegrid')
PALETTE = ['#1B4332', '#B87333', '#D4A574', '#2D3436', '#5C8A4D']

print("=" * 60)
print("  HOUSE PRICE PREDICTION: EDA & MODEL TRAINING")
print("=" * 60)

# ============================================================
# 1. LOAD & EXPLORE
# ============================================================
print("\n[Loading] Loading dataset...")
df = pd.read_csv(DATA_PATH)

print(f"\n[Shape] Dataset Shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\n[Columns] Columns: {df.columns.tolist()}")
print(f"\n[Data Types] Data Types:\n{df.dtypes}")
print(f"\n[Missing] Missing Values:\n{df.isnull().sum()}")
print(f"\n[Stats] Basic Statistics:\n{df.describe().round(2)}")

# ============================================================
# 2. DATA CLEANING
# ============================================================
print("\n" + "=" * 60)
print("  DATA CLEANING")
print("=" * 60)

# Check for missing values
missing = df.isnull().sum()
if missing.sum() == 0:
    print("[Clean] No missing values found: no imputation needed.")
else:
    print(f"[Warning] Missing values found:\n{missing[missing > 0]}")
    # Drop rows with missing values
    df = df.dropna()
    print(f"   Dropped rows with missing values. New shape: {df.shape}")

# Check for duplicates
duplicates = df.duplicated().sum()
if duplicates > 0:
    print(f"[Warning] {duplicates} duplicate rows found: dropping them.")
    df = df.drop_duplicates()
    print(f"   New shape: {df.shape}")
else:
    print("[Clean] No duplicate rows found.")

# Check for outliers using IQR method
print("\n[Analysis] Outlier Analysis (IQR method):")
features = ['Area Income', 'Area House Age', 'Area No of Rooms', 
            'Area No of Bedrooms', 'Area Population']

for col in features:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = ((df[col] < lower) | (df[col] > upper)).sum()
    print(f"   {col}: {outliers} outliers (range: {lower:.1f} to {upper:.1f})")

# Decision: Keep outliers for Linear Regression since they're within realistic ranges
print("\n[Decision] Retaining outliers: they fall within realistic value ranges")
print("   and removing them from a 5,000-row dataset would reduce training data")
print("   without clear benefit for Linear Regression.")

# ============================================================
# 3. EXPLORATORY DATA ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("  EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# --- 3a. Correlation Heatmap ---
print("\n[EDA] Generating correlation heatmap...")
fig, ax = plt.subplots(figsize=(10, 8))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.3f', cmap='YlOrBr',
            linewidths=0.5, ax=ax, vmin=-1, vmax=1,
            square=True, cbar_kws={'shrink': 0.8})
ax.set_title('Feature Correlation Heatmap', fontweight='bold', pad=15)
plt.savefig(os.path.join(PLOTS_DIR, 'correlation_heatmap.png'))
plt.close()

print("   Correlation with Price:")
price_corr = corr['Price'].drop('Price').sort_values(ascending=False)
for feat, val in price_corr.items():
    strength = "strong" if abs(val) > 0.5 else "moderate" if abs(val) > 0.3 else "weak"
    print(f"   * {feat}: {val:.3f} ({strength})")

# --- 3b. Feature vs Price Scatterplots ---
print("\n[EDA] Generating scatterplots...")
scatter_features = ['Area Income', 'Area No of Rooms', 'Area Population']

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for i, feat in enumerate(scatter_features):
    axes[i].scatter(df[feat], df['Price'], alpha=0.3, color=PALETTE[i], s=10)
    axes[i].set_xlabel(feat)
    axes[i].set_ylabel('Price ($)')
    axes[i].set_title(f'{feat} vs Price', fontweight='bold')
    # Add trend line
    z = np.polyfit(df[feat], df['Price'], 1)
    p = np.poly1d(z)
    x_sorted = np.sort(df[feat])
    axes[i].plot(x_sorted, p(x_sorted), color='#B87333', linewidth=2, linestyle='--')

plt.suptitle('Feature vs Price Scatterplots', fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'scatterplots.png'))
plt.close()

print("   Interpretation:")
print("   * Area Income vs Price: Strong positive linear trend: higher area income")
print("     correlates clearly with higher house prices. This is the strongest predictor.")
print("   * Area No of Rooms vs Price: Moderate positive trend: more rooms generally")
print("     means higher prices, but with more scatter than income.")
print("   * Area Population vs Price: Weak/moderate positive trend: more populated areas")
print("     tend to have slightly higher prices, but the relationship is noisier.")

# --- 3c. Price Distribution ---
print("\n[EDA] Generating price distribution plot...")
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df['Price'], bins=50, color=PALETTE[0], edgecolor='white', alpha=0.85)
ax.axvline(df['Price'].mean(), color=PALETTE[1], linestyle='--', linewidth=2, 
           label=f"Mean: ${df['Price'].mean():,.0f}")
ax.axvline(df['Price'].median(), color=PALETTE[2], linestyle='--', linewidth=2,
           label=f"Median: ${df['Price'].median():,.0f}")
ax.set_xlabel('Price ($)')
ax.set_ylabel('Count')
ax.set_title('Distribution of House Prices', fontweight='bold')
ax.legend()
plt.savefig(os.path.join(PLOTS_DIR, 'price_distribution.png'))
plt.close()

print(f"   Price range: ${df['Price'].min():,.0f} to ${df['Price'].max():,.0f}")
print(f"   Mean price:  ${df['Price'].mean():,.0f}")
print(f"   Median price: ${df['Price'].median():,.0f}")
print(f"   The distribution is approximately normal (bell-shaped), which is")
print(f"   favorable for Linear Regression assumptions.")

# ============================================================
# 4. TRAIN/TEST SPLIT & SCALING
# ============================================================
print("\n" + "=" * 60)
print("  TRAIN/TEST SPLIT & FEATURE SCALING")
print("=" * 60)

X = df[features]
y = df['Price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"[Split] Train set: {X_train.shape[0]} samples")
print(f"[Split] Test set:  {X_test.shape[0]} samples")
print(f"   Split ratio: 80/20, random_state=42")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\n[Scaler] Features scaled with StandardScaler")
print(f"   Scaler fitted on training data only (no data leakage)")

# ============================================================
# 5. MODEL TRAINING
# ============================================================
print("\n" + "=" * 60)
print("  MODEL TRAINING: LINEAR REGRESSION")
print("=" * 60)

model = LinearRegression()
model.fit(X_train_scaled, y_train)

print("[Model] Linear Regression model trained successfully")

# ============================================================
# 6. EVALUATION
# ============================================================
print("\n" + "=" * 60)
print("  MODEL EVALUATION")
print("=" * 60)

y_pred = model.predict(X_test_scaled)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"\n   RMSE: ${rmse:,.2f}")
print(f"   R2 Score: {r2:.4f} ({r2*100:.1f}%)")
print(f"\n   The model explains {r2*100:.1f}% of the variance in house prices.")
print(f"   On average, predictions are off by about ${rmse:,.0f}.")

# Save metrics for later use
metrics = {'rmse': rmse, 'r2': r2}

# ============================================================
# 7. COEFFICIENT INTERPRETATION
# ============================================================
print("\n" + "=" * 60)
print("  COEFFICIENT INTERPRETATION")
print("=" * 60)

# For interpretation, train on unscaled data to get interpretable coefficients
model_unscaled = LinearRegression()
model_unscaled.fit(X_train, y_train)

print(f"\n   Intercept: ${model_unscaled.intercept_:,.2f}")
print(f"\n   Feature Coefficients (per unit increase in feature):\n")

coef_df = pd.DataFrame({
    'Feature': features,
    'Coefficient': model_unscaled.coef_,
    'Abs_Coefficient': np.abs(model_unscaled.coef_)
}).sort_values('Abs_Coefficient', ascending=False)

interpretations = {
    'Area Income': 'For every $1 increase in area income, the predicted house price increases by ${coef:,.2f}. This is the strongest predictor: wealthier neighborhoods have significantly higher home values.',
    'Area House Age': 'For every 1-year increase in average house age, the predicted price changes by ${coef:,.2f}. {direction}older areas tend to have {adj} prices, possibly reflecting established neighborhoods{caveat}.',
    'Area No of Rooms': 'For every additional room (on average), the predicted price changes by ${coef:,.2f}. More rooms = {adj} price, as expected.',
    'Area No of Bedrooms': 'For every additional bedroom (on average), the predicted price changes by ${coef:,.2f}. {note}',
    'Area Population': 'For every 1-person increase in area population, the predicted price changes by ${coef:,.2f}. Population has a {strength} effect on price per person, though the cumulative effect across large population differences can be meaningful.'
}

for _, row in coef_df.iterrows():
    feat = row['Feature']
    coef = row['Coefficient']
    print(f"   * {feat}: ${coef:,.2f}")
    
    if feat == 'Area Income':
        print(f"      -> {interpretations[feat].format(coef=coef)}")
    elif feat == 'Area House Age':
        direction = "" if coef > 0 else "counter-intuitively, "
        adj = "higher" if coef > 0 else "lower"
        caveat = "" if coef > 0 else " or reflecting depreciation"
        print(f"      -> {interpretations[feat].format(coef=coef, direction=direction, adj=adj, caveat=caveat)}")
    elif feat == 'Area No of Rooms':
        adj = "higher" if coef > 0 else "lower"
        print(f"      -> {interpretations[feat].format(coef=coef, adj=adj)}")
    elif feat == 'Area No of Bedrooms':
        note = "Interestingly, this has a negative coefficient, which may seem counter-intuitive. This likely reflects multicollinearity with 'Area No of Rooms': when controlling for total rooms, more bedrooms may mean fewer other room types (living areas, offices)." if coef < 0 else "More bedrooms directly increase predicted price."
        print(f"      -> {interpretations[feat].format(coef=coef, note=note)}")
    elif feat == 'Area Population':
        strength = "small" if abs(coef) < 20 else "moderate"
        print(f"      -> {interpretations[feat].format(coef=coef, strength=strength)}")
    print()

# Multicollinearity check
print("   * Multicollinearity Note:")
rooms_bedrooms_corr = df['Area No of Rooms'].corr(df['Area No of Bedrooms'])
print(f"      Rooms-Bedrooms correlation: {rooms_bedrooms_corr:.3f}")
if abs(rooms_bedrooms_corr) > 0.3:
    print(f"      These features are moderately correlated. The individual coefficients")
    print(f"      should be interpreted with caution: their effects partially overlap.")
else:
    print(f"      Correlation is low: multicollinearity is not a major concern here.")

# ============================================================
# 8. EXAMPLE PREDICTIONS
# ============================================================
print("\n" + "=" * 60)
print("  EXAMPLE PREDICTIONS vs ACTUALS")
print("=" * 60)

# Pick 5 samples from test set
sample_indices = np.random.RandomState(42).choice(len(y_test), 5, replace=False)
sample_X = X_test.iloc[sample_indices]
sample_y = y_test.iloc[sample_indices]
sample_X_scaled = X_test_scaled[sample_indices]
sample_pred = model.predict(sample_X_scaled)

print(f"\n   {'#':<4} {'Actual':>15} {'Predicted':>15} {'Error':>15} {'Error %':>10}")
print(f"   {'-'*4} {'-'*15} {'-'*15} {'-'*15} {'-'*10}")

for i, (actual, pred) in enumerate(zip(sample_y.values, sample_pred)):
    error = pred - actual
    pct = (error / actual) * 100
    print(f"   {i+1:<4} ${actual:>13,.0f} ${pred:>13,.0f} ${error:>13,.0f} {pct:>8.1f}%")

# ============================================================
# 9. SAVE MODEL & SCALER
# ============================================================
print("\n" + "=" * 60)
print("  SAVING MODEL & SCALER")
print("=" * 60)

model_path = os.path.join(MODEL_DIR, 'house_price_model.pkl')
scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')

joblib.dump(model, model_path)
joblib.dump(scaler, scaler_path)

print(f"Model saved to: {model_path}")
print(f"Scaler saved to: {scaler_path}")

# Also save metrics for README
metrics_path = os.path.join(MODEL_DIR, 'metrics.pkl')
joblib.dump(metrics, metrics_path)
print(f"Metrics saved to: {metrics_path}")

# Save feature names for the API
feature_names_path = os.path.join(MODEL_DIR, 'feature_names.pkl')
joblib.dump(features, feature_names_path)
print(f"Feature names saved to: {feature_names_path}")

print("\n" + "=" * 60)
print("  ALL DONE: Model ready for API deployment!")
print("=" * 60)
print(f"\n   Final Summary:")
print(f"   * Dataset: USA Housing (5,000 rows, 5 features + target)")
print(f"   * Model: Linear Regression")
print(f"   * RMSE: ${rmse:,.2f}")
print(f"   * R2: {r2:.4f} ({r2*100:.1f}%)")
print(f"   * Files saved: model, scaler, metrics, feature names")
