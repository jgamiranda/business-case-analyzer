# Core Financial Modeling — Summary

Source: Industry Standard Methodology (Core FM)

---

## Business Case

**Projecoes de 3 demonstracoes** seguem processo sequencial: IS -> BS -> CFS, com links circulares resolvidos por iteracao.

**Step 1 - Projetar Revenue** em 3 metodos:
1. Simple % growth rate (caso rapido, 30min)
2. `# Units Sold * Avg Price per Unit` (mais defensavel)
3. `Market Share * Market Size` (industrias oligopolistas)

Sempre justificar o growth rate com drivers operacionais (ex: novos sales reps, pricing power).

**Step 2 - Projetar COGS e OpEx** como % de Revenue baseado em tendencia historica. Margem operacional deve seguir trend logico (ex: 10% -> 12% em 5 anos se ha operating leverage).

**Step 3 - Balance Sheet Operacional:**
- AR, Inventory, Prepaid = % of Revenue
- AP, Accrued Expenses = % of COGS ou OpEx
- `Change in WC = (Old Liabilities - New Liabilities) + (New Assets - Old Assets)`
- Checar: Change in WC como % de Change in Revenue deve ser consistente com historico

**Step 4 - CFS restante:** CapEx via schedule separado (industrias capital-intensive) ou % Revenue (tech). D&A geralmente % of CapEx ou PP&E.

**Step 5 - Cash e Debt:** Projetar saldo de Cash -> calcular Interest Income. Projetar Debt schedule -> Interest Expense. Circularidade resolvida com iteracao no Excel.

**Checks do modelo:**
- Revenue/EBIT/UFCF/EBITDA growth rates convergem para single-digits no longo prazo
- BS balanceia (Assets = L + E)
- CFS: Beginning Cash + Net Change = Ending Cash

**Formatting Standards (CFI):**
- Inputs = azul (editavel); Formulas = preto; Links = verde; Outputs = bold
- Sempre indicar moeda, escala (R$k, R$M) e periodo
- 3 cenarios minimo: Base, Upside, Downside

---

## M&A

**Accretion/Dilution em 5 Steps:**

```
Step 1: Buyer NI, EPS, Seller NI, EPS (standalone)
Step 2: Purchase Equity Value = Share Price * (1 + Premium%) * Diluted Shares
Step 3: Financing mix (Cash/Debt/Stock) + custos
Step 4: Combined NI = Buyer NI + Seller NI
        - Foregone Interest on Cash * (1 - Tax Rate)
        - New Interest on Debt * (1 - Tax Rate)
        + Interest Income on Seller's Cash * (1 - Tax Rate)
        Combined Shares = Buyer Shares + New Shares Issued
        Combined EPS = Combined NI / Combined Shares
Step 5: EPS Accretion = (Combined EPS - Buyer Standalone EPS) / Buyer EPS
```

**Regras de decisao rapida (100% Stock):**
- `Buyer P/E > Seller P/E at Purchase Price` -> **Accretive**
- `Buyer P/E < Seller P/E at Purchase Price` -> **Dilutive**

**Regra geral (qualquer mix):**
- `Weighted Cost of Acquisition < Seller Yield (NI/Equity Value)` -> **Accretive**
- Custo de cada fonte: Cash = Risk-Free Rate * (1-t); Debt = Coupon Rate * (1-t); Equity = 1/P*E

**Purchase Price Allocation (PPA):**
```
Goodwill = Purchase Equity Value - Seller's CSE
         - PP&E Write-Up - Other Intangible Write-Ups
         + New DTL Created (= Write-Ups * Tax Rate)
         + Existing DTA Write-Down - Existing DTL Write-Down
```
Nova DTL surge porque D&A dos write-ups e dedutivel para book mas NAO para cash taxes.

**Sources & Uses:**
- Sources = Cash + New Debt + Stock Issued (+ Seller's existing Debt refinanced)
- Uses = Purchase Equity Value + Fees + Seller Debt Refinanced

**Synergies:**
- Revenue synergies (cross-selling) e Expense synergies (headcount, buildings)
- Modelar Merger & Integration Costs como % das synergies realizadas
- Erros comuns: esquecer M&I costs, ignorar COGS adicional das revenue synergies

**Contribution Analysis:** Cada empresa contribui X% de Revenue, EBITDA, NI -> define ownership split justo em stock-for-stock mergers.

---

## Valuation DCF

**UFCF Formula:**
```
UFCF = EBIT * (1 - Tax Rate)    [NOPAT]
     + D&A
     +/- Change in Working Capital
     - CapEx
```
NAO adicionar SBC (dilui acionistas). Excluir Net Interest, Other Income, itens nao-recorrentes.

**WACC:**
```
WACC = Ke * %Equity + Kd * (1 - t) * %Debt + Kp * %Preferred
Ke = Rf + ERP * Levered Beta   (CAPM)
```
- ERP: 4-6% em developed markets, maior em emerging
- Kd: YTM dos bonds ou average interest rate

**Un-lever / Re-lever Beta:**
```
Unlevered Beta = Levered Beta / (1 + D/E * (1-t) + Pref/E)
Levered Beta = Unlevered Beta * (1 + D/E * (1-t) + Pref/E)
```
Usar median Unlevered Beta dos comparables, re-lever com capital structure ALVO (implied), nao atual.

**Terminal Value - 2 metodos:**
```
Gordon Growth:
TV = Final Year UFCF * (1 + g) / (WACC - g)
# g deve ser < GDP growth (1-3% em developed markets)

Exit Multiple:
TV = Terminal Year EBITDA * Exit Multiple

Cross-checks:
Implied Terminal Multiple = TV / Terminal EBITDA
Implied g = (TV * WACC - Final UFCF) / (TV + Final UFCF)
```

**Enterprise Value -> Equity Value Bridge:**
```
Implied EV = Sum(PV of UFCFs) + PV(TV)

Implied Equity Value = EV
  + Cash & Equivalents
  + Financial Investments
  + Equity Investments
  + NOLs (tax-effected)
  - Total Debt (fair market value)
  - Preferred Stock
  - Capital Leases
  - Noncontrolling Interests
  - Unfunded Pensions * (1 - Tax Rate)
  - (Potentially) Operating Leases

Implied Share Price = Equity Value / Diluted Shares
```
Regra anti-double-count: se deduziu expense no UFCF, NAO subtrair liability no bridge. Se excluiu/adicionou expense, SUBTRAIR liability.

**EV Formula (top-down):**
```
Enterprise Value = Equity Value - Cash + Debt + Preferred Stock + NCI
(Advanced: subtrair Investments, Non-Core Assets, NOLs;
           adicionar Unfunded Pensions, Leases)
```

**Diluted Shares (Treasury Stock Method):**
```
Diluted Shares = Basic + In-the-Money Options
New Shares from Options = # Options - (# Options * Exercise Price / Current Price)
```

**Multiples:**

| Metric   | Multiple       | Numerator        | Denominator                    |
|----------|----------------|------------------|--------------------------------|
| Revenue  | TEV / Revenue  | Enterprise Value | Revenue                        |
| EBITDA   | TEV / EBITDA   | Enterprise Value | EBIT + D&A + Non-Recurring     |
| Earnings | P / E          | Equity Value     | Net Income to Common           |

- Trading Comps: Current EV / NTM EBITDA. 5-10 comps por industry, size, geography
- Precedent Transactions: EV pago / LTM EBITDA. Inclui control premium (20-40%)

---

## LBO

**Modelo em 3 steps:**
1. Purchase Price + Sources & Uses
2. Projetar cash flows + Debt repayment
3. Exit assumptions + calcular retornos

**Purchase Price:** `EBITDA * Entry Multiple`. Cash-free, debt-free (Cash e Debt existentes zerados e substituidos).

**Sources & Uses:**
```
Sources: Senior Debt + Sub Debt + Mezzanine + Investor Equity (plug) + Min Cash
Uses: Purchase Enterprise Value + Transaction Fees + Financing Fees
Investor Equity = Total Uses - Total Debt Raised
```

**Debt Schedule:**
```
FCF = Net Income + D&A +/- Change in WC - CapEx
Cash Available for Repayment = FCF + Beginning Cash - Minimum Cash
```
Ordem: Revolver primeiro, Term Loans (mandatory), depois sweeps.

**Exit e Returns:**
```
Exit EV = Exit Year EBITDA * Exit Multiple
Exit Equity = Exit EV - Net Debt
MoM = Exit Equity / Investor Equity
IRR = (MoM)^(1/n) - 1
```

**Quick IRR Math:**

| MoM | 3 anos | 5 anos |
|-----|--------|--------|
| 2x  | ~25%   | ~15%   |
| 3x  | ~45%   | ~25%   |

```
Rule of 72: anos para 2x = 72 / IRR%
Rule of 115: anos para 3x = 115 / IRR%
```

**Returns Attribution:**
```
EBITDA Growth = (Exit EBITDA - Entry EBITDA) * Purchase Multiple
Multiple Expansion = (Exit Multiple - Purchase Multiple) * Exit EBITDA
Debt Paydown = Total Return - EBITDA Growth - Multiple Expansion
```

**Targets tipicos PE (mid-market, 5yr hold):**
- Downside: min 1.5x MoM
- Base: 2.0x MoM, 15% IRR
- Upside: 3.0x MoM, 25% IRR

**Credit Metrics:**
```
Leverage Ratio = Debt / EBITDA (max ~5x tipico)
Interest Coverage = EBITDA / Interest Expense (min 2.0x)
DSCR = (FCF + Interest + Leases) / Fixed Charges
FCCR = (EBITDA - CapEx - Cash Taxes - Dividends) / Fixed Charges
Debt / Total Capital < 50% (covenant tipico)
```

**Ideal LBO Candidate:** Stable cash flows, low CapEx, asset-rich (collateral), mature business, reasonable price, clear exit path. Estabilidade > crescimento.
