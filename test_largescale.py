import unittest
import tempfile
import os
from solution import read_lookup, process_flow_log, read_protocol

class TestLargeScaleProcessing(unittest.TestCase):
    def setUp(self):
        # Creating temporary directory to store the test files
        self.test_dir = tempfile.mkdtemp()
        self.test_protocol_file = os.path.join(self.test_dir, 'test_protocol.csv')
        self.create_protocol_file()  # Creating a protocol file
        self.test_lookup_file = os.path.join(self.test_dir, 'test_lookup.csv')
        self.create_lookup_file()  # Creating a lookup file
        self.test_flow_log = os.path.join(self.test_dir, 'test_flow.log')
        
    def create_protocol_file(self):
        # Defining the protocol content, with some common ones
        protocol_content = "number,name\n"
        standard_protocols = {
            "1": "icmp", "6": "tcp", "17": "udp", "443": "https",
            "53": "dns", "80": "http", "22": "ssh", "25": "smtp"
        }
        for num, name in standard_protocols.items():
            protocol_content += f"{num},{name}\n"
        
        # Adding some random protocols to make it a bit bigger
        for i in range(100, 200):
            protocol_content += f"{i},protocol{i}\n"
            
        # Writing the protocol data to the file
        with open(self.test_protocol_file, 'w') as f:
            f.write(protocol_content)
            
    def create_lookup_file(self):
        # Creating lookup file with some well-known services
        lookup_content = "dstport,protocol,tag\n"
        standard_services = [
            ("80", "http", "web_traffic"),
            ("443", "https", "secure_web"),
            ("53", "dns", "dns_service"),
            ("22", "ssh", "ssh_service")
        ]
        for port, proto, tag in standard_services:
            lookup_content += f"{port},{proto},{tag}\n"
            
        # Adding random services to match with protocols
        for i in range(1000, 2000):
            lookup_content += f"{i},protocol{i%100+100},service_{i}\n"
            
        # Writing the lookup data to the file
        with open(self.test_lookup_file, 'w') as f:
            f.write(lookup_content)
            
    def generate_flow_log_entry(self, i):
        # This creates a fake flow log entry, just for test
        dstport = str(1000 + (i % 1000))
        protocol = str((i % 100) + 100)
        return (f"2 123456789012 eni-{i:010d} 10.0.0.1 10.0.0.2 12345 "
                f"{dstport} {protocol} 100 1000 1623456789 1623456799 ACCEPT OK")

    def test_large_scale_processing(self):
        # Generating 100000 flow log entries, quite a big file!
        with open(self.test_flow_log, 'w') as f:
            # Write 100000 log entries
            for i in range(100000):
                f.write(self.generate_flow_log_entry(i) + "\n")

        # Now let's process the flow log and do some timing to see how it performs
        lookup = read_lookup(self.test_lookup_file)
        
        import time
        start_time = time.time()  # Starting the timer
        
        tag_counts, port_proto_counts = process_flow_log(self.test_flow_log, lookup)
        
        processing_time = time.time() - start_time  # End the timer

        # Counting the number of data lines in the flow log, skipping the header
        with open(self.test_flow_log, 'r') as f:
            data_lines = sum(1 for _ in f)
            print(f"Actual data lines in flow log: {data_lines}")

        # Verifying that we processed the correct number of lines
        total_processed = sum(port_proto_counts.values())
        print(f"Total entries processed: {total_processed}")
        
        # Checking if the counts match the number of data entries
        self.assertEqual(data_lines, 100000, "Should have exactly 100000 data lines")
        self.assertEqual(total_processed, 100000, "Should process exactly 100000 entries")
        
        # Checking tag counts, it should be 100000 as well
        total_tags = sum(tag_counts.values())
        self.assertEqual(total_tags, 100000, "Total tag counts should be 100000")
        
        # Printing out the results so we can see how it's doing
        print(f"\nLarge Scale Test Results:")
        print(f"Processing time: {processing_time:.2f} seconds")
        print(f"Total entries processed: {total_processed}")
        print(f"Unique port-protocol combinations: {len(port_proto_counts)}")
        
        # Verifying that all counts are within expected range
        for port_proto, count in port_proto_counts.items():
            self.assertLessEqual(count, 100000)
            self.assertGreater(count, 0)

    def tearDown(self):
        # Clean up by deleting the temporary directory and all files in it
        import shutil
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main(verbosity=2)
