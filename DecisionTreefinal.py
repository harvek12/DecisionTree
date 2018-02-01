import csv
import math
import flatdict

examples = []
attributes = []

# splits examples based on their best feature and returns dictionary containing tree
def id3(examples, classification_attribute, attributes, global_attributes):

    classes = find_unique_classifications(examples, classification_attribute, global_attributes)
    positive = check_labels(examples, classification_attribute, global_attributes)[0]
    negative = check_labels(examples, classification_attribute, global_attributes)[1]
    # if the attribute is perfectly partitioned, return its class
    if positive == len(examples):
        return classes[0]
    elif negative == len(examples):
        return classes[1]
    # if there are no attributes left, return root node with most popular class
    elif len(attributes) == 0 or (len(attributes) == 1 and attributes[0] == classification_attribute):
        return classes[0] if positive > negative else classes[1]
    else:
        best_attr = best_attribute(examples, classification_attribute, attributes, global_attributes)
        tree = {best_attr: {}}
        values = find_unique_classifications(examples, best_attr, global_attributes)
        for value in values:
            branch_examples = get_branches(examples, global_attributes, best_attr, value)

            # if there are no more branch examples to split on, assign the most popular class to this node
            if len(branch_examples) == 0:
                positive = check_labels(examples, classification_attribute, global_attributes)[0]
                negative = check_labels(examples, classification_attribute, global_attributes)[1]
                return classes[0] if positive > negative else classes[1]
            else:
                # check that the attribute hasn't been removed
                if best_attr in attributes:
                    attributes.remove(best_attr)
                subtree = id3(branch_examples, classification_attribute, attributes, global_attributes)
                tree[best_attr][value] = subtree
    return tree


def get_error(tree, examples, attributes):
    for k in tree.keys():
        first = k

    x, y = len(tree[first].keys()), 2
    label_listA = [[0 for i in range(y)] for j in range(x)]

    label_listB = [None] * len(tree[first].keys())
    i = 0
    j = 0

    for v in tree[first].values():

        if type(v) is not str:
            flat_labels = flatdict.FlatDict(v)
            label_listA[j][0] = flat_labels.keys()
            label_listA[j][1] = flat_labels.values()
            j += 1

        else:
            label_listB[i] = v
            i += 1
    print (label_listA)

    final_watch = []
    c = []
    total_error = 0.0
    count = 0
    for i in range(0, len(label_listA[0][0])):
        labelstmp = label_listA[0][0][i]
        labels = labelstmp.split(":")
        for j in labels:
            if j in attributes:
                labels.remove(j)

        for k in examples:
            if set(labels) < set(k) and k[0] != label_listA[0][1][i]:

                total_error += 1
                count += 1
                watch = 1- (total_error / count)
                final_watch.append(watch)

                c.append(count)
            else:
                count += 1

    print(final_watch)
    print(c)
    final = 1 - (total_error / count)
    print(final)
    return (final_watch)

# return list of an attribute's unique values
def find_unique_classifications(examples, attribute, global_attributes):
    values = get_values(examples, attribute, global_attributes)
    final_classifications = list(set(values))

    return final_classifications


# returns the values of the attribute given
def get_values(examples, attribute, global_attributes):
    x = 0
    values = [None] * len(examples)
    index = global_attributes.index(attribute)

    for j in range(0, len(examples)):
        values[j] = examples[j][index]
    return values


def get_frequencies(examples, attribute, attributes):
    frequency_dict = {}
    classifications = find_unique_classifications(examples, attribute, attributes)
    values = get_values(examples, attribute, attributes)

    for i in classifications:
        frequency_dict.update({i: 0})

    for j in classifications:
        for i in range(0, len(values)):
            if values[i] == j:
                frequency_dict[j] += 1

    return frequency_dict


def get_set_entropy(examples, classification_attribute, attributes):
    entropy = 0.0
    frequencies = get_frequencies(examples, classification_attribute, attributes)
    total = sum(frequencies.values())
    for key in frequencies.keys():
        if frequencies[key] == 0:
            entropy += 0
        else:
            entropy += (-frequencies[key] / total) * (math.log(frequencies[key] / total, 2))
    return entropy


def get_entropy(examples, subset_label, classification_attribute, attribute, attributes, global_attributes):
    set_frequencies = get_frequencies(examples, classification_attribute, attributes)
    entropy = 0.0
    subset_target_freqs = get_target_frequencies(examples, subset_label, classification_attribute, attributes,
                                                 global_attributes)
    total = sum(subset_target_freqs.values())
    for key in subset_target_freqs.keys():
        if subset_target_freqs[key] == 0:
            entropy += 0
        else:
            entropy += (-subset_target_freqs[key] / total) * (math.log(subset_target_freqs[key] / total, 2))

    return entropy


def get_target_frequencies(examples, subset_label, classification_attribute, attributes, global_attributes):
    frequencies = get_frequencies(examples, classification_attribute, attributes)
    target_frequencies = {}
    target_classifications = find_unique_classifications(examples, classification_attribute, global_attributes)
    target = global_attributes.index(classification_attribute)

    for i in target_classifications:
        target_frequencies.update({i: 0})

    for i in range(0, len(examples)):
        for j in range(0, len(examples[i])):
            if examples[i][j] == subset_label:
                for key in target_frequencies.keys():
                    if examples[i][target] == key:
                        target_frequencies[key] += 1

    return (target_frequencies)


def gain(examples, classification_attribute, attributes, i, global_attributes):
    frequency_dict = get_frequencies(examples, i, attributes)
    total_element_gain = 0.0
    set_entropy = get_set_entropy(examples, classification_attribute, attributes)
    attribute_entropy = 0.0
    total_values = sum(frequency_dict.values())

    for j in frequency_dict.keys():
        probability = frequency_dict[j] / total_values
        attribute_entropy += probability * get_entropy(examples, j, classification_attribute, i, attributes,
                                                       global_attributes)

    total_element_gain = set_entropy - attribute_entropy

    return total_element_gain

# calculate the info gain for each attribute and choose the highest
def best_attribute(examples, classification_attribute, attributes, global_attributes):
    max_info_gain = 0.0
    if len(attributes) > 1:
        best_attr = attributes[1]
    else:
        return 0
    for attribute in attributes:
        if attribute != classification_attribute:
            attr_gain = gain(examples, classification_attribute, attributes, attribute, global_attributes)
            if attr_gain > max_info_gain:
                max_info_gain = attr_gain
                best_attr = attribute

    return best_attr


# returns all observations in dataset that correspond to a given attribute's value
def get_branches(examples, global_attributes, best_attr, value):
    branches = []
    index = global_attributes.index(best_attr)
    for x in range(0, len(examples)):
        if examples[x][index] == value:
            branches.append(examples[x])

    return branches


# tallies the number of positive and negative labels in the dataset
def check_labels(examples, classification_attribute, global_attributes):
    positive = 0
    negative = 0

    labels = find_unique_classifications(examples, classification_attribute, global_attributes)

    for x in range(0, len(examples)):
        if examples[x][0] == labels[0]:
            positive = positive + 1
        elif examples[x][0] == labels[1]:
            negative = negative + 1

    return [positive, negative]

#iterate through each key-value in the tree, recursively printing pairs
def print_tree(d, keys=()):
    if type(d) == dict:
         for k in d:
            for rv in print_tree(d[k], keys + (k, )):
                yield rv
    else:
        yield (keys, d)


def main():
    #change file name to run on specific dataset (i.e. train or test)
    with open('house-votes-test.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            for i in row:
                if '?' not in i:
                    examples.append(row)

    for x in range(0, len(examples)):
        examples[x] = [i.split(',') for i in examples[x]]
        examples[x] = examples[x][0]

    classification_attr = "Class_Name"
    attributes = examples[0]
    global_attributes = list(attributes)
    examples.remove(examples[0])
    Decision_tree = id3(examples, classification_attr, attributes, global_attributes)
    print(Decision_tree)
    x = get_error(Decision_tree, examples, global_attributes)
    for compound_key, val in print_tree(Decision_tree):
        print('{} : {}'.format(compound_key, val))

if __name__ == "__main__":
    main()