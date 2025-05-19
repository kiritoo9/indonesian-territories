# 🇮🇩 Indonesian Territories Migration Tool

This project is a utility to **migrate and populate data** for all administrative territories in Indonesia, including:

- **Provinces**
- **Cities/Regencies**
- **Districts (Kecamatan)**
- **Subdistricts/Villages (Kelurahan/Desa)**

It reads structured JSON data and performs efficient **batch inserts** into a PostgreSQL database using UUIDs and `.env`-based configuration.

---

## 📦 Features

- Structured schema mapping from JSON to PostgreSQL
- UUIDv4 generation for unique primary keys
- Fast batch inserts for high performance
- .env-based configuration for secure connection handling
- Clean modular code using Python

---

## 🛠️ Requirements

- Python 3.11+
- PostgreSQL
- pip packages:
  - `psycopg2` or `psycopg2-binary`
  - `python-dotenv`

Install dependencies:

```bash
pip install psycopg2-binary python-dotenv
```

Run application:

```bash
python app.py province
python app.py city
python app.py district
python app.py subdistrict
```

## Author
kiritoo9