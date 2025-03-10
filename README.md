python3 -m venv myenv
source myenv/bin/activate 
pip install Flask

start docker
docker network create dns_net

docker build -t myas-image ./AS
docker build -t myfs-image ./FS
docker build -t myus-image ./US

docker-compose up 

testing the sequence 

myfs

curl -X PUT "http://localhost:9090/register" \
-H "Content-Type: application/json" \
-d '{
    "hostname": "myfs",
    "ip": "172.19.0.3",
    "as_ip": "172.19.0.2",
    "as_port": "53533"
}'

docker-compose down
docker-compose up --build

RUNNING ON K8
to run the app on k8 with aws use deploy_dns.yml file.
