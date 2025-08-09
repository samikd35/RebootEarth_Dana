#!/usr/bin/env python3
"""
Fix the broken scalers by creating new ones based on realistic agricultural data ranges
"""

import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler, StandardScaler

print("🔧 FIXING BROKEN SCALERS")
print("=" * 30)

# Create realistic training data based on actual agricultural ranges
# This simulates the data the original model should have been trained on
np.random.seed(42)  # For reproducibility

# Generate realistic agricultural data
n_samples = 1000

# Realistic ranges for each feature
nitrogen_data = np.random.uniform(0, 140, n_samples)      # 0-140 kg/ha
phosphorus_data = np.random.uniform(5, 145, n_samples)    # 5-145 kg/ha  
potassium_data = np.random.uniform(5, 205, n_samples)     # 5-205 kg/ha
temperature_data = np.random.uniform(8.8, 43.7, n_samples) # 8.8-43.7°C
humidity_data = np.random.uniform(14.3, 99.9, n_samples)   # 14.3-99.9%
ph_data = np.random.uniform(3.5, 9.9, n_samples)          # 3.5-9.9 pH
rainfall_data = np.random.uniform(20.2, 298.6, n_samples)  # 20.2-298.6 mm

# Combine into training data
training_data = np.column_stack([
    nitrogen_data, phosphorus_data, potassium_data,
    temperature_data, humidity_data, ph_data, rainfall_data
])

print(f"Generated {n_samples} realistic agricultural samples")
print("Feature ranges:")
for i, name in enumerate(['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall']):
    print(f"  {name}: {training_data[:, i].min():.1f} to {training_data[:, i].max():.1f}")

# Create and fit new scalers
print("\n🔧 Creating new MinMax scaler...")
new_minmax_scaler = MinMaxScaler()
new_minmax_scaler.fit(training_data)

print("🔧 Creating new Standard scaler...")
# Apply MinMax first, then Standard (as the original pipeline does)
minmax_transformed = new_minmax_scaler.transform(training_data)
new_standard_scaler = StandardScaler()
new_standard_scaler.fit(minmax_transformed)

# Test the new scalers
print("\n🧪 Testing new scalers...")
test_input = np.array([[50, 50, 50, 25, 70, 6.5, 100]]).reshape(1, -1)
print(f"Test input: {test_input[0]}")

minmax_result = new_minmax_scaler.transform(test_input)
print(f"After new MinMax: {minmax_result[0]}")

std_result = new_standard_scaler.transform(minmax_result)
print(f"After new Standard: {std_result[0]}")

# Verify the results are reasonable (should be roughly between -3 and 3 for standard scaler)
if np.all(np.abs(std_result[0]) < 5):
    print("✅ New scalers produce reasonable results!")
else:
    print("⚠️  New scalers may still have issues")

# Save the new scalers
print("\n💾 Saving new scalers...")
with open('minmaxscaler_fixed.pkl', 'wb') as f:
    pickle.dump(new_minmax_scaler, f)

with open('standscaler_fixed.pkl', 'wb') as f:
    pickle.dump(new_standard_scaler, f)

print("✅ New scalers saved as:")
print("  - minmaxscaler_fixed.pkl")
print("  - standscaler_fixed.pkl")

print("\n🔄 To use the fixed scalers, update your integration_bridge.py:")
print("  Change 'minmaxscaler.pkl' to 'minmaxscaler_fixed.pkl'")
print("  Change 'standscaler.pkl' to 'standscaler_fixed.pkl'")