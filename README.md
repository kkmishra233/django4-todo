# Development

## Setup
```
pip install virtualenv

virtualenv venv

venv\\Scripts\\activate

cd src

pip install -r requirements.txt
```

## Run
```
python manage.py createsuperuser

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```

## Run vulnerability scan

```
trivy image --severity HIGH,CRITICAL todo:latest

or

trivy image --severity CRITICAL --exit-code 1 todo:latest && echo "Pass: No critical vulnerabilities found." || echo "Fail: Critical vulnerabilities found."
```

## Run Space efficincy scan

```
docker run --rm -t -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest --ci todo:latest --highestUserWastedPercent=disabled --lowestEfficiency=0.85
```


testting
