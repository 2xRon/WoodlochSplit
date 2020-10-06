'''
Given a list of expenses, find the minimum numbers of transfers to even expenditures
between participants
'''
from itertools import chain, combinations
from decimal import getcontext, Decimal

def subsets_k(collection, k):
   yield from partition_k(collection, k, k)

def partition_k(collection, min, k):
  if len(collection) == 1:
    yield [ collection ]
    return
  first = collection[0]
  for smaller in partition_k(collection[1:], min - 1, k):
    if len(smaller) > k: continue
    # insert `first` in each of the subpartition's subsets
    if len(smaller) >= min:
      for n, subset in enumerate(smaller):
        yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
    # put `first` in its own subset 
    if len(smaller) < k: yield [ [ first ] ] + smaller

def zero_sum_partitions(collection):
    for k in range(1,len(collection)):
        for partition in subsets_k(collection, k):
            if all(sum(x[1] for x in subset) == 0 for subset in partition):
                yield partition

def most_zero_sum_partitions(participants):
    return sorted(zero_sum_partitions(list(participants.items())), key=len, reverse=True)[0]

def subgroup_transfers(debts):
    # for optimal size subgroups, finds len(debts)-1 transactions
    # transfer is (source, target, value)
    balances = {p:amt for (p,amt) in sorted(debts, key=lambda x: x[1], reverse=True)}
    transactions = list()
    for _ in range(0,len(balances)-1):
        non_zero = [p for p in balances.items() if p[1] != 0]
        first_nonzero = non_zero[0]
        last_nonzero = non_zero[-1]
        transfer_amt = min(abs(first_nonzero[1]), abs(last_nonzero[1]))
        balances[first_nonzero[0]] -= transfer_amt
        balances[last_nonzero[0]] += transfer_amt
        transactions.append((last_nonzero[0],first_nonzero[0],transfer_amt))
    return transactions

def solve(expenditures):
    getcontext().prec = 28
    target = Decimal(sum(expenditures.values()) / len(expenditures))
    net_expenditure = {k:Decimal(v-target) for k,v in expenditures.items()}
    net_expenditure.update({"EXCESS":Decimal(-1  * sum(net_expenditure.values()))})
    transactions = chain(*(subgroup_transfers(grp_debts) for grp_debts in most_zero_sum_partitions(net_expenditure)))
    return target, list(t for t in transactions if t[0] != "EXCESS" and t[1] != "EXCESS")

if __name__ == "__main__":
    participants = {"A":1100, "B":1100, "C":250, "D":71, "E":103, "F":240}
    target, transactions = solve(participants)
    print(f"After all transfers, everyone will have spent ${round(float(target),2)}")
    print("Transactions\n------------------")
    for t in transactions:
        print(f"{t[0]} transfers ${round(float(t[2]),2)} to {t[1]}")
