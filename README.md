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
trivy image --severity HIGH,CRITICAL todo:latest
or
trivy image --severity CRITICAL --exit-code 1 todo:latest && echo "Pass: No critical vulnerabilities found." || echo "Fail: Critical vulnerabilities found."
```

## Run Space efficincy scan

```bash
docker run --rm -t -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest --ci todo:latest --highestUserWastedPercent=disabled --lowestEfficiency=0.85
```

# Run application
```bash
docker build -t localhost:32000/todo:v1 .
docker push localhost:32000/todo:v1
helm upgrade --install todo chart --set image.registry=localhost:32000 --set image.tag=v1
```

# Test docker only
docker build -t todo:v1 .

docker run -it --rm -p 8888:8080 -e djangoSecret=1234 -e PYTHONDONTWRITEBYTECODE=1 -e PYTHONUNBUFFERED=1 todo:v1

curl http://127.0.0.1:8888/api/todo/

output: [{"id":2,"task":"Create a bitbucket repo for sample project","description":"Create the bitbucket repo for sample project","create_date":"2024-01-26","update_date":"2024-01-26","owner":1}]
