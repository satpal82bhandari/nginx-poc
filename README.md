# NGINX Implementation

## Project Structure
```
nginx-poc/
├── docker-compose.yml
├── nginx/
│   ├── Dockerfile          # NGINX Dockerfile
│   └── nginx.conf          # NGINX configuration file
├── server1/
│   ├── Dockerfile          # FastAPI Dockerfile for server1
│   ├── main.py             # FastAPI app for items
│   └── requirements.txt    # Python requirements for server1
└── server2/
    ├── Dockerfile          # FastAPI Dockerfile for server2
    ├── main.py             # FastAPI app for orders
    └── requirements.txt    # Python requirements for server2

```

---------------------

### Running Application without Docker

1. Clone the github repository
```
git clone https://github.com/satpal82bhandari/nginx-poc.git
cd nginx-poc
```

2. Set up a **Python3.10** virtual environment and install dependencies
```
sudo apt update
sudo apt install python3.10
sudo apt install python3-venv
python --version
# or 
python3 --version
python3 -m venv my_env
source my_env/bin/activate
```

3. Run individual Server1 and Server2 with the following command
```
cd server1 
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8001 --reload

cd server2
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8002 --reload
```

4. Starting NGINX(using the first code part in ngin.cong file)
```
sudo nginx -c /path/to/nginx-poc/nginx.conf
```

5. Closing previous connections if running port issue (optional)
```
sudo lsof -i :80
sudo systemctl stop nginx
# or 
sudo nginx -s stop
sudo nginx -c /path/to/nginx-poc/nginx.conf
```

6. Test the Setup
Now you should be able to test the endpoints via NGINX:
```
Access server1 (Items service): http://localhost/items
Access server2 (Orders service): http://localhost/orders
```

### Run the Application with Docker Image File

#### Build and Run server1 and server2 Containers Individually
1. Navigate to the server1 directory and build the Docker image:
```
docker build -t server1-app .
```
2. Run the server1 container on port 8001:
```
docker run -d --name server1 -p 8001:8001 server1-app
```
3. Navigate to the server2 directory and build the Docker image:
```
docker build -t server2-app .
```
4. Run the server2 container on port 8002:
```
docker run -d --name server2 -p 8002:8002 server2-app
```
5. Build the NGINX image:
```
docker build -t nginx-proxy -f nginx/Dockerfile nginx/
```
6. Run the NGINX container:
```
docker run -d --name nginx-proxy -p 80:80 --network bridge nginx-proxy
```
7. Test the Setup
Now you should be able to test the endpoints via NGINX:
```
Access server1 (Items service): http://0.0.0.0:8001/items/
Access server1 (Items service): http://0.0.0.0:8002/orders
# and for localhost
Access server1 (Items service): http://localhost/items
Access server2 (Orders service): http://localhost/orders
```
8. If issue arise of the accessing on localhost:
All containers (server1, server2, nginx-proxy) should be on the same Docker network. If they are not, NGINX won’t be able to connect to server1 or server2 by name.

You can create a custom network and run the containers on it:
```
docker network create my_network
```
Restart All Containers
```
docker stop server1 server2 nginx-proxy
docker rm server1 server2 nginx-proxy
docker image rm nginx-poc-server1:latest nginx-poc-server2:latest nginx-poc-nginx-proxy:latest
```
```
docker run -d --name server1 --network my_network -p 8001:8001 server1-app
docker run -d --name server2 --network my_network -p 8002:8002 server2-app
docker run -d --name nginx-proxy --network my_network -p 80:80 nginx-proxy
```
### Run the Application with Docker Compose
Build and start server1, server2, and nginx-proxy and connect all services to my_network, allowing NGINX to reach server1 and server2 by their container names.
1. Navigate to Application directory to run docker-compose command:
```
docker-compose up --build
```
2. To stop the containers, use:
```
docker-compose down
```
