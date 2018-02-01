import csv
import math

#globals
#index of classification_attribute wihtin csv file
class_attr = 5
examples = []
attributes = []
tree = [[]]
root = 0

def build_tree(examples, classification_attribute, attributes):
    best_attribute = id3(examples, attributes, classification_attribute)
    Decision_tree = {best: {}}
    for i in find_unique_classifications(examples, best_attribute, attributes):
        next_attributes = attributes[:]
        next_attributes.pop(best_attribute)
        next_examples = find_new_examples(examples, best_attribute, attributes, i)
        next_sub_tree = build_tree(next_examples, classification, next_attributes)
        Decision_tree[best_attribute][i] = next_sub_tree
    return Decision_tree


def find_unique_classifications(examples, attribute, attributes):

    values = get_values(examples, attribute,attributes)
    final_classifications = list(set(values))

    return final_classifications


def get_frequencies(examples, attribute, attributes):

    frequency_dict = {}
    classifications = find_unique_classifications(examples, attribute, attributes)
    values = get_values(examples, attribute, attributes)

    for i in classifications:
        frequency_dict.update({i:0})

    for j in classifications:
        for i in range(0, len(values)):
            if values[i] == j:
                frequency_dict[j] +=1
    
    return frequency_dict
        

def get_set_entropy(examples, classification_attribute,attributes):
    entropy = 0.0
    frequencies= get_frequencies(examples, classification_attribute, attributes)
    total = sum(frequencies.values())
    for key in frequencies.keys():
        if frequencies[key] == 0:
            entropy +=0
        else:
            entropy += (-frequencies[key]/total) * (math.log(frequencies[key]/total, 2))
    return entropy 

def get_entropy(examples, subset_label, classification_attribute, attribute, attributes):

    set_frequencies= get_frequencies(examples, classification_attribute, attributes)
    entropy = 0.0
    subset_target_freqs = get_target_frequencies(examples, subset_label, classification_attribute, attributes)
    total = sum(subset_target_freqs.values())
    for key in subset_target_freqs.keys():
        if subset_target_freqs[key] == 0:
            entropy +=0
        else:
            entropy += (-subset_target_freqs[key]/total) * (math.log(subset_target_freqs[key]/total, 2))

    print("entropy:")
    print(entropy)
    return entropy

def get_target_frequencies(examples, subset_label, classification_attribute, attributes):

    print("hello")
    print(subset_label)
    frequencies= get_frequencies(examples, classification_attribute, attributes)
    target_frequencies={}
    target_classifications = find_unique_classifications(examples, classification_attribute, attributes)
    target = attributes.index(classification_attribute)

    for i in target_classifications:
        target_frequencies.update({i:0})

    print(target_frequencies)
        
    for i in range(0, len(examples)):
        for j in range(0, len(examples[i])):
            if examples[i][j] == subset_label:
                for key in target_frequencies.keys():
                    if examples[i][target] == key:
                        target_frequencies[key]+=1
    print(target_frequencies)

    return(target_frequencies)


# returns the values of the attribute given
def get_values(examples, attribute, attributes):
    x = 0
    values = [None] * (len(examples) - 1)
    index = attributes.index(attribute)

    for j in range(0, (len(examples) - 1)):
        values[j] = examples[j][index]
    values.remove(values[0])

    return values


def gain(examples,classification_attribute, attributes, i):

    frequency_dict = get_frequencies(examples, i, attributes)
    total_element_gain = 0.0
    set_entropy = get_set_entropy(examples, classification_attribute, attributes)
    attribute_entropy = 0.0
    total_values = sum(frequency_dict.values())

    for j in frequency_dict.keys():
        probability = frequency_dict[j]/total_values
        attribute_entropy += probability * get_entropy(examples, j, classification_attribute, i, attributes)

    total_element_gain = set_entropy - attribute_entropy
    print(total_element_gain)

    return total_element_gain

def best_attribute(examples, classification_attribute, attributes):

    max_info_gain = 0.0
    best_attr = attributes[0]
    #calculate the info gain for each attibute and choose the highest
    for attribute in attributes:
        attr_gain = gain(examples, classification_attribute, attributes, attribute)
        if (attr_gain > max_info_gain) and (attribute != classification_attribute):
            max_info_gain = attr_gain
            best_attr = attribute

    print("best: ")
    print(best_attr)

    return best_attr

                 
def id3(examples, classification_attribute, attributes):

    global root
    positive = check_labels(examples)[0]
    negative = check_labels(examples)[1]
    if positive == len(examples) - 1:
        tree[root] = 'Yes'
        return tree
    elif negative == len(examples) - 1:
        tree[root] = 'No'
        return tree
    elif len(attributes) == 0:
        tree[root] = 'Yes' if positive > negative else 'No'
        return tree
    else:
        best_attr = best_attribute(examples, classification_attribute, attributes)
        tree[root] = best_attr
        root = root + 1
        values = get_values(examples, best_attr, attributes)
        for value in values:
            branch_examples = get_branches(examples, attributes, best_attr, value)
            if len(branch_examples) == 0:
                positive = check_labels(examples)[0]
                negative = check_labels(examples)[1]
                tree[root] = 'Yes' if positive > negative else 'No'
            else:
                attributes.remove(best_attr)
                tree[root] = id3(branch_examples, classification_attribute, attributes)


def get_branches(examples, attributes, best_attr, value):
    branches = []
    index = attributes.index(best_attr)
    print(index)
    for x in range(0, len(examples)-1):
        if examples[x][index] == value:
            branches.append(examples[x])

    return branches


def check_labels(examples):
    positive = 0
    negative = 0
    for x in range(0, len(examples)-1):
        if examples[x][4] == 'Yes ':
            positive = positive + 1
        elif examples[x][4] == 'No ':
            negative = negative + 1

    return [positive, negative]


def main():

    with open('playtennis.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            examples.append(row)

    for x in range(0,len(examples)-1):
        examples[x] = [i.split(' \t') for i in examples[x]]
        examples[x] = examples[x][0]

    classification_attr = "Play?"
    attributes = examples[0]
    examples.remove(examples[0])
    print(examples)
    print(attributes)
    print(id3(examples, classification_attr, attributes))

if __name__ == "__main__":
    main()