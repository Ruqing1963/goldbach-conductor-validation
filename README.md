# The True Conductor of Goldbach–Frey Curves

**Paper #12 in the Titan Project series**

Computational validation of the conductor proxy via Magma genus-2 conductor computations.

## Key Result

For the Goldbach–Frey curve C: y² = x(x² − p²)(x² − q²), p + q = 2N:

```
Cond_odd(Jac(C)) = [rad_odd(p) · rad_odd(q) · rad_odd(M) · rad_odd(|p−q|)]²
```

- **All odd conductor exponents = 2** (tame semistable), verified across 10 Magma computations.
- The proxy from Papers #8–10 is an **exact algebraic subterm** of the true conductor.
- The proxy–true gap equals 2·log(rad_odd_new(|p−q|))/log(2N) exactly (10/10 match).

## Repository Structure

```
├── paper/
│   ├── True_Conductor_Validation.tex    LaTeX source
│   └── True_Conductor_Validation.pdf    Compiled paper (6 pages)
├── figures/
│   ├── fig_conductor.pdf                Proxy vs true conductor + gap prediction
│   ├── fig_conductor.png
│   ├── fig_exponents.pdf                Universal f_r = 2 across all curves
│   └── fig_exponents.png
├── data/
│   ├── magma_conductors.txt             Raw Magma Conductor() output (10 cases)
│   └── sage_pointcounts.txt             SageMath point-counting cross-validation
├── scripts/
│   ├── goldbach_batch_simple.m          Magma batch script (10 test cases)
│   ├── goldbach_conductor_manual.sage   Sage manual point counting at bad primes
│   ├── fig_conductor.py                 Figure generation and analysis
│   ├── kani_rosen_invalid.sage          Kani-Rosen splitting (INVALID, kept for record)
│   └── conductor_elliptic_split.sage    Elliptic splitting (INVALID, kept for record)
├── README.md
├── LICENSE
└── .gitignore
```

**Note on invalid scripts:** `kani_rosen_invalid.sage` and `conductor_elliptic_split.sage`
attempted to split the genus-2 Jacobian as E1 × E2. Euler-factor verification
(20 primes) showed 35–50% mismatch rates, proving the splitting is invalid.
These files are kept for transparency.

## Series Context

| # | Paper | DOI |
|---|-------|-----|
| 8 | Goldbach Mirror II | [10.5281/zenodo.18719056](https://zenodo.org/records/18719056) |
| 9 | Algebraic Vacuum | [10.5281/zenodo.18720040](https://zenodo.org/records/18720040) |
| 11 | Ternary Conductor Boundary | [10.5281/zenodo.18727994](https://zenodo.org/records/18727994) |
| **12** | **True Conductor Validation** | *this paper* |

## License

MIT
