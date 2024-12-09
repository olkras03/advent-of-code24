# Step 1: Read the input files
with open('input_rules.txt', 'r') as file:
    rules_lines = file.read().strip().split('\n')

with open('input_ordering.txt', 'r') as file:
    ordering_lines = file.read().strip().split('\n')


# Step 2: Convert each line into a tuple
rules = [tuple(map(int, line.split('|'))) for line in rules_lines]
ordering = [list(map(int, line.split(','))) for line in ordering_lines]

def validate_ordering(rules, ordering):
    """Validate if each sequence in ordering respects the rules and return only valid sequences."""
    valid_sequences = []  # List to store valid sequences
    invalid_sequences = [] # List to store invalid sequences
    
    for i, order in enumerate(ordering, start=1):
        is_valid = True  # Assume valid until proven otherwise
        
        for rule in rules:
            X, Y = rule
            if X in order and Y in order:
                # Check positions of X and Y
                if order.index(X) > order.index(Y):
                    print(f"Sequence {i} is invalid: Rule {rule} violated.")
                    is_valid = False
                    break  # No need to check further rules for this sequence
        
        if is_valid:
            print(f"Sequence {i} is valid: {order}")
            valid_sequences.append(order)  # Add to valid list
        else:
            print(f"Sequence {i} is invalid: {order}")
            invalid_sequences.append(order)
    
    return valid_sequences, invalid_sequences

valid_sequences, invalid_sequences = validate_ordering(rules, ordering)
print(valid_sequences)
print(invalid_sequences)

def sum_middle(valid_sequences):
    """Calculate the sum of middle numbers from a list of sequences."""
    middle_sum = 0
    for seq in valid_sequences:
        middle_index = len(seq) // 2
        middle_number = seq[middle_index]
        middle_sum += middle_number
        print(f"Sequence: {seq}, Middle number: {middle_number}")
    return middle_sum

middle_sum = sum_middle(valid_sequences)
print(f"Total sum of middle numbers: {middle_sum}")

#part 2

from collections import defaultdict, deque

def reorder_invalid_sequences(invalid_sequences, rules):
    """Reorder invalid sequences to make them valid using topological sorting."""
    corrected_sequences = []
    
    for seq in invalid_sequences:
        # Build graph for this sequence
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        
        # Add rules to the graph
        for X, Y in rules:
            if X in seq and Y in seq:
                graph[X].append(Y)
                in_degree[Y] += 1
                if X not in in_degree:  # Ensure X is in the in-degree map
                    in_degree[X] = 0
        
        # Perform topological sort
        queue = deque([node for node in seq if in_degree[node] == 0])
        sorted_sequence = []
        
        while queue:
            current = queue.popleft()
            sorted_sequence.append(current)
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Add sorted sequence to results
        corrected_sequences.append(sorted_sequence)
    
    return corrected_sequences

corrected_sequences = reorder_invalid_sequences(invalid_sequences, rules)
print(corrected_sequences)

middle_sum_corrected = sum_middle(corrected_sequences)
print(f"Total sum of middle numbers: {middle_sum_corrected}")
