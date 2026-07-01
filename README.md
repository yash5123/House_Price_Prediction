<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=House%20Price%20Estimator&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Know%20what%20a%20home%20is%20worth%20before%20you%20even%20visit&descSize=16&descAlignY=55"/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&pause=1000&color=B87333&center=true&vCenter=true&width=600&lines=Trained+on+5%2C000+real+US+housing+records;Predicts+prices+in+under+200ms;91.8%25+accuracy+with+Linear+Regression;Clean+responsive+UI+with+no+frameworks;Built+with+FastAPI+%2B+scikit-learn)](https://git.io/typing-svg)

<br/>

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_Now-success?style=for-the-badge)](https://house-price-prediction-vhgo.onrender.com)
[![GitHub Repo](https://img.shields.io/badge/📦_Repository-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/yash5123/House_Price_Prediction)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

<br/>

*Enter a few neighborhood details. Get a home price estimate in seconds.*

</div>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" />

## 🎯 About

This is a full-stack house price estimator that takes in five simple neighborhood characteristics and returns a predicted home value, powered by a Linear Regression model trained on 5,000 real US housing records. No sign-ups, no API keys, no nonsense.

You type in numbers like average area income and house age, hit a button, and watch the price animate into view with an easing counter that genuinely feels satisfying. The model handles everything behind the scenes: scaling your inputs, running them through the trained regression, and even telling you how confident it is about the prediction.

The whole thing runs on a FastAPI backend that loads the model once at startup and never touches the disk again. The frontend is hand-crafted HTML, CSS, and JavaScript with a custom Forest Green + Warm Stone + Copper color palette that looks nothing like a default Bootstrap template.

> [!NOTE]
> The model achieves an **R² score of 0.918**, meaning it explains 91.8% of the variance in house prices. That is genuinely strong for a single linear regression with five features.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" />

## 🔄 How It Works

Here is the full journey from opening the app to getting your estimate:

1. 🖥️ **Open the app** — You land on a clean homepage with a hero section that immediately tells you what this does. No clutter, no popups.

2. ✏️ **Fill in five fields** — Average area income, house age, number of rooms, number of bedrooms, and area population. Each field has helper text so you know exactly what to enter.

3. 🔒 **Real-time validation kicks in** — Leave a field blank or type something out of range? The border turns red and a clear error message appears. The form will not submit until every field is valid.

4. 🖱️ **Hit "Estimate Price"** — The button disables, a copper spinner appears in the result card, and the text changes to "Computing the estimate..." while the API processes your request.

5. ⚙️ **Behind the scenes** — Your inputs are sent to the FastAPI backend, scaled using the same StandardScaler that was fitted during training, and passed through the Linear Regression model. The server also checks whether your inputs fall within typical training data ranges to assess confidence.

6. 💰 **The price animates in** — An easing counter rolls up from $0 to the predicted value over 1.2 seconds. A confidence badge (High, Moderate, or Low) appears below it. A note explains what the estimate is based on.

7. 🔄 **Start over** — Click "New Estimate" to reset everything and try different numbers.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" />

## ✨ Features

### 🏠 Core Prediction Engine

- 🔥 **Instant Price Estimation** — Enter five neighborhood metrics, get a dollar-value home price prediction within milliseconds. The model was trained on 5,000 data points and achieves 91.8% accuracy.

- 📊 **Confidence Assessment** — Every prediction comes with a confidence tag. The system checks each of your inputs against the typical ranges from the training data and flags when values are unusual. You get "High", "Moderate", or "Low" so you know how much to trust the number.

- 🧮 **StandardScaler Preprocessing** — Your raw inputs are normalized using the exact same scaler that was fitted on training data. This prevents data leakage and ensures the model sees inputs in the format it was trained on.

> [!TIP]
> The confidence system is not just a label. It actually loops through each feature, checks if it falls within the interquartile range of the training data, and counts how many fields are out of range. Zero out of range = High. One or two = Moderate. Three or more = Low.

### 🎨 UI & Experience

- 🎯 **Animated Price Counter** — The predicted price does not just appear. It counts up from zero using an `easeOutCubic` timing function over 1.2 seconds. It respects the user's `prefers-reduced-motion` system setting.

- ✅ **Field-Level Validation** — Every input is validated individually. Error messages are contextual ("Average Area Income is required", "Must be between 0 and 500,000"). Errors clear automatically as you type.

- 🌿 **Custom Design System** — Forest Green (#1B4332), Warm Stone (#D4A574), and Copper (#B87333) with DM Serif Display for headings and Inter for body text. No CSS framework. Every pixel is intentional.

- 📱 **Fully Responsive** — Works cleanly on desktop, tablet, and mobile. The two-column layout stacks to single-column on small screens, the sticky result card becomes static, and font sizes scale with `clamp()`.

- 📈 **SVG Regression Chart** — The "How it Works" section includes a hand-crafted SVG scatter plot with training data points and a regression trendline, visually explaining what the model is doing.

### ⚡ Backend & API

- 🚀 **Singleton Model Loading** — The model, scaler, and feature names are loaded exactly once at server startup via FastAPI's lifespan context manager. Every subsequent request reads from memory. Zero redundant disk I/O.

- 🛡️ **Pydantic Schema Validation** — Every request is validated against strict Pydantic schemas with min/max constraints before it ever reaches the model. Bad input gets a clean 422 response with human-readable error messages.

- 🌐 **Global Error Handler** — Unhandled exceptions never leak raw stack traces to the client. A catch-all returns clean JSON with a generic message.

- 📄 **Auto-Generated API Docs** — FastAPI provides Swagger UI at `/docs` out of the box. Every endpoint is documented with examples, descriptions, and response models.

> [!TIP]
> The API is designed so the frontend can be served directly by FastAPI via `StaticFiles`, but also works standalone if opened as a local HTML file — it detects `file://` origins and falls back to `localhost:8000`.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" />

## 💡 Who Can Use This?

| 👤 Who | 🎯 What they do with it |
|--------|------------------------|
| 🎓 ML Students | Study a complete end-to-end regression pipeline: data → EDA → training → API → frontend |
| 🏡 Curious Homeowners | Plug in their neighborhood stats and see what the model thinks their area is worth |
| 📚 Data Science Learners | See how StandardScaler, train/test splits, and coefficient interpretation work in practice |
| 👨‍🏫 Teachers & Professors | Use it as a classroom demo for supervised learning and web deployment |
| 💼 Portfolio Builders | Fork it, swap the dataset, retrain, and have a polished full-stack ML project in minutes |
| 🔍 Real Estate Curious | Compare different neighborhood profiles side by side to see what drives home prices |

> [!IMPORTANT]
> **For ML students**: This project does not skip steps. The training script includes full EDA with correlation heatmaps, scatter plots with trendlines, price distribution analysis, outlier detection via IQR, multicollinearity checks, and coefficient interpretation on unscaled data. Every decision is explained in the terminal output.

> [!TIP]
> **For portfolio builders**: The project is structured exactly how a production ML app should be — separated model training, singleton loader, schema validation, and a frontend that talks to a real API. It is not a Jupyter notebook with a `predict()` call at the bottom.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" />

## 🛠️ Built With

| Technology | What it does in this project |
|---|---|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | The backbone — runs the training script, the API server, and all data processing |
| ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) | Trains the LinearRegression model and fits the StandardScaler on training data |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) | Serves the prediction API with automatic validation, docs, and CORS handling |
| ![Uvicorn](https://img.shields.io/badge/Uvicorn-2D6A4F?style=for-the-badge) | ASGI server that runs FastAPI in production with async support |
| ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) | Loads, explores, and cleans the 5,000-row housing dataset |
| ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white) | Handles feature arrays and numerical operations during prediction |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge) | Generates all EDA plots — heatmaps, scatter plots, histograms |
| ![Seaborn](https://img.shields.io/badge/Seaborn-43AA8B?style=for-the-badge) | Adds statistical styling and the correlation heatmap visualization |
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | Semantic page structure with accessible form inputs and ARIA labels |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) | Custom design system with CSS variables, responsive grid, and micro-animations |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) | Handles form validation, API calls, state management, and the animated price counter |

The stack was chosen deliberately: scikit-learn for a clean, interpretable model. FastAPI because it auto-generates docs and validates inputs with zero extra code. Vanilla frontend because this project does not need 200KB of React to render five input fields.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" />

## 📸 Model Training Visualizations

These plots are generated automatically when you run the training script. They live in `notebook/plots/`.

<div align="center">

### Correlation Heatmap
<img src="notebook/plots/correlation_heatmap.png" width="80%" />

*<sub>Area Income dominates with a 0.640 correlation to Price. Bedrooms show a weak 0.171 — likely due to multicollinearity with total rooms.</sub>*

<br/>

### Feature vs Price Scatter Plots
<img src="notebook/plots/scatterplots.png" width="90%" />

*<sub>Income shows a tight linear trend. Rooms are positive but scattered. Population is noisy but still contributes to the full model.</sub>*

<br/>

### Price Distribution
<img src="notebook/plots/price_distribution.png" width="80%" />

*<sub>Near-perfect bell curve centered at $1.23M. The normal distribution validates the linear regression assumptions.</sub>*

</div>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" />

## 🤓 Did You Know?

> [!NOTE]
> 💬 The animated price counter uses `requestAnimationFrame` with a cubic easing function — the same technique used in high-end UI libraries. It also gracefully degrades for users who have `prefers-reduced-motion` enabled.

> [!NOTE]
> 💬 The model loads in a **singleton pattern** — the `.pkl` files are read from disk exactly once when the server starts. Every prediction after that is pure in-memory computation. That is why responses come back in under 200ms.

> [!NOTE]
> 💬 The confidence assessment is not cosmetic. It programmatically checks each of your 5 inputs against the interquartile ranges of the original training dataset and counts how many fall outside typical bounds.

> [!NOTE]
> 💬 The entire frontend is **738 lines of CSS** with zero frameworks. Every color, shadow, and spacing value comes from CSS custom properties defined in a single `:root` block — making the whole design system swappable by changing ~15 variables.

> [!NOTE]
> 💬 The training script does not just train a model. It runs a full EDA pipeline: missing value checks, duplicate detection, IQR-based outlier analysis, correlation heatmaps, scatter plots with trendlines, distribution plots, coefficient interpretation on unscaled data, and a multicollinearity check between rooms and bedrooms.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" />

<div align="center">

### Made with ❤️ by Yash

![GitHub](https://img.shields.io/badge/GitHub-yash5123-181717?style=for-the-badge&logo=github)

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer"/>

</div>
