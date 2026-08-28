import pandas as pd

from reconciliation import reconcile

internal = pd.read_csv("internal.csv")
external = pd.read_csv("external.csv")

results, internal_duplicates, external_duplicates = reconcile(internal, external)

print("Reconcile Results : " ,results["status"].value_counts())

print(results)

print(internal_duplicates)

print(external_duplicates)