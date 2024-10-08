# Development

## Setup
```bash
pip install virtualenv
virtualenv venv
venv\\Scripts\\activate
cd src
pip install -r requirements.txt
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Run vulnerability scan

```bash
trivy image --severity HIGH,CRITICAL django4-todo:latest
or
trivy image --severity CRITICAL --exit-code 1 django4-todo:latest && echo "Pass: No critical vulnerabilities found." || echo "Fail: Critical vulnerabilities found."
```

## Run Space efficincy scan

```bash
docker run --rm -t -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest --ci todo:latest --highestUserWastedPercent=disabled --lowestEfficiency=0.85
```

# Run application
```bash
# build
docker build -t localhost:32000/django4-django4-todo:1.0.0 .
docker push localhost:32000/django4-django4-todo:1.0.0
helm upgrade --install django4-todo chart --set image.registry=localhost:32000 --set image.tag=v1

or

docker login ghcr.io -u kkmishra233 -p $PAT
docker build -t ghcr.io/kkmishra233/docker-registry/django4-todo:1.0.0 .
docker push ghcr.io/kkmishra233/docker-registry/django4-todo:1.0.0

helm registry login ghcr.io -u kkmishra233 -p $PAT
helm package chart
export CHART_VERSION=$(grep 'version:' ./chart/Chart.yaml | head -n1 | awk '{ print $2}')
helm push django4-todo-${CHART_VERSION}.tgz oci://ghcr.io/kkmishra233/helm-charts
rm -rf django4-todo-${CHART_VERSION}.tgz

# run
docker run -it --rm -p 8888:8080 -e djangoSecret=1234 -e PYTHONDONTWRITEBYTECODE=1 -e PYTHONUNBUFFERED=1 ghcr.io/kkmishra233/docker-registry/django4-todo:1.0.0
or
kubectl create secret docker-registry ghcr-secret --docker-server=ghcr.io --docker-username=kkmishra233 --docker-password=$PAT --docker-email=kkbit233@gmail.com
helm upgrade --install django4-todo oci://ghcr.io/kkmishra233/helm-charts/django4-todo --version=1.0.0  --timeout 60s --set image.registry=ghcr.io/kkmishra233/docker-registry --set image.imagePullSecrets=ghcr-secret
```

# Test docker only
docker build -t django4-todo:1.0.0 .

docker run -it --rm -p 8888:8080 -e djangoSecret=1234 -e PYTHONDONTWRITEBYTECODE=1 -e PYTHONUNBUFFERED=1 django4-todo:1.0.0

curl http://127.0.0.1:8888/api/todo/

output: [{"id":2,"task":"Create a bitbucket repo for sample project","description":"Create the bitbucket repo for sample project","create_date":"2024-01-26","update_date":"2024-01-26","owner":1}]
