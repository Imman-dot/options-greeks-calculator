# 📊 Options Greeks Calculator (Black–Scholes)

Command-line Python project that calculates **European option prices and Greeks** (Delta, Gamma, Vega, Theta) using the **Black–Scholes model**.  
Includes a neat reporting mode and visualizations showing how sensitivities evolve with **stock price (S)** and **time-to-expiry (T)**.

---

## 🔑 Key Features

- **Option Pricing**
  - Black–Scholes closed-form formulas for calls and puts  

- **Greeks Calculation**
  - Delta, Gamma, Vega, Theta  

- **Interactive Reporting**
  - Prints formatted output including Vega per **1%** volatility and Theta per **day**  

- **Visualizations**
  - Greeks vs underlying price (S)  
  - Greeks vs time-to-expiry (T)  
  - Separate plots for calls and puts  

- **CLI Interface**
  - Simple flags: `--report`, `--plotS`, `--plotT`, `--saveplots`, `--demo`  

---

## 📝 Overview

This project implements the **Black–Scholes model**, the foundation of modern option pricing, and turns it into a **practical CLI tool**.  

It allows you to:
- Compute **option prices** quickly  
- Generate all major **Greeks** used in hedging and risk management  
- **Visualize** how sensitivities evolve with price and time  

The goal was to bridge **finance theory with production-ready code**, building a tool that would look equally at home in a learning environment or as part of a trading research toolkit.

---

## 🎯 Problem Statement & Business Context

Options traders, market-makers, and risk managers constantly monitor how their portfolios respond to **changes in price, volatility, and time**. The **Greeks** are the universal language for this:  

- **Delta** tells you directional exposure  
- **Gamma** captures curvature of risk  
- **Vega** shows volatility sensitivity  
- **Theta** measures time decay  

Having a tool to **compute and visualize Greeks** is crucial for:  
- **Traders**: hedging and position sizing  
- **Risk managers**: stress-testing exposure  
- **Students/Researchers**: building intuition for how options behave  

---

## 🛠 Data & Tools Used

- **Languages & Frameworks**: Python 3, CLI with `argparse`, `dataclasses` for clean data handling  
- **Libraries**:  
  - `numpy` for numerical stability  
  - `matplotlib` for plots  
  - `math` for Black–Scholes formulas  

---

## 📐 Methodology

### Black–Scholes Pricing
Call option:  

\[
C = S \cdot N(d_1) - K e^{-rT} N(d_2)
\]  

Put option:  

\[
P = K e^{-rT} N(-d_2) - S N(-d_1)
\]  

Where:  

\[
d_1 = \frac{\ln(S/K) + (r + 0.5\sigma^2)T}{\sigma\sqrt{T}}, \quad
d_2 = d_1 - \sigma\sqrt{T}
\]  

### Greeks
\[
\Delta_{\text{call}} = N(d_1), \quad \Delta_{\text{put}} = N(d_1) - 1
\]  

\[
\Gamma = \frac{\phi(d_1)}{S\sigma\sqrt{T}}
\]  

\[
\text{Vega} = S\phi(d_1)\sqrt{T} \quad (\text{per 1.00 vol; per 1% = Vega/100})
\]  

\[
\Theta_{\text{call}} = -\frac{S\phi(d_1)\sigma}{2\sqrt{T}} - rKe^{-rT}N(d_2)
\]  

\[
\Theta_{\text{put}} = -\frac{S\phi(d_1)\sigma}{2\sqrt{T}} + rKe^{-rT}N(-d_2)
\]  

Plots sweep **S** (50 → 150) and **T** (0 → 1y) to show how exposures evolve.

---

### Example Report

```bash
=== Black–Scholes ===
Type       : call
S, K       : 100.000000, 100.000000
T (years)  : 0.500000
sigma, r   : 0.200000, 0.030000
----------------------------
Price      : 6.371028
Delta      : 0.570158
Gamma      : 0.027772
Vega       : 27.772132   (per 1.00 vol; per 1% ≈ 0.277721)
Theta (yr) : -7.073770
Theta/day  : -0.019380
```

### Sample Plots

**Call Greeks vs Stock Price (S)**  
![Call vs S](Call%20vs%20S.png)

**Put Greeks vs Stock Price (S)**  
![Put vs S](Put%20vs%20S.png)

**Call Greeks vs Time-to-Expiry (T)**  
![Call vs T](Call%20vs%20T.png)

---

##  Key Challenges & Solutions

- **Numerical Stability**: handled cases where \( T \to 0 \) or \( \sigma \to 0 \) by enforcing safe lower bounds  
- **Units**: reported Vega per 1% vol, Theta per day — makes results intuitive for traders  
- **UX**: added `--demo` and `--saveplots` so new users get instant results without setting parameters  

---

##  Takeaways

- Converted **quantitative finance theory into code**  
- Built a **production-style CLI** with clear user options  
- Developed strong intuition by **visualizing Greeks** vs price and time  
- Reinforced the importance of **stability and usability** when building financial tools  

---

##  Future Improvements

- Add **dividend yield (q)** support  
- Implement **implied volatility solver** (given market price → solve σ)  
- Add **unit tests** with `pytest`  
- Package for distribution on **PyPI**  

---

## 👤 Author

**Immanuel Edunsin (Imman-dot)**  
T-Level Finance student | Aspiring **Quant / Trader**

- [LinkedIn](https://www.linkedin.com/in/immanuel-edunsin-0324ab336/)  
- [GitHub](https://github.com/Imman-dot)  

