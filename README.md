# House Price Estimator

A web application that estimates regional house prices using Linear Regression. Built with scikit-learn for model training, FastAPI for the backend API, and a responsive vanilla HTML/CSS/JS frontend.

**Live Demo**: *Render link coming soon*

**Repository**: [github.com/yash5123/House_Price_Prediction](https://github.com/yash5123/House_Price_Prediction)

---

## Project Structure

```
House_Price_Prediction/
├── app/
│   ├── main.py            # FastAPI application and endpoints
│   ├── model_loader.py    # Singleton model loader
│   └── schema.py          # Pydantic request/response schemas
├── data/
│   └── housing.csv        # USA Housing dataset (5,000 records)
├── frontend/
│   ├── index.html         # User interface
│   ├── style.css          # Design system
│   └── script.js          # Form handling and API integration
├── model/
│   ├── house_price_model.pkl
│   ├── scaler.pkl
│   ├── feature_names.pkl
│   └── metrics.pkl
├── notebook/
│   ├── train_model.py     # EDA and training script
│   └── plots/             # Generated diagnostic charts
├── requirements.txt
└── README.md
```

---

## Exploratory Data Analysis

The training script performs a full analysis of the dataset before fitting the model. Below are the key findings.

### Correlation Heatmap

![Correlation Heatmap](notebook/plots/correlation_heatmap.png)

This heatmap shows the pairwise correlation between every feature and the target variable (Price).

* **Area Income** has the strongest correlation with Price at 0.640, making it the most influential predictor. Neighborhoods with higher average household incomes consistently have higher home values.
* **House Age** (0.452), **Number of Rooms** (0.336), and **Population** (0.408) show moderate positive correlations, meaning they contribute meaningfully but less dominantly.
* **Number of Bedrooms** has a weak correlation of 0.171. When paired with the total room count, additional bedrooms may indicate fewer non-bedroom spaces (offices, living areas), which explains the weak standalone signal.

### Feature vs Price Scatterplots

![Feature vs Price Scatterplots](notebook/plots/scatterplots.png)

These scatterplots visualize three key feature relationships individually, with dashed trendlines fitted by linear regression:

* **Area Income vs Price** (left): Tight, clearly linear upward trend. This validates income as the strongest single predictor. The data points cluster tightly around the trendline, indicating low residual variance for this feature alone.
* **Number of Rooms vs Price** (center): Positive relationship but with noticeably wider scatter. More rooms generally mean higher prices, but other factors (location quality, house age) add noise.
* **Area Population vs Price** (right): Weak positive trend with substantial scatter. Population alone is a poor predictor, but it adds marginal value when combined with the other features in the full regression.

### Price Distribution

![Price Distribution](notebook/plots/price_distribution.png)

The histogram of target home prices shows a near-symmetric bell curve centered around the mean ($1,232,073). The mean and median are close together, confirming the distribution is approximately normal. This is important because Linear Regression assumes normally distributed residuals, and a well-behaved target distribution supports that assumption.

---

## Model Performance

| Metric | Value |
|--------|-------|
| R2 Score | 0.918 (91.8% of variance explained) |
| RMSE | $100,444 |
| Algorithm | Linear Regression |
| Training Samples | 4,000 (80% split) |
| Test Samples | 1,000 (20% split) |
| Scaler | StandardScaler (fitted on training data only) |

The model explains 91.8% of the variance in house prices. On average, predictions deviate from the actual value by approximately $100,000, which is reasonable given the price range spans from roughly $15,000 to $2,470,000.

---

## API Endpoints

### Health Check
```
GET /health
```
Returns the server status and confirms the model is loaded.

### Predict Price
```
POST /predict
```
**Request body:**
```json
{
  "area_income": 68583.11,
  "area_house_age": 5.98,
  "area_no_of_rooms": 6.99,
  "area_no_of_bedrooms": 3.98,
  "area_population": 36163.52
}
```

**Response:**
```json
{
  "predicted_price": 1232072.65,
  "formatted_price": "$1,232,073",
  "confidence": "High: all inputs are within typical ranges"
}
```

---

## Local Setup

### Prerequisites
* Python 3.11+

### Installation
```bash
git clone https://github.com/yash5123/House_Price_Prediction.git
cd House_Price_Prediction
pip install -r requirements.txt
```

### Run the Server
```bash
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 in your browser.

### Re-train the Model (optional)
```bash
python notebook/train_model.py
```

---

## Tech Stack

* **Model**: scikit-learn LinearRegression + StandardScaler
* **Backend**: FastAPI, Uvicorn
* **Frontend**: HTML5, CSS3, JavaScript (no frameworks)
