# OneLease
OneLese - це агрегатор оголошень оренди житла, який збирає оголошення в одному місці для зручного пошуку житла.

# Команди запуску
Клонувати репозиторій
```
git clone https://github.com/Ivan-Usenko/usenko-onelease.git
cd usenko-onelease
```

Створити та активувати віртуальне середовище
```
python3 -m venv .venv
source .venv/bin/activate
```

Встановити і запустити проєкт:
```
pip install -e .
onelease
```

Або якщо потрібно запустити тести:
```
pip install -e ".[dev]"
pytest
```
