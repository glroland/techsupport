install:
	pip install -r requirements.txt

lint:
	pylint src/*.py

run: lint
	cd src && streamlit run app.py --server.port 8080 --server.address 0.0.0.0  --server.headless true --logger.level debug

build:
	podman build -t techsupport-image:latest . --platform linux/amd64

push:
	podman tag techsupport-image:latest registry.home.glroland.com/ai/techsupport:latest
	podman push registry.home.glroland.com/ai/techsupport:latest --tls-verify=false

deploy:
	oc apply -f kubernetes/deploy.yaml

dev: lint
	odo dev
