# PowerShell скрипт быстрого запуска Case системы

Write-Host ""
Write-Host "========================================"
Write-Host "Case Система - Запуск" 
Write-Host "Лабораторная работа №11"
Write-Host "========================================" 
Write-Host ""

# Проверка Python
try {
    $pythonVer = python --version 2>&1
    Write-Host "[OK] Python найден: $pythonVer"
} catch {
    Write-Host "ОШИБКА: Python не установлен или недоступен в PATH" -ForegroundColor Red
    Write-Host "Скачайте Python с https://python.org/"
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

# Проверка Django
$djangoFound = $false
try {
    python -m django --version 2>&1 | Out-Null
    $djangoFound = $true
    Write-Host "[OK] Django уже установлен"
} catch {
    Write-Host ""
    Write-Host "[1/3] Установка Django..."
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ОШИБКА: Не удалось установить зависимости" -ForegroundColor Red
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
    Write-Host "[OK] Django установлен"
}

# Проверка базы данных  
if (-not (Test-Path "db.sqlite3")) {
    Write-Host ""
    Write-Host "[2/3] Инициализация базы данных..."
    python manage.py migrate
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ОШИБКА: Не удалось инициализировать БД" -ForegroundColor Red
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
    Write-Host "[OK] БД готова"
} else {
    Write-Host "[OK] БД уже существует"
}

Write-Host ""
Write-Host "[3/3] Запуск сервера..."
Write-Host ""
Write-Host "========================================"
Write-Host "Откройте браузер: http://127.0.0.1:8000/"
Write-Host "Для остановки нажмите: Ctrl+C"
Write-Host "========================================" 
Write-Host ""

# Запуск сервера
python manage.py runserver
