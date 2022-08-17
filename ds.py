import random
import numpy as np

def diamond_square(g, r, w, n, per):
  wiggle = w
  g[0][0] = random.randrange(0, r)
  g[0][n-1] = random.randrange(0, r)
  g[n-1][0] = random.randrange(0, r)
  g[n-1][n-1] = random.randrange(0, r)

  distance = int ((n-1) / 2)

  while True:
    #diamond step
    x = 0
    y = 0
    square_centers = [] #keeps track of the square centers for the square step
    while y != n - 1:
      # You can imagine this part as starting in the top left and 
      # Finding every 'square' inside the grid. Round 1 there is only 1.
      # The next round there are 4 squares, and so on.
      mx = x + distance
      my = y + distance
      square_centers.append((mx, my)) #saving for later.
      tl = g[y][x]
      tr = g[y][x + 2 * distance]
      bl = g[y + 2 * distance][x]
      br = g[y + 2 * distance][x + 2 * distance]
      avg = ((tl + tr + bl + br) / 4) + random.uniform(-1 * wiggle, wiggle)
      
      #Caps the value between 0 and the max.
      if avg >= r:
        avg = r
      if avg <= 0:
        avg = 0

      g[my][mx] = avg
      x += 2 * distance
      if x == n - 1: # If you've gotten all the way to the right edge
        y += 2 * distance  #Move the y down to the next 'row' of squares
        x = 0

    #square step
    diamond_centers = []

    for c in square_centers:
      left =   (c[0] - distance, c[1])
      top =    (c[0], c[1] - distance)
      right =  (c[0] + distance, c[1])
      bottom = (c[0], c[1] + distance)
      diamond_centers.append(left)
      diamond_centers.append(right)
      diamond_centers.append(top)
      diamond_centers.append(bottom)
    diamond_centers = set(diamond_centers)

    for d in diamond_centers:
      points = []
      left = (d[0] - distance, d[1])
      right = (d[0] + distance, d[1])
      bottom = (d[0], d[1] + distance)
      top = (d[0], d[1] - distance)
      # Everything below is for the edge cases. If you are on the left edge,
      # you shouldn't add a point off the grid, otherwise you'll get index errors.
      if d[1] == 0:
        points.append(right)
        points.append(left)
        points.append(bottom)
      elif d[1] == n-1:
        points.append(top)
        points.append(right)
        points.append(left)
      elif d[0] == 0:
        points.append(top)
        points.append(right)
        points.append(bottom)
      elif d[0] == n-1:
        points.append(top)
        points.append(left)
        points.append(bottom)
      else:
        points.append(top)
        points.append(right)
        points.append(left)
        points.append(bottom)

      total = 0
      for p in points:
        value = g[p[1]][p[0]]
        total += value
      avg = total / len(points) + random.uniform(-1 * wiggle, wiggle)

      if avg >= r:
        avg = r
      if avg <= 0:
        avg = 0
      g[d[1]][d[0]] = avg

    if distance == 1:
      break
    distance = int(distance // 2)
    wiggle = wiggle * per

  return g