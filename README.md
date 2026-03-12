# Global_Wage_Convergence-A_Path_To_Reducing_Inequality



This repository accompanies the research paper:

**“Global Wage Convergence: A Path to Reducing Inequality?”**  
📄 _The Journal of Economic Inequality_

---

## 🔍 Project Overview

This project investigates whether global wage convergence is occurring and whether it offers a viable path to reducing international income inequalities. We construct wage estimates for countries globally using GDP per capita, employment ratios, labor share of income, and working hours. Convergence is tested through β- and σ-convergence, benchmarking against OECD wages.

---

## 📁 Repository Structure

 Global_Wage_Convergence
├── Code/ # All Jupyter Notebooks, numbered by stage

├── Data/ # Input datasets (CSV, Excel)

├── Result/ # Output files (CSV) and results

│ 
└── Plots/ # Final figures in PDF format

├── README.md # Project documentation


---

## Replication and Technical Notes

This repository contains the full code used to generate the results in the paper.

### OECD Overview Validation (Section 3.4.1)

To compare the imputed wage series with official OECD wages, the following steps are implemented programmatically:

1. Merge the estimated wage series and OECD series by country and year, compute log values, and construct the gap  

   d(i,t) = log(w_OECD(i,t)) − log(w_hat(i,t))

2. For each country compute the standard deviation of the gap:

   σ_i = std(d_i,t)

3. Plot both series

   log(w_OECD(i,t))  
   log(w_hat(i,t))

   and shade the confidence region:

   log(w_OECD(i,t)) ± 1.96 σ_i

This procedure generates the OECD comparison figures shown in the paper.

---

### Convergence Projection Models (Section 3.5)

For each country–scenario combination the following model specifications are evaluated.

Candidate models include:

Parametric curves

Exponential decay

f(t) = A exp(-k t) + C

Logistic curve

f(t) = C + L / (1 + exp(-k t))

Flexible regression specifications

• Linear trend  
• Quadratic trend  
• Square-root trend  

Polynomial features with linear regression are implemented using **scikit-learn**.

A cubic (degree-3) specification was tested but excluded because it produced unstable extrapolations outside the historical sample.

The best-performing model is selected using rolling-origin time-series cross-validation based on mean squared error (MSE).
