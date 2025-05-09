Nowa wersja detekcji wycieków :)

Uruchomienie modułów backend:

    cd backend
    uv venv
    .venv\Scripts\activate
    uv pip install -e .
    python -m nazwa_modułu
    
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
