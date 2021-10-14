import math
def combos(wordSet, sentences):
  bank = {}
  for word in wordSet:
    order = list(word)
    order.sort()
    bank[tuple(order)] = bank.get(tuple(order),0) + 1
  total = 0
  for ana in bank:
    total += math.factorial(bank[ana])

  return total

print(check([2,1,2,1,3], 2))

