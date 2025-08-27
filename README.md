# 📊 Options Greeks Calculator (Black–Scholes)

A Python command-line tool that computes **European option prices and Greeks** (Delta, Gamma, Vega, Theta) using the **Black–Scholes model**.  
Includes neat reporting and plots showing how Greeks change with **underlying price (S)** and **time-to-expiry (T)**.  

This project showcases practical **quantitative finance + Python** skills and is ideal for learning, trading strategy research, or interview preparation.

---

## 🚀 Features
- **Black–Scholes pricing** for European calls & puts  
- **Greeks calculation**: Delta, Gamma, Vega, Theta  
- **Report mode**: clean formatted output (Theta/day, Vega per 1%)  
- **Visualization**:
  - Greeks vs Underlying Price (S)
  - Greeks vs Time-to-Expiry (T)
  - Call & Put plots  
- **CLI interface** with `argparse`  
- **Flexible output**:
  - Show plots in a window  
  - Or save them as `.png` for reports/README  

---

## 📦 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/Imman-dot/options-greeks-calculator.git
cd options-greeks-calculator
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

