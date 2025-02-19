# Function - read_lookup
# Logic - Reads the lookup.csv file and parses it into a dictionary
# Input - lookup.csv
# Output - dictionary with dstport and protocol as key and tag as value
def read_lookup(lookup_file):
    # Initializing an empty dictionary
    lookup = {}
    # Open the lookup.csv file in read mode
    with open(lookup_file, 'r') as f:
        # Ignoring the header line
        header = f.readline()
        # Reading the rest of the lines
        for line in f:
            # Skipping empty lines
            if not line.strip():
                continue
            # Splitting the line into parts
            parts = line.strip().split(',')
            # Checking if the line has 3 parts 
            if len(parts) != 3:
                continue
            # Assigning the parts to the variables
            dstport, protocol, tag = parts
            # Adding the key-value pair to the dictionary
            lookup[(dstport, protocol)] = tag
    # Returning the dictionary
    return lookup

print(read_lookup('lookup.csv'))