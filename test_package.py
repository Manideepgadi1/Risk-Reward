"""Test the installed package"""

from riskapp import RiskRewardAPI

# Initialize API
api = RiskRewardAPI()

# Get metrics
metrics = api.get_metrics(duration='3years')

print(f"✅ Package working! Total indices: {len(metrics)}")
print("\n📊 Top 5 by V1 (Higher = Better):")

# Sort by V1 and get top 5
top5 = sorted(metrics, key=lambda x: x['V1'] or 0, reverse=True)[:5]

for i, m in enumerate(top5, 1):
    print(f"{i}. {m['Index Name']}: V1={m['V1']}, Ret={m['Ret']}%, Risk={m['Risk']}")

# Get list of all indices
all_indices = api.get_available_indices()
print(f"\n📋 Total available indices: {len(all_indices)}")
print(f"First 10: {all_indices[:10]}")

# Get specific index data
n50_data = api.get_index_data('N50')
print(f"\n📈 N50 latest price: {n50_data.iloc[-1]:.2f}")
print(f"   Data points: {len(n50_data)}")

print("\n✅ All tests passed! Package is ready to use in other projects.")
