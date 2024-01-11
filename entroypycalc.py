import math

def calculate_entropy(dataset):
    total_samples = len(dataset)
    class_labels = set(sample[0] for sample in dataset)
    entropy = 0
    for label in class_labels:
        class_prob = sum(1 for sample in dataset if sample[0] == label) / total_samples
        entropy -= class_prob * math.log2(class_prob)
    return entropy

def calculate_information_gain(dataset, property_index):
    property_values = set(sample[property_index] for sample in dataset)
    total_samples = len(dataset)
    entropy_s = calculate_entropy(dataset)
    conditional_entropy = 0
    for value in property_values:
        subset = [sample for sample in dataset if sample[property_index] == value]
        subset_size = len(subset)
        conditional_entropy += subset_size / total_samples * calculate_entropy(subset)
    information_gain = entropy_s - conditional_entropy
    return information_gain

# Given dataset
dataset = [
    [1, "yes", "rainy", "big", "big"],
    [2, "yes", "rainy", "big", "small"],
    [3, "no", "rainy", "med", "big"], 
    [4, "no", "rainy", "med", "small"],
    [5, "yes", "sunny", "big", "big"],
    [6, "yes", "sunny", "big", "small"],
    [7, "yes", "sunny", "med", "big"], 
    [8, "yes", "sunny", "med", "big"], 
    [9, "yes", "sunny", "med", "small"],
    [10, "yes", "sunny", "no", "small"],
    [11, "no", "sunny", "no", "big"],
    [12, "no", "rainy", "med", "big"],
    [13, "no", "rainy", "no", "big"],
    [14, "no", "rainy", "no", "big"],
    [15, "no", "rainy", "no", "small"],
    [16, "no", "rainy", "no", "small"],
    [17, "yes", "sunny", "big", "big"],
    [18, "no", "sunny", "big", "small"],
    [19, "no", "sunny", "med", "big"],
    [20, "no", "sunny", "med", "big"]
]


# Problem A: Calculate entropy E (Sail | Outlook)
outlook_index = 1
outlook_values = set(sample[outlook_index] for sample in dataset)
entropy_sail_outlook = 0
for value in outlook_values:
    subset = [sample for sample in dataset if sample[outlook_index] == value]
    probability = len(subset) / len(dataset)
    entropy_sail_outlook += probability * calculate_entropy(subset)
print(f"Entropy E (Sail | Outlook): {entropy_sail_outlook:.4f}")

# Problem B: Calculate information gain (IG) for Outlook
information_gain_outlook = calculate_information_gain(dataset, outlook_index)
print(f"Information Gain (Outlook): {information_gain_outlook:.4f}")

# Problem C: Using information gain as a metric, determine the property for splitting at the root of the tree
property_indices = [1, 2, 3]
information_gains = {}
for index in property_indices:
    information_gain = calculate_information_gain(dataset, index)
    information_gains[index] = information_gain
splitting_property_index = max(information_gains, key=information_gains.get)
print(f"Splitting property at the root: Property {splitting_property_index} (Information Gain: {information_gains[splitting_property_index]:.4f})")

# Problem D: Calculate information gain for changed dataset
changed_dataset = [
    [1, "yes", "rainy", "big", "big"],
    [2, "yes", "rainy", "big", "small"],
    [3, "no", "rainy", "med", "big"], 
    [4, "no", "rainy", "med", "small"],
    [5, "yes", "sunny", "big", "big"],
    [6, "yes", "sunny", "big", "small"],
    [7, "yes", "sunny", "med", "big"], 
    [8, "yes", "sunny", "med", "big"], 
    [9, "yes", "sunny", "med", "small"],
    [10, "yes", "sunny", "no", "small"],
    [11, "no", "sunny", "no", "big"],
#    [12, "no", "rainy", "med", "big"],
    [13, "no", "rainy", "no", "big"],
#    [14, "no", "rainy", "no", "big"],
    [15, "no", "rainy", "no", "small"],
  #  [16, "no", "rainy", "no", "small"],
  #  [17, "yes", "sunny", "big", "big"],
    [18, "no", "sunny", "big", "small"],
    [19, "no", "sunny", "med", "big"],
  #  [20, "no", "sunny", "med", "big"]
]

information_gains_changed = {}
for index in property_indices:
    information_gain = calculate_information_gain(changed_dataset, index)
    information_gains_changed[index] = information_gain
splitting_property_index_changed = max(information_gains_changed, key=information_gains_changed.get)
print(f"Splitting property at the root (changed dataset): Property {splitting_property_index_changed} (Information Gain: {information_gains_changed[splitting_property_index_changed]:.4f})")
