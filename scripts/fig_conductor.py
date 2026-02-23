import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math

def rad_odd(n):
    if n == 0: return 1
    n = abs(n)
    while n % 2 == 0: n //= 2
    result = 1; temp = n; d = 3; seen = set()
    while d * d <= temp:
        if temp % d == 0:
            seen.add(d)
            while temp % d == 0: temp //= d
        d += 2
    if temp > 1: seen.add(temp)
    for p in seen: result *= p
    return result

def odd_prime_factors(n):
    if n == 0: return set()
    n = abs(n); factors = set()
    while n % 2 == 0: n //= 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0: n //= d
        d += 2
    if n > 1: factors.add(n)
    return factors

magma_data = [
    (3,  7,   {2:8, 3:2, 5:2, 7:2}),
    (7,  23,  {2:4, 3:2, 5:2, 7:2, 23:2}),
    (11, 19,  {2:7, 3:2, 5:2, 11:2, 19:2}),
    (13, 17,  {2:8, 3:2, 5:2, 13:2, 17:2}),
    (3,  17,  {2:8, 3:2, 5:2, 7:2, 17:2}),
    (7,  19,  {2:8, 3:2, 7:2, 13:2, 19:2}),
    (3,  37,  {2:7, 3:2, 5:2, 17:2, 37:2}),
    (7,  41,  {2:4, 3:2, 7:2, 17:2, 41:2}),
    (7,  53,  {2:8, 3:2, 5:2, 7:2, 23:2, 53:2}),
    (11, 37,  {2:4, 3:2, 11:2, 13:2, 37:2}),
]

records = []
for p, q, fac in magma_data:
    twoN = p + q; M = twoN // 2; diff = abs(p - q)
    cond_odd = 1
    for r, e in fac.items():
        if r != 2: cond_odd *= r**e
    rho_true = math.log(cond_odd) / math.log(twoN)
    proxy_rad = rad_odd(p) * rad_odd(q) * rad_odd(M)
    rho_proxy = 2 * math.log(proxy_rad) / math.log(twoN) if proxy_rad > 1 else 0
    known = odd_prime_factors(p) | odd_prime_factors(q) | odd_prime_factors(M)
    new_primes = odd_prime_factors(diff) - known
    gap = rho_true - rho_proxy
    predicted_gap = sum(2 * math.log(r) / math.log(twoN) for r in new_primes) if new_primes else 0
    records.append({
        'p': p, 'q': q, 'twoN': twoN, 'diff': diff,
        'rho_true': rho_true, 'rho_proxy': rho_proxy,
        'gap': gap, 'predicted_gap': predicted_gap,
        'has_new': len(new_primes) > 0, 'new_primes': new_primes
    })

# ═══════════════════════════════════════════════════════════════════
# FIGURE 2
# ═══════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))

# --- Panel (a) ---
ax = axes[0]
mn, mx = 2.6, 6.5
ax.plot([mn, mx], [mn, mx], 'k--', lw=1, alpha=0.3)

for r in records:
    c = '#CC3333' if r['has_new'] else '#2255BB'
    m = 's' if r['has_new'] else 'o'
    ax.scatter(r['rho_proxy'], r['rho_true'], c=c, marker=m, s=90,
              edgecolors='black', linewidths=0.6, zorder=5)

# Carefully placed labels — each tested manually
offsets_a = {
    # Blue (no new primes) — spread along diagonal
    (3, 7):   (10, -16),      # bottom, alone
    (7, 23):  (10, -16),      # middle, alone
    (11, 19): (10, 8),        # above (13,17)
    (13, 17): (10, -16),      # below (11,19)
    # Red (new primes) — clustered upper-left, need careful separation
    (3, 17):  (-72, -18),     # far left-below
    (7, 41):  (-72, 2),       # far left-center
    (3, 37):  (10, 14),       # right-above
    (11, 37): (10, -18),      # right-below
    (7, 19):  (10, -16),      # alone in middle
    (7, 53):  (10, 8),        # alone at top
}

for r in records:
    key = (r['p'], r['q'])
    ox, oy = offsets_a.get(key, (10, -12))
    color = '#CC3333' if r['has_new'] else '#2255BB'
    use_arrow = abs(ox) > 30
    props = dict(arrowstyle='-', color='#BBBBBB', lw=0.6, shrinkB=2) if use_arrow else None
    ax.annotate(f"({r['p']}, {r['q']})", (r['rho_proxy'], r['rho_true']),
               fontsize=8, textcoords="offset points", xytext=(ox, oy),
               color=color, fontweight='bold', arrowprops=props)

# Gap arrow for (3,17)
ex = records[4]
ax.annotate('', xy=(ex['rho_proxy'], ex['rho_true']),
           xytext=(ex['rho_proxy'], ex['rho_proxy']),
           arrowprops=dict(arrowstyle='<->', color='#CC3333', lw=1.8))
ax.text(ex['rho_proxy'] + 0.12, (ex['rho_proxy'] + ex['rho_true'])/2,
       r'$\delta$', fontsize=13, color='#CC3333', va='center', fontweight='bold')

legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#2255BB',
           markersize=9, markeredgecolor='k', markeredgewidth=0.6,
           label=r'$|p{-}q|$: no new odd primes ($\delta=0$)'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='#CC3333',
           markersize=9, markeredgecolor='k', markeredgewidth=0.6,
           label=r'$|p{-}q|$: introduces new odd primes ($\delta>0$)'),
    Line2D([0], [0], color='k', linestyle='--', lw=1, alpha=0.3,
           label=r'$\rho_{\rm proxy}=\rho_{\rm true}$'),
]
ax.legend(handles=legend_elements, fontsize=8, loc='lower right')
ax.set_xlabel(r'$\rho_{\rm proxy}$', fontsize=13)
ax.set_ylabel(r'$\rho_{\rm true}$', fontsize=13)
ax.set_title(r'(a) Proxy vs True Conductor Ratio', fontsize=13)
ax.set_xlim(mn, mx); ax.set_ylim(mn, mx)
ax.set_aspect('equal')
ax.grid(True, alpha=0.15)

# --- Panel (b) ---
ax2 = axes[1]
ax2.plot([-0.15, 1.9], [-0.15, 1.9], 'k--', lw=1, alpha=0.3)

zero_cases = [r for r in records if r['predicted_gap'] < 0.01]
nonzero_cases = [r for r in records if r['predicted_gap'] >= 0.01]

# Zero cluster
if zero_cases:
    ax2.scatter([r['predicted_gap'] for r in zero_cases],
               [r['gap'] for r in zero_cases],
               c='#228833', s=90, edgecolors='black', linewidths=0.6, zorder=5)
    combined = ",  ".join(f"({r['p']},{r['q']})" for r in zero_cases)
    ax2.annotate(combined, (0.0, 0.0), fontsize=7, textcoords="offset points",
                xytext=(16, -20), color='#228833', fontweight='bold',
                arrowprops=dict(arrowstyle='-', color='#AAAAAA', lw=0.5))

# Non-zero points
offsets_b = {
    (7, 19):  (12, -16),       # alone
    (3, 17):  (12, -16),       # bottom of upper cluster
    (11, 37): (-68, -4),       # left
    (3, 37):  (12, 8),         # right-above
    (7, 41):  (-60, 10),       # left-above
    (7, 53):  (12, 8),         # top, alone
}
for r in nonzero_cases:
    ax2.scatter(r['predicted_gap'], r['gap'], c='#228833', s=90,
               edgecolors='black', linewidths=0.6, zorder=5)
    key = (r['p'], r['q'])
    ox, oy = offsets_b.get(key, (12, -12))
    use_arrow = abs(ox) > 30
    props = dict(arrowstyle='-', color='#AAAAAA', lw=0.5) if use_arrow else None
    ax2.annotate(f"({r['p']}, {r['q']})", (r['predicted_gap'], r['gap']),
                fontsize=8, textcoords="offset points", xytext=(ox, oy),
                color='#228833', fontweight='bold', arrowprops=props)

ax2.set_xlabel(r'Predicted gap $\delta = \frac{2\ln\,\mathrm{rad}_{\rm odd}^{\rm new}(|p{-}q|)}{\ln(2N)}$', fontsize=11)
ax2.set_ylabel(r'Actual gap $\rho_{\rm true} - \rho_{\rm proxy}$', fontsize=11)
ax2.set_title(r'(b) Gap Prediction: 10/10 Exact Match', fontsize=13)
ax2.set_xlim(-0.15, 1.9); ax2.set_ylim(-0.15, 1.9)
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.15)

plt.tight_layout(w_pad=3)
plt.savefig('/home/claude/paper12/figures/fig_conductor.pdf', dpi=300, bbox_inches='tight')
plt.savefig('/home/claude/paper12/figures/fig_conductor.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 2 done.")

# ═══════════════════════════════════════════════════════════════════
# FIGURE 1: exponents
# ═══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 4.5))
all_pts = []; case_labels = []
for i, (p, q, fac) in enumerate(magma_data):
    case_labels.append(f"({p},{q})")
    for r, e in sorted(fac.items()):
        if r > 2: all_pts.append((i, r, e))

ax.scatter([pt[0] for pt in all_pts], [pt[2] for pt in all_pts],
          s=60, c='#2255BB', edgecolors='black', linewidths=0.5, zorder=5)
ax.axhline(y=2, color='#CC3333', linestyle='--', lw=2, alpha=0.7, label=r'$f_r = 2$ (semistable)')
for x, y, r in all_pts:
    ax.annotate(str(r), (x, y), fontsize=6.5, textcoords="offset points",
               xytext=(0, 7), ha='center', color='#666666')
ax.set_xticks(range(len(case_labels)))
ax.set_xticklabels(case_labels, rotation=45, fontsize=9, ha='right')
ax.set_ylabel(r'Conductor exponent $f_r$', fontsize=12)
ax.set_title(r'Odd conductor exponents across 10 Goldbach--Frey curves', fontsize=12)
ax.set_ylim(0, 4); ax.legend(fontsize=10); ax.grid(True, alpha=0.15, axis='y')
plt.tight_layout()
plt.savefig('/home/claude/paper12/figures/fig_exponents.pdf', dpi=300, bbox_inches='tight')
plt.savefig('/home/claude/paper12/figures/fig_exponents.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 1 done.")
