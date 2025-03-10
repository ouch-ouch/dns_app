from flask import Flask, request
import socket

app = Flask(__name__)
DNS_RECORDS_FILE = "dns_records.txt"

# Handle registration requests from FS
@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = data['as_port']

    # Save the DNS record to the file
    with open(DNS_RECORDS_FILE, 'a') as f:
        f.write(f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n\n")
    
    return "Registered Successfully", 201


# Handle DNS Queries from US (User Service)
def handle_dns_query():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 53533))

    while True:
        # ✅ Receive a DNS query
        data, addr = sock.recvfrom(1024)
        query = data.decode('utf-8').strip()
        print(f"Received DNS Query: {query}")

        # ✅ Check if the query is TYPE=A
        if "TYPE=A" in query:
            hostname = query.split('\n')[1].split('=')[1]
            found = False

            # ✅ Read the DNS records from the file
            with open(DNS_RECORDS_FILE, 'r') as f:
                for record in f.read().split('\n\n'):
                    if f"NAME={hostname}" in record:
                        # ✅ Found the record, send it back
                        sock.sendto(record.encode('utf-8'), addr)
                        found = True
                        break
            
            # ✅ If no record was found, return "NOT_FOUND"
            if not found:
                response = f"TYPE=A\nNAME={hostname}\nVALUE=NOT_FOUND\nTTL=0"
                sock.sendto(response.encode('utf-8'), addr)

if __name__ == "__main__":
    # ✅ Start the DNS query handler in a separate thread
    import threading
    threading.Thread(target=handle_dns_query).start()
    app.run(host='0.0.0.0', port=53533)