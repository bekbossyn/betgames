def calc(c, n, profit):
  if n == 1:
    x = profit / (c - 1.0)
    print x
    return x
  x0 = calc(c, n - 1, profit)
  x = (profit + x0) / (c - 1.0)
  print x
  return x + x0


