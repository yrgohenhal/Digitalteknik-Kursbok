#| label: fig-timing-tff-simple
#| fig-cap: "Förenklat timingdiagram för en T-vippa. Utgången Q växlar tillstånd (toggle) vid varje stigande klockflank där T=1."
#| echo: false

import matplotlib.pyplot as plt
import numpy as np

# Inställningar för tidsaxel (0 till 6 klockcykler)
num_cycles = 6
t = np.linspace(0, num_cycles, 1200)

# 1. Klocksignal (C) - Startar låg (0) och går hög vid 0.5, 1.5...
clk = (np.sin(np.pi * t * 2 - np.pi) > 0).astype(int)

# 2. Toggle-ingång (T) 
t_in = np.zeros_like(t)
t_in[(t > 0.2) & (t < 1.7)] = 1  # T=1 över flanken i Cykel 1 och 2
t_in[(t > 2.2) & (t < 2.8)] = 1  # En glitch i Cykel 3 (missar flanken 2.5)
t_in[(t > 3.2) & (t < 4.7)] = 1  # T=1 över flanken i Cykel 4 och 5

# 3. Logik för T-vippa (Endast utgång Q)
q_out = np.zeros_like(t)
current_q = 0
last_clk = 0

for i in range(len(t)):
    # Detektera positiv klockflank
    if clk[i] == 1 and last_clk == 0:
        # Om T är hög vid flanken, toggla Q
        if t_in[i] == 1:
            current_q = 1 - current_q
    q_out[i] = current_q
    last_clk = clk[i]

# Skapa diagrammet med 3 rader
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
plt.subplots_adjust(hspace=0.4)

def setup_axis(ax, label_text):
    ax.set_ylabel(label_text, fontsize=12, fontweight='bold', rotation=0, labelpad=25, va='center')
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_yticks([0, 1])
    ax.set_ylim(-0.2, 1.3)

# 1. Klocka (C)
ax1.step(t, clk, where='post', color='#2c3e50', linewidth=2)
setup_axis(ax1, '$C$')
ax1.set_title('Timingdiagram: T-vippa', fontsize=14, pad=30, fontweight='bold')

for i in range(num_cycles):
    ax1.text(i + 0.5, 1.45, f"Cykel {i+1}", ha='center', fontsize=10, color='#7f8c8d')
    edge_pos = i + 0.5
    ax1.annotate('', xy=(edge_pos, 1.2), xytext=(edge_pos, -0.1),
                 arrowprops=dict(arrowstyle="->", color='#27ae60', lw=1.5))

# 2. T-ingång
ax2.step(t, t_in, where='post', color='#8e44ad', linewidth=2)
setup_axis(ax2, '$T$')

# 3. Utgång (Q)
ax3.step(t, q_out, where='post', color='#c0392b', linewidth=2.5)
setup_axis(ax3, '$Q$')

# Sätt generisk x-axel
ax3.set_xticks(np.arange(0, num_cycles + 1, 1))
ax3.set_xlabel('Tid (Klockcykler)', fontsize=12, fontweight='bold')

plt.show()