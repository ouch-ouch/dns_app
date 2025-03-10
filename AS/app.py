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

    # Save to file
    with open(DNS_RECORDS_FILE, 'a') as f:
        f.write(f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n\n")
    
    return "Registered Successfully", 201


# Handle DNS Queries from US
def handle_dns_query():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 53533))

    while True:
        data, addr = sock.recvfrom(1024)
        query = data.decode('utf-8').strip()

        if "TYPE=A" in query:
            hostname = query.split('\n')[1].split('=')[1]
            with open(DNS_RECORDS_FILE, 'r') as f:
                for line in f.read().split('\n\n'):
                    if f"NAME={hostname}" in line:
                        response = line
                        sock.sendto(response.encode('utf-8'), addr)
                        break

if __name__ == "__main__":
    import threading
    threading.Thread(target=handle_dns_query).start()
    app.run(host='0.0.0.0', port=53533)