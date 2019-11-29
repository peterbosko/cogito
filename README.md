# cogito
Projekt zameraný na porozumenie obsahu slovenského textu

Inštalácia:
1. Nainštalovať python min 3.7
2. Nainštalovanie pip-u
3. Clonovanie GITu do adresára C:\python\cogito
4. Inštalácia MySQL DB. Vytvorenie db cogito z dumpu databazy. User cogito. 
5. Vytvorenie virtualneho environmentu s názvom venv.
6. Pustenie virt env venv - env.bat
7. Nainštalovanie všetkých packagov vo venv pip install -r requirements.txt
8. Vytvorenie súboru config/config.py podľa templatu config/config.py.template
9.  Nastavenie správnych hodnôt v súbore config.py
10. Initializácia db - python run.py init_db
11. Pustenie flask servera pomocou run.bat - v cmd v ktorom bolo predtym spustene env.bat
12. http://localhost/
