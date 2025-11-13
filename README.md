# 🔬 Marketing Science: A/B Testing Playbook

Creating a Marketing Science Series where it consists of a series of tools that enable users to learn and use as a playbook/reference for their own marketing strategies. 
<img width="1465" height="318" alt="image" src="https://github.com/user-attachments/assets/52563db6-0af2-4a8e-a4a8-eb6d694ad384" />

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Application Workflow](#application-workflow)
- [Dependencies](#dependencies)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🎯 Overview

This application provides a step-by-step framework for conducting statistically sound A/B tests in marketing. It helps you:

- **Define clear business objectives** based across customer lifecycle stages
- **Select appropriate metrics** for your experiments
- **Design experiments** with power analysis and sample size calculator
- **Implement tests** with best practices
- **Analyze results** using appropriate statistical tests
- **Make data-driven decisions** based on statistical significance

## ✨ Features

### 6-Phase Workflow

1. **Phase 1: Business Objective** 🎯
   - Define your business goal
   - Select customer lifecycle stage (Awareness, Acquisition, Activation, Engagement, etc.)
   - Choose marketing channel and campaign type

2. **Phase 2: Define Metrics** 📊
   - Select primary and secondary metrics and guardrail metrics
   - Understand metric distributions (Binomial, Normal, Log-normal, etc.) to know which statistical tests to use. 
   - Get baseline estimates and industry benchmarks

3. **Phase 3: Design Experiment** 🔬
   - Learn how to do Power Analysis with built in Sample Size Calculator!
   - Learn how to set baselines, mde and understanding significance level and statistical power
   - Choose appropriate statistical tests

4. **Phase 4: Implementation** ⚙️
   - Get implementation guidelines
   - Learn randomization best practices
   - Understand experiment duration requirements

5. **Phase 5: Analysis** 📈
   - Perform statistical tests
   - Visualize results
   - Check assumptions

6. **Phase 6: Decision** ✅
   - Interpret results
   - Make go/no-go decisions
   - Document findings

### Statistical Tests Supported

- **Two-proportion z-test**: For binary metrics (conversion rates, click rates)
- **Two-sample t-test**: For continuous metrics with normal distribution
- **Mann-Whitney U test**: Non-parametric alternative for skewed data
- **Log-transformed t-test**: For log-normally distributed data (revenue, AOV)
- **Chi-square test**: For categorical distributions and randomization checks

### Marketing Channels & Metrics

Covers a wide range of marketing channels:
- Email Marketing
- Paid Search (SEM/PPC)
- Social Media
- Display Advertising
- Website/Landing Pages
- Mobile Apps
- And more...

## 🔧 Prerequisites

- **Python 3.10 or higher** (required)
- pip (Python package installer)

## 📦 Installation

### Option 1: Local Setup with Virtual Environment (Recommended)

1. **Clone or navigate to the project directory**:
   ```bash
   cd ab_test_app
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv_marsci_ab
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv_marsci_ab/bin/activate
     ```
   - On Windows:
     ```bash
     venv_marsci_ab\Scripts\activate
     ```

4. **Upgrade pip**:
   ```bash
   pip install --upgrade pip
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Global Installation

If you prefer not to use a virtual environment:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Usage

1. **Activate your virtual environment** (if using one):
   ```bash
   source venv_marsci_ab/bin/activate  # macOS/Linux
   # or
   venv_marsci_ab\Scripts\activate     # Windows
   ```

2. **Run the Streamlit application**:
   ```bash
   streamlit run mrkt_sci_ab_v2.py
   ```

3. **Open your browser**:
   - The app will automatically open in your default browser
   - Typically available at `http://localhost:8501`

4. **Navigate through the workflow**:
   - Use the navigation buttons at the top to move between phases
   - Fill in the required information in each phase
   - The sidebar will show an experiment snapshot as you progress

## 📊 Application Workflow

### Getting Started

1. **Start with Business Objective**: Define what you want to achieve
2. **Select Metrics**: Choose your primary and secondary metrics
3. **Design Experiment**: Determine sample size and test parameters
4. **Plan Implementation**: Understand how to set up your test
5. **Analyze Results**: Run statistical analysis on your data
6. **Make Decision**: Interpret results and decide next steps

### Best Practices

- **Start with clear hypotheses**: Always begin with a well-defined hypothesis
- **Choose appropriate metrics**: Select metrics that align with business goals
- **Ensure adequate sample size**: Don't rush - wait for sufficient data
- **Check assumptions**: Verify statistical test assumptions before analysis
- **Document everything**: Keep track of your experiment design and results

## 📚 Dependencies

The application uses the following Python packages:

- **streamlit** (≥1.31.0): Web framework for building the application
- **numpy** (≥1.24.3): Numerical computations
- **pandas** (≥2.0.3): Data manipulation and analysis
- **scipy** (≥1.11.3): Statistical tests and functions
- **plotly** (≥5.18.0): Interactive visualizations

All dependencies are listed in `requirements.txt` and will be installed automatically when you run `pip install -r requirements.txt`.

## 📁 Project Structure

```
ab_test_app/
├── mrkt_sci_ab_v2.py      # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── venv_marsci_ab_v1/     # Virtual environment (not included in version control)
```

## 🎨 Features Highlights

- **Interactive UI**: Modern, Google-inspired design with intuitive navigation
- **Statistical Rigor**: Built-in knowledge of statistical tests and their assumptions
- **Industry Benchmarks**: Reference data from industry sources
- **Visual Guidance**: Progress bars and visual indicators throughout
- **Real-time Calculations**: Instant sample size and statistical power calculations

## 🔍 Troubleshooting

### Python Version Error

If you see a Python version error:
- Ensure you have Python 3.10 or higher installed
- Check your Python version: `python3 --version`
- Update Python if necessary

### Import Errors

If you encounter import errors:
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify your virtual environment is activated
- Try upgrading pip: `pip install --upgrade pip`

### Streamlit Not Starting

- Make sure Streamlit is installed: `pip install streamlit`
- Check if port 8501 is available
- Try a different port: `streamlit run mrkt_sci_ab_v2.py --server.port 8502`

## 📝 Notes

- For Streamlit Cloud deployment, ensure `runtime.txt` specifies Python 3.10+
- The application automatically checks Python version on startup
- Session state is maintained throughout your workflow

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this application:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is available for use in marketing science and A/B testing workflows.

---

**Ready to run better experiments?** Start by running `streamlit run mrkt_sci_ab_v2.py` and begin with Phase 1: Business Objective!

# marketing_science_ab_test_playbook_app
