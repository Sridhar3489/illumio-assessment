import unittest
import tempfile
import os
from solution import read_lookup, process_flow_log, read_protocol

class TestFlowLogProcessing(unittest.TestCase):
    # This function will run before each test. Creating some temporary files
    # for the tests like protocol file, lookup file and flow log file.
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()  # Creates a temporary directory

        # Preparing a temp protocol file with protocol number and protocol names
        self.temp_protocol_file = os.path.join(self.test_dir, 'test_protocol.csv')
        self.protocol_content = """number,name
6,tcp
17,udp
1,icmp"""
        with open(self.temp_protocol_file, 'w') as f:
            f.write(self.protocol_content)

        # Preparing a temp lookup file with dstport, protocol and tags
        self.temp_lookup_file = os.path.join(self.test_dir, 'test_lookup.csv')
        self.lookup_content = """dstport,protocol,tag
80,tcp,web_traffic
443,tcp,secure_web
53,udp,dns_traffic"""
        with open(self.temp_lookup_file, 'w') as f:
            f.write(self.lookup_content)

        # Preparing a temp flow log file (which will be used in the tests)
        self.temp_flow_log = os.path.join(self.test_dir, 'test_flow.log')

    # Test that the read_protocol function works as expected
    def test_read_protocol(self):
        protocol_map = read_protocol(self.temp_protocol_file)
        
        # Check that the protocol map has the expected values
        self.assertEqual(protocol_map['6'], 'tcp')
        self.assertEqual(protocol_map['17'], 'udp')
        self.assertEqual(protocol_map['1'], 'icmp')
        
        # Also checking if the length of the dictionary is correct
        self.assertEqual(len(protocol_map), 3)

    # Test for the read_lookup function. Ensuring it reads lookup file correctly
    def test_read_lookup(self):
        lookup = read_lookup(self.temp_lookup_file)
        
        # Check that lookup is working for each (port, protocol) tuple
        self.assertTrue('web_traffic' in lookup[('80', 'tcp')])  # tcp port 80 should be mapped to web_traffic
        self.assertTrue('secure_web' in lookup[('443', 'tcp')])  # tcp port 443 should be mapped to secure_web
        self.assertTrue('dns_traffic' in lookup[('53', 'udp')])  # udp port 53 should be mapped to dns_traffic
        
        # Check if lookup dictionary contains exactly 3 entries
        self.assertEqual(len(lookup), 3)

    # Test for the flow log processing when there's an unknown protocol
    def test_process_flow_logs_unknown_protocol(self):
        # Creating flow log with an unknown protocol (protocol number 99)
        flow_log_content = """version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
2 123456789012 eni-123456789 10.0.0.1 10.0.0.2 12345 80 99 100 1000 1623456789 1623456799 ACCEPT OK"""
        
        with open(self.temp_flow_log, 'w') as f:
            f.write(flow_log_content)  # Writing the flow log content into temp file

        # Read lookup to match tags with flow log entries
        lookup = read_lookup(self.temp_lookup_file)
        
        # Process the flow log with the given lookup file
        tag_counts, port_proto_counts = process_flow_log(self.temp_flow_log, lookup)
        
        # We are expecting that 'unknown' protocol should be counted in port_proto_counts
        self.assertEqual(port_proto_counts[('80', 'unknown')], 1)  # Expecting 1 count for protocol 'unknown' at port 80
        
        # For tags, the 'Untagged' tag should be counted (because we had an unknown protocol)
        self.assertEqual(tag_counts['Untagged'], 2)  # Expecting 2 'Untagged' occurrences (flow log with unknown protocol)

    # Cleanup any temp files after test is done.
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)  # Removes the temporary test directory and its contents

# Running the tests
if __name__ == '__main__':
    unittest.main()
