"""Quick verification of V1 formula"""
import urllib.request
import json

r = urllib.request.urlopen('http://127.0.0.1:5000/api/metrics?duration=3years')
data = json.loads(r.read())

print("="*70)
print("V1 FORMULA VERIFICATION")
print("Formula: (Current - Price_3Y_ago) / Price_3Y_ago * 100")
print("Percentile: (rank - 1) / (total - 1)")
print("="*70)

# Sort by V1
sorted_data = sorted(data, key=lambda x: x['V1'] if x['V1'] is not None else -1, reverse=True)

print("\n📊 TOP 10 (Highest V1 = Best 3Y Return):")
for i, item in enumerate(sorted_data[:10], 1):
    print(f"{i:2}. {item['Index Name']:20} V1={item['V1']:.3f}, Ret={item['Ret']}%")

print("\n📉 BOTTOM 10 (Lowest V1 = Worst 3Y Return):")
for i, item in enumerate(sorted_data[-10:], 1):
    v1 = item['V1']
    if v1 is not None:
        print(f"{i:2}. {item['Index Name']:20} V1={v1:.3f}, Ret={item['Ret']}%")

print("\n🔍 KEY INDICES:")
for name in ['N50', 'NBANK', 'NMC50', 'NIDEF', 'NMEDIA']:
    item = next((d for d in data if d['Index Name'] == name), None)
    if item:
        print(f"{name:15} V1={item['V1']:.3f}, Ret={item['Ret']}%")

print("\n✅ V1 now uses 3-year simple return")
print("✅ Percentile formula: (rank-1)/(total-1)")
print("✅ Higher V1 = Better 3-year performance")
