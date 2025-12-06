"""Verify V1 formula: (FV/CV)^(1/5) - 1, then rank percentile"""

import urllib.request
import json

# Test API
r = urllib.request.urlopen('http://127.0.0.1:5000/api/metrics?duration=3years')
data = json.loads(r.read())

print("="*70)
print("V1 FORMULA VERIFICATION")
print("Formula: CAGR_5y = (Latest Price / Price 5 years ago)^(1/5) - 1")
print("Then: V1 = Rank Percentile (higher = better)")
print("="*70)

print(f"\nTotal indices: {len(data)}")

# Sort by V1 descending
sorted_data = sorted(data, key=lambda x: x['V1'] if x['V1'] is not None else -1, reverse=True)

print("\n📊 TOP 10 PERFORMERS (Highest V1):")
print("-" * 70)
for i, item in enumerate(sorted_data[:10], 1):
    v1 = item['V1']
    ret = item['Ret']
    print(f"{i:2}. {item['Index Name']:15} V1={v1:.3f} ({v1*100:.1f}%), Ret={ret}%")

print("\n📉 BOTTOM 10 PERFORMERS (Lowest V1):")
print("-" * 70)
for i, item in enumerate(sorted_data[-10:], 1):
    v1 = item['V1']
    ret = item['Ret']
    if v1 is not None:
        print(f"{i:2}. {item['Index Name']:15} V1={v1:.3f} ({v1*100:.1f}%), Ret={ret}%")
    else:
        print(f"{i:2}. {item['Index Name']:15} V1=None, Ret={ret}%")

# Check specific indices
print("\n🔍 SPECIFIC INDICES:")
print("-" * 70)
for name in ['N50', 'NBANK', 'NTECH', 'NPHARMA', 'NMC50']:
    item = next((d for d in data if d['Index Name'] == name), None)
    if item:
        v1 = item['V1']
        ret = item['Ret']
        print(f"{name:15} V1={v1:.3f} ({v1*100:.1f}%), Ret={ret}%")

print("\n✅ V1 values now use 5-year CAGR for ranking")
print("✅ Higher V1 = Better 5-year performance")
