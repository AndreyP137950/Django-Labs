@echo off
REM Скрипт быстрого запуска Case системы на Windows

echo.
echo ========================================
echo Case Система - Запуск
echo Лабораторная работа №11
echo ========================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не установлен или недоступен в PATH
    echo Скачайте Python с https://python.org/
    pause
    exit /b 1
)

echo [OK] Python найден

REM Проверка Django
python -m django --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [1/3] Установка Django...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ОШИБКА: Не удалось установить зависимости
        pause
        exit /b 1
    )
    echo [OK] Django установлен
) else (
    echo [OK] Django уже установлен
)

REM Проверка базы данных
if not exist db.sqlite3 (
    echo.
    echo [2/3] Инициализация базы данных...
    python manage.py migrate
    if errorlevel 1 (
        echo ОШИБКА: Не удалось инициализировать БД
        pause
        exit /b 1
    )
    echo [OK] БД готова
) else (
    echo [OK] БД уже существует
)

echo.
echo [3/3] Запуск сервера...
echo.
echo ========================================
echo Откройте браузер: http://127.0.0.1:8000/
echo Для остановки нажмите: Ctrl+C
echo ========================================
echo.

REM Запуск сервера
python manage.py runserver

pause
