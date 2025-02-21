from collections import defaultdict

# Function - read_lookup
# Logic - Reads the lookup.csv file and parses it into a dictionary
# Input - lookup.csv
# Output - dictionary with dstport and protocol as key and tag as value
def read_lookup(lookup_file):
    # Initializing an empty dictionary
    lookup = defaultdict(list)
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
            dstport, protocol, tag = [part.strip().lower() for part in parts]
            # Adding the key-value pair to the dictionary
            lookup[(dstport, protocol)].append(tag)
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
            number, name = [part.strip().lower() for part in parts]
            # Adding the key-value pair to the dictionary
            protocol[number] = name
    # Returning the dictionary
    return protocol

def process_flow_log(flow_log_file, lookup):
    # Reading the protocol.csv file
    protocol_map = read_protocol('protocol.csv')
    # Initializing the tag counts and port protocol counts
    tag_counts = defaultdict(int)  # defaultdict for counting tags
    port_protocol_counts = defaultdict(int)  # defaultdict for counting port/protocol
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
            dstport = parts[6].strip().lower()
            protocol_number = parts[7].strip()
            # Getting the protocol name from the protocol map
            protocol = protocol_map.get(protocol_number, 'unknown')
            # Creating a key for the port protocol counts
            key = (dstport, protocol)
            # Adding the count to the port protocol counts
            port_protocol_counts[key] += 1
            # Creating a key for the lookup
            lookup_key = (dstport, protocol)
            # Getting the tag from the lookup
            tags = lookup[lookup_key] if lookup[lookup_key] else ["Untagged"]
            # Adding the count to the tag counts
            for tag in tags:
                tag_counts[tag] += 1
    # Returning the tag counts and port protocol counts
    return tag_counts, port_protocol_counts

# Function - write_port_protocol_counts
# Logic - Writes the tag counts and port/protocol counts to the specified output file
# Input - output_file, tag_counts, port_protocol_counts
# Output - None
def write_port_protocol_counts(output_file, port_protocol_counts):
    # Opening the output file in write mode
    with open(output_file, 'w') as f:
        # Writing the header
        f.write("Port,Protocol,Count\n")
        # Writing the port/protocol counts
        for (port, protocol), count in sorted(port_protocol_counts.items(), key=lambda x: (int(x[0][0]) if x[0][0].isdigit() else float('inf'), x[0][1])):
            # Writing the port, protocol and count
            f.write(f"{port},{protocol},{count}\n")

# Function - write_tag_counts
# Logic - Writes the tag counts to the specified output file
# Input - output_file, tag_counts
# Output - None
def write_tag_counts(output_file, tag_counts):
    # Opening the output file in write mode
    with open(output_file, 'w') as f:
        # Writing the header
        f.write("Tag,Count\n")
        # Writing the tag counts
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
            # Writing the tag and count
            f.write(f"{tag},{count}\n")

# Function - main
# Logic - Main function to execute the program
# Input - None
# Output - None
def main():
    lookup_file = 'lookup.csv'
    flow_log_file = 'flow-log.log'
    tag_counts_file = 'tag_counts.txt'
    port_protocol_counts_file = 'port_protocol_counts.txt'
    
    # Load the lookup table
    lookup = read_lookup(lookup_file)
    
    # Process the flow logs using the lookup table
    tag_counts, port_protocol_counts = process_flow_log(flow_log_file, lookup)
    
    # Write the results to two separate output files
    write_tag_counts(tag_counts_file, tag_counts)
    write_port_protocol_counts(port_protocol_counts_file, port_protocol_counts)
    
    print(f"Program complete.\nTag counts written to {tag_counts_file}\nPort/Protocol counts written to {port_protocol_counts_file}")

if __name__ == "__main__":
    main()