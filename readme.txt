Investment Fund Growth Simulator
This repository contains a Python application built with Streamlit that simulates the growth of an investment fund over time. Users can adjust various parameters like monthly deposits, annual interest rates, and simulate the impact of market events (like "Tariff Impact" and "Extreme Event") to visualize their potential investment growth.
Features
* Interactive Simulation: Adjust investment period, monthly deposit, and annual interest rate using sliders and input fields.
* Market Event Simulation: Option to enable and customize the severity of two predefined market events (Tariff Impact and Extreme Event) that cause a percentage drop in the fund value at specific points in time.
* Visual Data Representation: A Plotly chart displays the accumulated deposits versus the fund value with growth and event impacts over the selected investment period.
* Key Metrics: Displays the total accumulated deposits and the final fund value, along with the total growth achieved.
How it Works
The core of the application is a simulation function that calculates monthly fund value based on deposits, compound interest, and applies simulated market shocks at predetermined months (Year 2 for Tariff Impact, Year 3 for Extreme Event). Streamlit is used to create an interactive web interface for inputting parameters and displaying the results and the interactive chart.
Getting Started
Follow these steps to get a copy of the project up and running on your local machine.
Prerequisites
You need Python installed on your system. This application also requires the following Python libraries:
* streamlit
* pandas
* plotly
* python-dateutil
You can install them using pip:
pip install streamlit pandas plotly python-dateutil

Installation and Running Locally
1. Clone the repository (or download app.py):
If you've already pushed your code to GitHub, you can clone it:
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name

(Replace your-username and your-repository-name with your actual GitHub details.)
If you just have the app.py file, navigate to its directory:
cd /Users/nathan.jones/Documents/Code/app # Or wherever your app.py is located

2. Run the Streamlit application:
streamlit run app.py

This command will open the application in your default web browser (usually at http://localhost:8501).
Deployment
This application is built with Streamlit and requires a Python environment to run. It cannot be directly hosted on static hosting services like GitHub Pages.
To deploy this application online, consider using:
   * Streamlit Community Cloud: The easiest way to deploy Streamlit apps.
   * Heroku
   * PythonAnywhere
   * AWS, Google Cloud Platform, Azure (for more advanced hosting)
Contributing
If you have suggestions for improvements or find any issues, feel free to open an issue or submit a pull request.
License
[Optional: Add a license here, e.g., MIT License]