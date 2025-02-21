# illumio-assessment

## Assumptions
- The flow log is a log file with 14 columns (version 2 of the log file - default one)
- Protocol Mapping is taken from protocol.csv which contains two columns - number and name, if protocol number is not found, then the protocol is considered `unknown`

## Files


### `solution.py`

This is the main script responsible for:
- Reading the `lookup.csv` and `protocol.csv` files.
- Processing the flow log entries.
- Writing the results to output files.

### `test.py`

Contains unit tests for the functions in `solution.py`. These tests ensure that the core functionality works as expected, including handling corner cases.

### `test_largescale.py`

Performs large-scale tests to measure the program's performance when handling large datasets (e.g., flow logs with 100,000+ entries). These tests are used to measure the performance of the program when handling large datasets. And these tests will be performed without modifying the existing files like `lookup.csv` and `protocol.csv`. New files will be created for the test and they will be deleted after the test is completed by the tearDown function.

### `lookup.csv`

A CSV file that maps `dstport` and `protocol` (as a combination) to a specific tag (e.g., `web_traffic`, `dns_service`). It is used to classify network traffic in the flow log.

### `protocol.csv`

A CSV file that maps protocol numbers (e.g., `6`, `17`, `1`) to human-readable protocol names (e.g., `tcp`, `udp`, `icmp`). This mapping is necessary to convert the numeric protocol IDs in the flow logs into human-friendly names.

### `flow-log.log`

A sample flow log file (in the standard AWS VPC flow log format) used for testing and processing.


### Run Main Solution   
```
python3 solution.py
```

### Run Unit Tests
```
python3 -m unittest test.py
```

### Run Large Scale Test
```
python3 -m unittest test_largescale.py
```

### Output
- `tag_counts.txt` - Contains the count of each tag in the flow log
- `port_protocol_counts.txt` - Contains the count of each port and protocol combination in the flow log
