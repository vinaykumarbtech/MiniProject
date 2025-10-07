from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import os
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt


app = Flask(__name__)

df = pd.read_csv("static/petrol_bunk_analysis_hyderabad_expanded.csv")

os.makedirs("static/images", exist_ok=True)

def get_dropdown_options():
    return {
        "areas": sorted(df["Area"].unique()),
        "years": sorted(df["Year"].unique()),
        "months": sorted(df["Month"].unique())
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    options = get_dropdown_options()
    return render_template('index.html', options=options)

@app.route('/dashboard', methods=['POST'])
def dashboard():
    area = request.form.get("area")
    year = request.form.get("year")
    month = request.form.get("month")

    # Filter dataset
    filtered_df = df[(df["Area"] == area) & (df["Year"] == int(year))]

    if filtered_df.empty:
        return f"No data found for {area}, {year}."

    # Save all plots
    plot_paths = {}

    # 1️⃣ **Seaborn Histogram**
    plt.figure(figsize=(8, 5))
    sns.histplot(filtered_df["Petrol Consumption (Liters)"], bins=10, kde=True, color='blue')
    plt.title("Petrol Consumption Distribution")
    plt.xlabel("Petrol Consumption (Liters)")
    plt.ylabel("Frequency")
    plot_paths["histogram"] = "static/images/histogram.png"
    plt.savefig(plot_paths["histogram"])
    plt.close()

    # 2️⃣ **Line Plot (Yearly Trend)**
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=filtered_df, x="Month", y="Petrol Consumption (Liters)", marker='o', color='green')
    plt.title("Monthly Petrol Consumption Trend")
    plt.xlabel("Month")
    plt.ylabel("Consumption (Liters)")
    plot_paths["line"] = "static/images/line_plot.png"
    plt.savefig(plot_paths["line"])
    plt.close()

    # 3️⃣ **Bar Chart**
    plt.figure(figsize=(8, 5))
    sns.barplot(data=filtered_df, x="Month", y="Petrol Consumption (Liters)", palette="Blues_d")
    plt.title("Monthly Petrol Consumption")
    plt.xlabel("Month")
    plt.ylabel("Consumption (Liters)")
    plot_paths["bar"] = "static/images/bar_chart.png"
    plt.savefig(plot_paths["bar"])
    plt.close()

    # 4️⃣ **Pie Chart (Consumption Share per Month)**
    plt.figure(figsize=(6, 6))
    filtered_df.groupby("Month")["Petrol Consumption (Liters)"].sum().plot.pie(autopct='%1.1f%%', cmap="coolwarm")
    plt.title("Monthly Consumption Share")
    plot_paths["pie"] = "static/images/pie_chart.png"
    plt.savefig(plot_paths["pie"])
    plt.close()

    # 5️⃣ **Scatter Plot (Consumption vs Month)**
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=filtered_df, x="Month", y="Petrol Consumption (Liters)", color='red')
    plt.title("Petrol Consumption Scatter Plot")
    plt.xlabel("Month")
    plt.ylabel("Consumption (Liters)")
    plot_paths["scatter"] = "static/images/scatter_plot.png"
    plt.savefig(plot_paths["scatter"])
    plt.close()

    # 6️⃣ **Box Plot (Distribution per Month)**
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=filtered_df, x="Month", y="Petrol Consumption (Liters)", palette="Set2")
    plt.title("Monthly Consumption Distribution")
    plt.xlabel("Month")
    plt.ylabel("Consumption (Liters)")
    plot_paths["box"] = "static/images/box_plot.png"
    plt.savefig(plot_paths["box"])
    plt.close()

    return render_template('dashboard.html', area=area, year=year, month=month, plot_paths=plot_paths)

if __name__ == '__main__':
    app.run(debug=True)
