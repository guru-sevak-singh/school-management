### Create a virtual environment & install dependencies:
1. python -m venv venv
2. source venv/bin/activate   # Mac/Linux
3. venv\Scripts\activate      # Windows
4. pip install -r requirements.txt



### Database Setup
1. Install PostgreSQL (https://www.postgresql.org/download/).
2. Create a database (e.g., `schooldb`).
3. Update `config.py` or `.env` with your database credentials.


### Run migrations & start server:
1. flask db upgrade
2. flask run
