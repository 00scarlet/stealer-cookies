# SystemService Utility

## Overview
SystemService is a Python-based utility designed to collect and process browser data and Telegram session information from a Windows system. It compiles data such as browser passwords, cookies, and Telegram session files, then sends them to a specified Telegram chat via a bot. The utility is packaged as a Windows executable using `cx_Freeze`.

**Note**: This project appears to involve sensitive data collection. Ensure you have explicit permission to access and process any data, and comply with all applicable laws and ethical guidelines regarding privacy and security.

## Features
- **Browser Data Extraction**: Collects passwords and cookies from popular browsers (e.g., Chrome, Edge, Firefox, Opera, Brave, etc.).
- **Telegram Session Collection**: Gathers Telegram session files (`tdata`) from supported clients (e.g., Telegram Desktop, AyuGram, Kotatogram).
- **Screenshot Capture**: Takes a system screenshot and sends it via Telegram.
- **IP and Geolocation**: Retrieves IP address and city information using the `ip-api.com` service.
- **Data Encryption Handling**: Decrypts browser passwords and cookies using the master key from the browser's Local State.
- **Executable Packaging**: Converts the Python script into a Windows executable (`WindowsUpdate.exe`) using `cx_Freeze`.

## Requirements
- **Operating System**: Windows (due to `win32crypt` and `Win32GUI` dependencies).
- **Python Version**: Python 3.6+.
- **Dependencies**: Listed in `setup.py` and include:
  - `cx_Freeze`
  - `requests`
  - `psutil`
  - `pycryptodome` (for AES decryption)
  - `pywin32` (for `win32crypt`)
  - `Pillow` (for screenshot capture)
  - Standard Python libraries: `os`, `json`, `base64`, `sqlite3`, `shutil`, `zipfile`, `tempfile`, `pathlib`, `datetime`

## Installation
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Alternatively, install the required packages manually:
   ```bash
   pip install cx_Freeze requests psutil pycryptodome pywin32 Pillow
   ```

2. **Configure Telegram Bot**:
   - Obtain a Telegram bot token from [BotFather](https://t.me/BotFather).
   - Set the `BOT_TOKEN` and `CHAT_ID` in `program.py` to your bot token and target chat ID.

3. **Build the Executable**:
   ```bash
   python setup.py build
   ```
   This generates the `WindowsUpdate.exe` executable in the `build` directory.

## Usage
1. **Run the Executable**:
   - Execute `WindowsUpdate.exe` from the `build` directory.
   - The program runs silently (console window is hidden on Windows) and performs the following:
     - Captures a screenshot and sends it to the specified Telegram chat.
     - Collects browser passwords and cookies, saving them to a text file and sending it via Telegram.
     - Collects Telegram session files, zips them, and sends the archive via Telegram.

2. **Run the Python Script Directly** (for development):
   ```bash
   python program.py
   ```

## File Structure
- **setup.py**: Configuration for `cx_Freeze` to build the executable.
- **program.py**: Main script containing the `DataStealer` class with methods for data collection and Telegram communication.
- **build/**: Directory containing the compiled executable (generated after running `setup.py`).

## Security and Anti-Detection
- The script checks for virtualization environments (e.g., VMware, VirtualBox, QEMU) and exits if detected.
- It checks for debugging environments and exits if a debugger is present.
- The console window is hidden on Windows for stealth operation.
- Temporary files (e.g., database copies, screenshots, zip archives) are removed after use.

## Limitations
- **Platform**: Windows-only due to dependencies like `win32crypt` and `Win32GUI`.
- **Browser Support**: Limited to specific browsers (Chrome, Edge, Firefox, etc.) and profiles (e.g., "Default" for Chromium-based browsers).
- **Telegram Clients**: Supports specific Telegram clients (e.g., Telegram Desktop, AyuGram).
- **Network Dependency**: Requires internet access for Telegram API and IP geolocation.

## Ethical Considerations
This utility is designed to collect sensitive user data (e.g., passwords, cookies, Telegram sessions). Use it responsibly and only with explicit consent from users whose data is being processed. Unauthorized data collection may violate privacy laws and Telegram's terms of service.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for bug reports or feature requests.

## License
This project is unlicensed. Use it at your own risk and ensure compliance with all applicable laws and regulations.


# (RUS) Утилита SystemService

## Обзор
SystemService — это утилита на Python, предназначенная для сбора и обработки данных браузеров и сессий Telegram на системах Windows. Она собирает данные, такие как пароли и файлы cookie браузеров, а также файлы сессий Telegram (`tdata`), и отправляет их в указанный чат Telegram через бота. Утилита компилируется в исполняемый файл для Windows с использованием `cx_Freeze`.

**Примечание**: Этот проект связан со сбором конфиденциальных данных. Убедитесь, что у вас есть явное разрешение на доступ и обработку данных, и соблюдайте все применимые законы и этические нормы в отношении конфиденциальности и безопасности.

## Возможности
- **Извлечение данных браузеров**: Сбор паролей и файлов cookie из популярных браузеров (например, Chrome, Edge, Firefox, Opera, Brave и др.).
- **Сбор сессий Telegram**: Извлечение файлов сессий (`tdata`) из поддерживаемых клиентов (например, Telegram Desktop, AyuGram, Kotatogram).
- **Снимок экрана**: Создание снимка экрана системы и отправка его через Telegram.
- **IP и геолокация**: Получение IP-адреса и информации о городе с использованием сервиса `ip-api.com`.
- **Обработка шифрования данных**: Расшифровка паролей и файлов cookie браузеров с использованием мастер-ключа из Local State браузера.
- **Упаковка в исполняемый файл**: Преобразование Python-скрипта в исполняемый файл Windows (`WindowsUpdate.exe`) с помощью `cx_Freeze`.

## Требования
- **Операционная система**: Windows (из-за зависимостей `win32crypt` и `Win32GUI`).
- **Версия Python**: Python 3.6+.
- **Зависимости**: Указаны в `setup.py` и включают:
  - `cx_Freeze`
  - `requests`
  - `psutil`
  - `pycryptodome` (для расшифровки AES)
  - `pywin32` (для `win32crypt`)
  - `Pillow` (для захвата снимков экрана)
  - Стандартные библиотеки Python: `os`, `json`, `base64`, `sqlite3`, `shutil`, `zipfile`, `tempfile`, `pathlib`, `datetime`

## Установка
1. **Установка зависимостей**:
   ```bash
   pip install -r requirements.txt
   ```
   Или установите необходимые пакеты вручную:
   ```bash
   pip install cx_Freeze requests psutil pycryptodome pywin32 Pillow
   ```

2. **Настройка бота Telegram**:
   - Получите токен бота Telegram через [BotFather](https://t.me/BotFather).
   - Укажите `BOT_TOKEN` и `CHAT_ID` в файле `program.py` для вашего токена бота и ID целевого чата.

3. **Сборка исполняемого файла**:
   ```bash
   python setup.py build
   ```
   Это создаст исполняемый файл `WindowsUpdate.exe` в папке `build`.

## Использование
1. **Запуск исполняемого файла**:
   - Запустите `WindowsUpdate.exe` из папки `build`.
   - Программа работает в фоновом режиме (консольное окно скрыто в Windows) и выполняет следующее:
     - Создает снимок экрана и отправляет его в указанный чат Telegram.
     - Собирает пароли и файлы cookie браузеров, сохраняет их в текстовый файл и отправляет через Telegram.
     - Собирает файлы сессий Telegram, архивирует их и отправляет архив через Telegram.

2. **Запуск Python-скрипта напрямую** (для разработки):
   ```bash
   python program.py
   ```

## Структура файлов
- **setup.py**: Конфигурация для `cx_Freeze` для создания исполняемого файла.
- **program.py**: Основной скрипт, содержащий класс `DataStealer` с методами для сбора данных и взаимодействия с Telegram.
- **build/**: Папка, содержащая скомпилированный исполняемый файл (создается после выполнения `setup.py`).

## Безопасность и антидетекция
- Скрипт проверяет наличие виртуализированных сред (например, VMware, VirtualBox, QEMU) и завершает работу, если они обнаружены.
- Проверяет наличие отладочных сред и завершает работу при их обнаружении.
- Консольное окно скрыто в Windows для скрытной работы.
- Временные файлы (например, копии баз данных, снимки экрана, архивы) удаляются после использования.

## Ограничения
- **Платформа**: Только Windows из-за зависимостей, таких как `win32crypt` и `Win32GUI`.
- **Поддержка браузеров**: Ограничена определенными браузерами (Chrome, Edge, Firefox и др.) и профилями (например, "Default" для браузеров на базе Chromium).
- **Клиенты Telegram**: Поддерживает определенные клиенты Telegram (например, Telegram Desktop, AyuGram).
- **Сетевая зависимость**: Требуется доступ в интернет для работы с API Telegram и геолокацией IP.

## Этические аспекты
Эта утилита предназначена для сбора конфиденциальных данных пользователей (например, паролей, файлов cookie, сессий Telegram). Используйте ее ответственно и только с явного согласия пользователей, чьи данные обрабатываются. Несанкционированный сбор данных может нарушать законы о конфиденциальности и условия использования Telegram.

## Вклад в проект
Приветствуются любые вклады! Пожалуйста, отправляйте запросы на включение изменений (pull requests) или открывайте вопросы (issues) для сообщений об ошибках или предложений по улучшению.

## Лицензия
Этот проект не имеет лицензии. Используйте его на свой страх и риск, соблюдая все применимые законы и правила.
