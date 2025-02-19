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

# Function - read_protocol
# Logic - Reads the protocol.csv file and parses it into a dictionary
# Input - protocol.csv
# Output - dictionary with number as key and name as value
def read_protocol(protocol_file):
    # Initializing an empty dictionary
    protocol = {}
    # Opening the protocol.csv file in read mode
    with open(protocol_file, 'r') as f:
        # Ignoring the header line
        header = f.readline()
        # Reading the rest of the lines
        for line in f:
            # Skipping empty lines
            if not line.strip():
                continue
            # Splitting the line into parts
            parts = line.strip().split(',')
            # Checking if the line has 2 parts
            if len(parts) != 2:
                continue
            # Assigning the parts to the variables
            number, name = parts
            # Adding the key-value pair to the dictionary
            protocol[number] = name
    # Returning the dictionary
    return protocol

def process_flow_log(flow_log_file, lookup):    
    # Reading the protocol.csv file
    protocol_map = read_protocol('protocol.csv')
    # Initializing the tag counts and port protocol counts
    tag_counts = {}
    port_protocol_counts = {}
    # Opening the flow-log.log file in read mode
    with open(flow_log_file, 'r') as f:
        # Reading the rest of the lines
        for line in f:
            if not line.strip():
                # Skipping empty lines
                continue
            # Splitting the line into parts
            parts = line.strip().split()
            # Checking if the line has 14 parts
            if len(parts) != 14:
                # Skipping lines with incorrect number of parts
                continue
            # Assigning the parts to the variables
            dstport = parts[5]
            protocol_number = parts[7]
            # Getting the protocol name from the protocol map
            protocol = protocol_map.get(protocol_number, 'unknown')
            # Creating a key for the port protocol counts
            key=(dstport, protocol)
            # Adding the count to the port protocol counts
            port_protocol_counts[key] = port_protocol_counts.get(key, 0) + 1
            # Creating a key for the lookup
            lookup_key = (dstport, protocol)
            # Getting the tag from the lookup
            tag = lookup.get(lookup_key, "Untagged")
            # Adding the count to the tag counts
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    # Returning the tag counts and port protocol counts
    return tag_counts, port_protocol_counts


print(read_lookup('lookup.csv'))
print(process_flow_log('flow-log.log', read_lookup('lookup.csv')))