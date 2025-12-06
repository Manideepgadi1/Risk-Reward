import urllib.request
import json

r = urllib.request.urlopen('http://127.0.0.1:5000/api/metrics?duration=3years')
data = json.loads(r.read())
print(f"Total indices: {len(data)}")
print("\nFirst 15 indices:")
for d in data[:15]:
    print(f"  {d['Index Name']}: V1={d['V1']}, Ret={d['Ret']}, Mom={d.get('Momentum')}")
