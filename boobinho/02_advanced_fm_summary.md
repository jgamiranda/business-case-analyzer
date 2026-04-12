# Advanced Financial Modeling — Summary

Source: Industry Standard Methodology (Advanced FM)

---

## Business Case (Advanced)

**Convertible Bonds** -- contabilizacao complexa:
- Separar Debt Component (PV dos cash flows usando coupon rate de debt equivalente nao-conversivel) e Equity Component (residual = Face Value - Debt Component)
- Book Value inicial = Face Value - Equity Component - Issuance Fees
- Amortizacao do Debt Discount: `Amortization = (Beginning BV + Beginning Fee Balance) * Equivalent Rate - Cash Interest`
- Conversao: `IF(Year = Conversion Year, -MIN(Beginning Face Value, Initial Face Value), 0)`

**SBC & Excess Tax Benefits (ASC 718):**
- SBC nao reduz Cash Taxes na emissao; cria DTA
- Quando exercido, se valor aumentou: `Excess Tax Benefit = (Fair Value - Grant Value) * Tax Rate`
- U.S. GAAP pos-2017: Excess Tax Benefit vai direto no IS (pode fazer NI > Pre-Tax Income)
- IFRS: DTA reavaliado anualmente, Tax Surplus em OCI

**Financial Investments:**
- Trading/FVPL = Unrealized G/L no IS com DTA/DTL adjustment
- AFS/FVOCI = G/L em AOCI (equity), sem IS
- HTM = sem registro de G/L (so bonds)
- Pos-ASU 2016-01: equity securities so FVPL; bonds qualquer categoria

**Equity Method vs Consolidation:**
- <50% ownership = Equity Method (Equity Investment no BS, earnings reversed no CFS, so dividends sao cash)
- >=50% = Consolidation 100% com NCI adjustment
- Realized G/L na venda parcial: `(Market Cap * Previous Ownership% - Cost Basis) * (-% Change / Previous Ownership%)`

**Pension (DB):**
- Pension Asset = Actual Return + Employer Contributions + Participant Contributions - Benefit Payments
- PBO (Liability) = Service Cost + Interest Cost + Participant Contributions - Benefit Payments +/- Actuarial Adjustments
- Service Cost = operational (nao-cash); Interest Cost = PBO * Discount Rate

---

## M&A (Advanced)

**Stock vs Asset vs 338(h)(10):**

| Aspecto | Stock Purchase | Asset Purchase | 338(h)(10) |
|---------|---------------|----------------|------------|
| Goodwill | NAO amortiza para tax | Amortiza 15y para tax | Amortiza 15y para tax |
| Write-up D&A | NAO dedutivel para cash tax | Dedutivel | Dedutivel |
| Forma legal | Stock | Assets | Stock (forma) / Asset (tax) |
| Requisitos | -- | -- | Buyer C-corp, Seller U.S., >=80% em 12 meses |

**NOLs em M&A — formula critica:**
```
Allowable Annual NOL Usage = Equity Purchase Price * MAX(Past 3 Months' Adj Long-Term Rates)
Write-down = MAX(0, NOL Balance - Allowable Usage * Years Until Expiration)
DTA Write-down = MAX(0, NOL DTA - Allowable Usage * Tax Rate * Years Until Expiration)
```
- Stock Purchase: uso limitado anual (Section 382)
- Asset/338(h)(10): NOLs = 100% write-down

**Stub Periods:**
- Quando deal fecha em data irregular, criar 2 stubs
- IS/CFS = full-year * fraction (ex: 45/92 dias)
- BS = rollforward: items de CFS linkam do BS anterior +/- CFS stub
- Working Capital = old + (FY difference * stub fraction)
- Modelo trimestral: YoY growth (nao QoQ por sazonalidade)

**Spinoffs/Carveouts:**
- Distribution Ratio = shares SpunOff por share Parent
- BS: realocar assets/liabilities, Cash transfer (excess -> Parent)
- IS: remover receitas/despesas da SpunOff, recalcular taxes standalone
- Dis-synergies = custos adicionais de operar separadamente
- Beta SpunOff: re-levered Beta dos Public Comps (sem historico proprio)
- SOTP: `Implied Equity Value = Parent EV + SpunOff EV - Capitalized Corporate Overhead`
- Share count = `Parent Shares * (1 + Distribution Ratio)`

**Break-even Synergies:**
```
= (Lost Earnings from Cash + New Interest - Target Net Income) / (1 - Tax Rate) / Acquirer Shares
```

---

## Valuation DCF (Advanced)

**Mid-Year Convention:**
- Desconta a t-0.5, t-1.5, etc. (cash flows ocorrem no meio do ano)
- `Discount Factor = 1 / (1 + WACC)^(t - 0.5)`
- TV tipicamente 60-80% do EV total (flag se > 85%)

**SOTP em Spinoffs:**
- Valuar cada entidade separadamente via Public Comps + DCF
- Range de Implied EV = 25th-75th percentile multiples
- Somar EVs, deduzir corporate overhead capitalizado
- `Capitalized Overhead = Annual Overhead * Median EBITDA Multiple`
- Dividir por total shares pos-distribution

**Convertible Bond no WACC (Blended Cost):**
```
Cost of Debt Component = Equivalent Non-Convertible Coupon * (1 - Tax Rate)
Cost of Conversion Option = Risk-Free Rate + ERP * Option Beta
Option Beta = Option Elasticity * Levered Beta
Option Elasticity = Option Delta * (Convertible Value If Converted / Market Price)
Option Delta = N(d1) do Black-Scholes
```
A medida que stock price sobe, Blended Cost converge para Cost of Equity.

**Duration e Convexity:**
```
Duration = Sum(PV(CF_t) * t) / Bond Price
YTM approx = (Annual Interest + (Redemption - Price)/Years) / ((Redemption + Price)/2)
```
- Bonds com coupon maior = menor Duration (menos sensivel a rate changes)
- Bonds com maturity maior = maior Duration

**Sensitivity Analysis:**
- WACC (rows) x Terminal Growth (columns)
- Variacao tipica: WACC +/- 1%, g +/- 0.5%
- Football field: ranges de cada metodologia lado a lado

---

## LBO (Advanced)

**Covenant Analysis:**
- Maintenance covenants (Revolvers, Term Loans): limites rigidos (max Debt/EBITDA, min Interest Coverage, min DSCR). Violacao = penalidade, rate increase, repayment demand
- Incurrence covenants (Sub Notes, Mezz): restringem acoes (venda de assets, spinoffs), sem monitoramento continuo
- Avaliar compliance nos cenarios Downside e Extreme Downside
- Calcular "cushion" = % decline em EBITDA antes de violar covenant

**Capital Structure Optimization (hierarquia de custo):**
```
Revolver < TLA < TLB < Senior Unsecured Notes < Sub Notes < Mezz/Preferred < Equity
```
- Se covenant compliance falha no Downside, subir na hierarquia
- TLB = sem amortizacao significativa (resolve DSCR)
- PIK = juros acumulam no principal, reduz cash cost

**Refinancing Mechanics:**
- Call Premiums: schedule decrescente (ex: 105% -> 104% -> 100%)
- Make-Whole Provision = PV dos cash flows perdidos, descontados a T + spread (ex: T+50bps)
- Penalidade AUMENTA quando rates caem (inversamente proporcional)
- `YTW (Yield to Worst) = MIN(YTM, YTC em cada call date)`
- Refinancing so compensa se reducao de coupon supera call premium + custos

**Dividend Recap em LBO:**
- Empresa levanta debt adicional no Year 3-4 para pagar dividendo ao PE sponsor
- Impacto no IRR e pequeno porque: (1) recap e fracao do investimento, (2) debt adicional reduz equity value no exit, (3) maior cash interest
- Impacto no IRR > impacto no MOIC (time value of money)

**Cash Sweep Mechanics:**
```
ECF = EBITDA - Cash Interest - Cash Taxes - CapEx - Delta NWC - Mandatory Amort
Sweep Amount = ECF * Sweep% (tipico 50-75%)
```
- Sweep % step-down com leverage reduction (ex: >4x = 75%, <3x = 25%)

**Returns to Lenders:**
- IRR inclui OID, issuance fees, cash interest, principal repayments, prepayment penalties
- PIK aumenta principal mas nao gera cash intermediario — IRR pior vs cash interest
- Em deals menores, items one-time (OID, penalties) pesam mais no IRR

**Debt Capacity Benchmarks:**
```
Senior Debt / EBITDA: max 4-6x
Total Debt / EBITDA: max 5-7x
Fixed Charge Coverage: > 1.0x minimum
Interest Coverage: > 2.0x minimum
```
