# 🚴‍♂️ Bike Sharing - Final Data Analytics Project

Welcome to my final project for the Dicoding course **"Belajar Analisis Data Dengan Python"**. In this project, I dive deep into the world of **bike-sharing** data, analyzing trends and patterns using **Python**. This includes **Data Wrangling**, **Exploratory Data Analysis (EDA)**, and **Data Visualization**. To make this analysis more interactive, I also created a **dashboard** using **Streamlit**. Feel free to explore it by clicking the link on the right sidebar or [here](https://bike-sharing-syahrial.streamlit.app/).

For details on the dataset background, characteristics, and file structure, refer to the `README.md`. Below, I outline the project workflow and how you can interact with the data.

---

## 📂 Project Structure

```
.
├── dashboard
│ ├── dashboard.py
│ └── day.csv
├── data
│ ├── day.csv
| └── hour.csv
├── README.md
├── notebook_analisis.ipynb
└── requirements.txt

```

## 🔄 Project Workflow

### 1. Data Wrangling

- **Gathering Data**: Pulling in the bike-sharing dataset.
- **Assessing Data**: Reviewing the data for inconsistencies and missing values.
- **Cleaning Data**: Tidying the data for further analysis.

### 2. Exploratory Data Analysis (EDA)

- **Business Questions**: Formulating key questions to explore.
- **Exploration**: Digging deep into the data to extract meaningful insights.

### 3. Data Visualization

- **Visual Storytelling**: Crafting visualizations to answer business questions and showcase key findings.

### 4. Dashboard

- **DataFrame Setup**: Preparing data for use in the dashboard.
- **Interactive Filters**: Adding dynamic filtering options for an enhanced user experience.
- **Visualization Integration**: Completing the dashboard with rich visualizations.

_Note: Steps 1 to 3 are performed in `notebook_analisis.ipynb`, while step 4 is in the `dashboard/` folder._

---

## 🚀 Getting Started

### Using `notebook_analisis.ipynb`

1. **Download** the project.
2. Open your preferred IDE like **Jupyter Notebook** or **Google Colab**.
3. **Create a New Notebook** and upload the `.ipynb` file.
4. Connect to the runtime and **run the cells**.

### Running the Dashboard (`dashboard/dashboard.py`)

1. **Download** the project.
2. Install **Streamlit** using `pip install streamlit`. You'll also need libraries like **pandas**, **numpy**, **scipy**, **matplotlib**, and **seaborn**, or you can do

```
pip install -r requirement.txt
```

3. Keep the **CSV files** in the same folder as `dashboard.py` to maintain the data source.
4. Run the dashboard by opening your terminal and typing:

```bash
streamlit run dashboard.py
```
