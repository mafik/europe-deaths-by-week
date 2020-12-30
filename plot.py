#!/usr/bin/env python3

import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import colorsys
from iso3166 import countries

file = open('demo_r_mwk_ts.tsv', newline='')

data = csv.reader(file, delimiter='\t')

header = None

fig, axs = plt.subplots(6, 6)
fig.set_size_inches(32, 24)
fig.suptitle('Deaths per week by country')

ax_i = 0
ax_j = 0
  
x = list(range(1, 54))

for row in data:
  if not header:
    header = row
    continue
  gender, unit, region = row[0].split(',')
  if gender != 'T': continue
  print(region)
  if region == 'AD': continue  # Andorra is just too small
  if region == 'EL': region = 'GR'
  if region == 'UK': region = 'GB'
  y = defaultdict(lambda: [None] * 53)
  
  for i in range(1, len(row)):
    year, _, week = header[i].partition('W')
    year = int(year)
    week = int(week) - 1
    if week > 52: week = 52
    val = row[i].strip()
    if val.endswith('p'):
      val = val[:-1].strip()
    if val == ':':
      val = None
    else:
      val = int(val)
    if val:
      y[year][week] = val
  
  
  ax = axs[ax_i][ax_j]
  ax_i += 1
  if ax_i >= 6:
    ax_i = 0
    ax_j += 1
  ax.set_title(countries.get(region).name)
  ax.set_xticks([1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53])
  
  first_year = 2000
  last_year = max(year for year in y.keys())
  
  for year in range(first_year, last_year + 1):
    series = y[year]
    sat = (year - first_year + 3) / (last_year - first_year + 3)
    if year != last_year: sat /= 2
    r, g, b = colorsys.hsv_to_rgb(1, sat, 1)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    ax.plot(x, series, color = f'#{r:02x}{g:02x}{b:02x}', label=str(year))
  ax.set_ylim(ymin=0)

handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc=(0.40, 0.92), ncol=7)

fig.savefig('Europe_Deaths_by_Week.png')
plt.close()