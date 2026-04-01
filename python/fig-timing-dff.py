#| label: fig-timing-dff-final-v2
#| fig-cap: "Timingdiagram för en Master-Slave D-vippa. Notera hur Q går låg i cykel 5 eftersom D fallit innan klockflanken."
#| echo: false

import matplotlib.pyplot as plt
import numpy as np

# Inställningar för tidsaxel (0 till 6 klockcykler)
num_cycles = 6
t = np.linspace(0, num_cycles, 1200)

# 1. Klocksignal (C) - Startar låg (0) och går hög vid 0.5, 1.5...
clk = (np.sin(np.pi * t * 2 - np.pi) > 0).astype(int)
clk_inv = 1 - clk

# 2. Data (D) - Justerad för att gå låg i cykel 5
d = np.zeros_like(t)
d[(t > 0.2) & (t < 1.7)] = 1  # Täcker flanken i Cykel 1 (0.5)
d[(t > 2.2) & (t < 2.8)] = 1  # Glitch i Cykel 3 (missar flanken 2.5)
d[(t > 3.2) & (t < 4.3)] = 1  # Täcker flanken i Cykel 4 (3.5) men slutar före flanken i Cykel 5 (4.5)

# 3. Logik för Master-latch och Slave-latch
q_master = np.zeros_like(t)
q_slave = np.zeros_like(t)
current_m = 0
current_s = 0

for i in range(len(t)):
    # Master-latch är transparent när C=0
    if clk[i] == 0:
        current_m = d[i]
    q_master[i] = current_m
    
    # Slave-latch (Q) är transparent när C=1
    if clk[i] == 1:
        current_s = q_master[i]
    q_slave[i] = current_s

# Skapa diagrammet
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(10, 11), sharex=True)
plt.subplots_adjust(hspace=0.4)

# Funktion för att snygga till axlar med enhetlig stil
def setup_axis(ax, label_text):
    ax.set_ylabel(label_text, fontsize=12, fontweight='bold', rotation=0, labelpad=25, va='center')
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_yticks([0, 1])
    ax.set_ylim(-0.2, 1.3)

# Rita signaler
ax1.step(t, clk, where='post', color='#2c3e50', linewidth=2)
setup_axis(ax1, '$C$')
ax1.set_title('Timingdiagram: Master-Slave D-vippa', fontsize=14, pad=30, fontweight='bold')

# Markera klockcykler och sätt pilar på stigande flanker
for i in range(num_cycles):
    ax1.text(i + 0.5, 1.45, f"Cykel {i+1}", ha='center', fontsize=10, color='#7f8c8d')
    edge_pos = i + 0.5
    ax1.annotate('', xy=(edge_pos, 1.2), xytext=(edge_pos, -0.1),
                 arrowprops=dict(arrowstyle="->", color='#27ae60', lw=1.5))

ax2.step(t, clk_inv, where='post', color='#95a5a6', linewidth=1.5, linestyle='--')
setup_axis(ax2, r'$\overline{C}$')

ax3.step(t, d, where='post', color='#2980b9', linewidth=2)
setup_axis(ax3, '$D$')

ax4.step(t, q_master, where='post', color='#f39c12', linewidth=2)
setup_axis(ax4, '$Q_M$')

ax5.step(t, q_slave, where='post', color='#c0392b', linewidth=2.5)
setup_axis(ax5, '$Q$')

# Sätt generisk x-axel
ax5.set_xticks(np.arange(0, num_cycles + 1, 1))
ax5.set_xlabel('Tid (Klockcykler)', fontsize=12, fontweight='bold')

plt.show()