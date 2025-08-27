#!/usr/bin/env python3
import math
import argparse
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt


SQRT_2PI = math.sqrt(2.0 * math.pi)

def std_norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / SQRT_2PI

def std_norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

# -------- d1 and d2 --------
def d1(S, K, T, r, sigma):
    T = max(T, 1e-8)
    sigma = max(sigma, 1e-8)
    return (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * math.sqrt(max(T, 1e-8))

# -------- pricing --------
def bs_price(S, K, T, r, sigma, opt_type="call"):
    d1v = d1(S, K, T, r, sigma)
    d2v = d2(S, K, T, r, sigma)
    disc = math.exp(-r * T)
    if opt_type == "call":
        return S * std_norm_cdf(d1v) - K * disc * std_norm_cdf(d2v)
    elif opt_type == "put":
        return K * disc * std_norm_cdf(-d2v) - S * std_norm_cdf(-d1v)
    else:
        raise ValueError("opt_type must be 'call' or 'put'")

# -------- Greeks --------
@dataclass
class Greeks:
    price: float
    delta: float
    gamma: float
    vega: float
    theta: float

def bs_greeks(S, K, T, r, sigma, opt_type="call"):
    T = max(T, 1e-8)
    sigma = max(sigma, 1e-8)
    d1v = d1(S, K, T, r, sigma)
    d2v = d2(S, K, T, r, sigma)
    pdf = std_norm_pdf(d1v)
    Nd1 = std_norm_cdf(d1v)
    Nd2 = std_norm_cdf(d2v)
    disc = math.exp(-r * T)

    price = bs_price(S, K, T, r, sigma, opt_type)

    if opt_type == "call":
        delta = Nd1
        theta = -(S * pdf * sigma) / (2 * math.sqrt(T)) - r * K * disc * Nd2
    else:
        delta = Nd1 - 1.0
        theta = -(S * pdf * sigma) / (2 * math.sqrt(T)) + r * K * disc * std_norm_cdf(-d2v)

    gamma = pdf / (S * sigma * math.sqrt(T))
    vega  = S * pdf * math.sqrt(T)

    return Greeks(price, delta, gamma, vega, theta)

def print_report(S, K, T, r, sigma, opt_type, g):
    """
    Make the output human-readable and interview-ready.
    - Shows theta per year and per day
    - Shows vega per 1% vol (what traders use)
    """
    print("=== Black–Scholes ===")
    print(f"Type       : {opt_type}")                 # call or put
    print(f"S, K       : {S:.6f}, {K:.6f}")         # underlying and strike (fixed width)
    print(f"T (years)  : {T:.6f}")                  # time to expiry in YEARS
    print(f"sigma, r   : {sigma:.6f}, {r:.6f}")     # vol and risk-free rate
    print("----------------------------")
    print(f"Price      : {g.price:.6f}")            # fair option price
    print(f"Delta      : {g.delta:.6f}")            # ≈ shares per option
    print(f"Gamma      : {g.gamma:.6f}")            # delta’s sensitivity to S
    print(f"Vega       : {g.vega:.6f}   (per 1.00 vol; per 1% ≈ {g.vega/100:.6f})")
    #              ^ vega here is “per 1.00 of vol” (e.g., from 0.20→1.20). Traders talk per 1%,
    #                so we also print vega/100.
    print(f"Theta (yr) : {g.theta:.6f}")            # time decay per YEAR
    print(f"Theta/day  : {g.theta/365:.6f}")        # time decay per DAY (easier to feel)

import numpy as np
import matplotlib.pyplot as plt

def plot_greeks_vs_S(K=100, T=0.5, r=0.03, sigma=0.2, opt_type="call"):
    """
    Plot how Greeks change as the underlying price S varies.
    """
    S_values = np.linspace(50, 150, 100)  # 100 points from 50 → 150
    deltas, gammas, vegas, thetas = [], [], [], []

    for S in S_values:
        g = bs_greeks(S, K, T, r, sigma, opt_type)
        deltas.append(g.delta)
        gammas.append(g.gamma)
        vegas.append(g.vega / 100.0)  # per 1% vol
        thetas.append(g.theta / 365.0)  # per day

    plt.figure(figsize=(10, 6))
    plt.plot(S_values, deltas, label="Delta")
    plt.plot(S_values, gammas, label="Gamma")
    plt.plot(S_values, vegas, label="Vega (per 1%)")
    plt.plot(S_values, thetas, label="Theta/day")
    plt.axhline(0, color="black", lw=0.5)
    plt.title(f"{opt_type.capitalize()} Greeks vs Underlying Price (K={K}, T={T}yr, σ={sigma}, r={r})")
    plt.xlabel("Stock Price S")
    plt.ylabel("Greek Value")
    plt.legend()
    plt.grid(True)
    plt.show()

def parse_args():
    """
    Reads command-line flags for option inputs.
    Example:
      python3 starter-kit.py --S 100 --K 100 --T 0.5 --sigma 0.2 --r 0.03 --type call --report
    """
    p = argparse.ArgumentParser(description="Black–Scholes price & Greeks calculator")
    p.add_argument("--S", type=float, help="Underlying price (e.g., 100)")
    p.add_argument("--K", type=float, help="Strike price (e.g., 100)")
    p.add_argument("--T", type=float, help="Time to expiry in YEARS (e.g., 30/365)")
    p.add_argument("--sigma", type=float, help="Volatility (annual, decimal, e.g., 0.2)")
    p.add_argument("--r", type=float, default=0.0, help="Risk-free rate (annual, decimal)")
    p.add_argument("--type", choices=["call","put"], default="call", help="Option type")
    p.add_argument("--report", action="store_true", help="Print a neat report")
    p.add_argument("--demo", action="store_true", help="Run demo with preset inputs")
    return p.parse_args()

# -------- smoke test --------
def _smoke_test():
    print("Running smoke test…")
    print("φ(0)  =", round(std_norm_pdf(0.0), 5))
    print("N(0)  =", round(std_norm_cdf(0.0), 5))
    print("N(1)  =", round(std_norm_cdf(1.0), 5))

    S, K, T, r, sigma = 100, 100, 0.5, 0.03, 0.20
    print("d1 ≈", round(d1(S, K, T, r, sigma), 6))
    print("d2 ≈", round(d2(S, K, T, r, sigma), 6))

    g_call = bs_greeks(S, K, T, r, sigma, "call")
    g_put  = bs_greeks(S, K, T, r, sigma, "put")
    print("Call Greeks:", g_call)
    print("Put  Greeks:", g_put)
        # demo: pretty report for the call
    print_report(S, K, T, r, sigma, "call", g_call)

def main():
    args = parse_args()

    # If no inputs provided, run demo
    if args.S is None or args.K is None or args.T is None or args.sigma is None:
        if args.demo:
            S, K, T, r, sigma, opt_type = 100, 100, 0.5, 0.03, 0.20, "call"
            g = bs_greeks(S, K, T, r, sigma, opt_type)
            print_report(S, K, T, r, sigma, opt_type, g)
            return
        else:
            print("Missing inputs. Example:")
            print("  python3 starter-kit.py --S 100 --K 100 --T 0.5 --sigma 0.2 --r 0.03 --type call --report")
            print("Or try:  python3 starter-kit.py --demo")
            return

    # Compute results
    g = bs_greeks(args.S, args.K, args.T, args.r, args.sigma, args.type)
    if args.report:
        print_report(args.S, args.K, args.T, args.r, args.sigma, args.type, g)
    else:
        print(g)

if __name__ == "__main__":
    main()

