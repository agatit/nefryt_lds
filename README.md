Nowa wersja detekcji wycieków :)

Uruchomienie modułów backend:

    cd backend
    uv venv
    .venv\Scripts\activate
    uv pip install -e .
    python -m nazwa_modułu

Uruchomienie pełnego testu zapisu trendów i symulatora:

    1. Przygotuj odpowiednie trendy w bazie danych
    2. Przypisz trendom rejestry modbus jako parametry
    3. Przygotuj odpowiednie symulacje, wykorzystujące aktywne trendy, w bazie danych
    4. Uruchom moduł trends_writer: python -m trends_writer
    5. Dostosuj skrypt generowania danych i uruchom go: python .\utils\trends_writer_data_generator.py
    (WIP) 6. Uruchom moduł simulator: python -m simulator
    
Uruchomienie testów:

    cd backend
    uv venv
    .venv\Scripts\activate
    uv pip install -e .[dev]
    pytest

Przed uruchomieniem testów wymagane jest utworzenie w katalogu backend pliku .env, którego zawartość będzie zawierała przypisane do zmiennej PASSWORD_TEST_DB hasło dostępu do bazy danych

Uruchomienie frontendu:

    cd frontend
    npm install
    npm run rollup
    npm run dev
