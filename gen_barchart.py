import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# https://www.python-graph-gallery.com/11-grouped-barplot

df = pd.read_csv("f1-engines-scores.csv", header=0)
df.drop(columns=["domain"], inplace=True)
data = df.values
# data = data.reshape((3, -1, 4))
data = data.T.reshape((3, 4, -1))

print(data[0])

domains = ["win", "cook", "wiki"]
engines = ["Curie", "Babbage", "Ada"]
barWidth = 0.18

bars1 = data[0][0]
bars2 = data[0][1]
bars3 = data[0][2]
bars4 = data[0][3]

fig, ax = plt.subplots()

r1 = np.arange(3)
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]

plt.bar(r1, bars1, color='#b4ffff', width=barWidth, edgecolor='white', label='1-example')
plt.bar(r2, bars2, color='#80deea', width=barWidth, edgecolor='white', label='2-examples')
plt.bar(r3, bars3, color='#4bacb8', width=barWidth, edgecolor='white', label='3-examples')
plt.bar(r4, bars4, color='#005662', width=barWidth, edgecolor='white', label='4-examples')

plt.ylim([0, 0.8])
plt.xlabel('Engine', fontweight='bold')
plt.title("WHS F1 Scores")
plt.xticks([r + barWidth*3/2 for r in range(len(bars1))], engines)
plt.legend()


plt.show()












################################################
# fig, ax = plt.subplots()
# width = 0.5  # the width of the bars
#
# x = np.arange(4)
# for dom_data, dom_name in zip(data, engines):
#     rects1 = plt.bar(x - width/, dom_data[0], width, label=dom_name)
    # rects2 = ax.bar(dom_data[0], dom_data[1], width, label='2')
    # rects3 = ax.bar(dom_data[0] + width, dom_data[0], width, label='3')
    # break

    # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('F1 Scores')
# ax.set_title('Windows Help')
# # ax.set_xticks()
# ax.set_xticklabels(domains)
# ax.legend()
#
# # ax.set_ylabel(rects1, padding=3)
# # ax.bar_label(rects2, padding=3)
# # ax.bar_label(rects3, padding=3)
#
# fig.tight_layout()
# plt.show()
