# Django Server Install Guide

이 저장소는 로컬 테스트용 Django 서버 구조를 포함합니다.

## 1. 설치

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements-ci.txt
python manage.py migrate --noinput
python manage.py check
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip setuptools wheel
pip install -r requirements-ci.txt
py manage.py migrate --noinput
py manage.py check
```

## 2. 서버 실행

```bash
python manage.py runserver 0.0.0.0:8000
```

Windows PowerShell:

```powershell
py manage.py runserver 127.0.0.1:8000
```

## 3. 확인 URL

- Home: http://127.0.0.1:8000/
- Health: http://127.0.0.1:8000/health/

## 4. 테스트

```bash
python manage.py test --verbosity 2
python -m pytest -q
```

## 5. GitHub Actions

`.github/workflows/django.yml`에서 Python 3.10, 3.11, 3.12 기준으로 테스트합니다.

이 구성은 외부 AI API를 호출하지 않습니다.
