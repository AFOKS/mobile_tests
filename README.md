# mobile_tests

Репозиторий с автотестами для мобильного приложения на Python + pytest.

## 📋 Описание

Проект содержит набор автоматизированных тестов для мобильного приложения, написанных на Python с использованием фреймворка pytest.

## 📁 Структура проекта

mobile_tests/
├── tests/            # Директория с тестами
├── .gitignore        # Исключения Git
├── pytest.ini        # Конфигурация pytest
├── requirements.txt  # Зависимости проекта
└── README.md         # Документация

## 🚀 Установка и запуск

### 1. Клонирование репозитория

git clone https://github.com/AFOKS/mobile_tests.git
cd mobile_tests

### 2. Создание виртуального окружения

bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

### 3. Установка зависимостей

pip install -r requirements.txt

### 4. Настройка переменных окружения

# Пример переменных окружения
DEVICE_NAME=emulator-5554
APP_PATH=/path/to/app.apk
PLATFORM_NAME=Android

### 5. Запуск тестов

pytest

Для запуска с подробным выводом:

pytest -v

Запуск конкретного файла с тестами:

pytest tests/test_example.py

## ⚙️ Конфигурация

Настройки pytest находятся в файле pytest.ini.

## 📦 Зависимости

Все зависимости перечислены в requirements.txt. Установить их можно командой:

pip install -r requirements.txt

## 🤝 Вклад в проект

Форкните репозиторий

Создайте ветку для новой функции (git checkout -b feature/your-feature)

Закоммитьте изменения (git commit -m 'Add some feature')

Отправьте изменения в ветку (git push origin feature/your-feature)

Откройте Pull Request
