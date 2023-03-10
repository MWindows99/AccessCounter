# AccessCounter
A simple access counter written in Python.

## Setup

### 1. Create a Database
```sql
CREATE DATABASE AccessCount DEFAULT CHARACTER SET utf8;
GRANT ALL ON AccessCount.* TO AccessCount@localhost IDENTIFIED BY 'AccessCount';
FLUSH PRIVILEGES;
quit;
```

### 2. Create some DB tables
```sql
use AccessCount;
CREATE TABLE IF NOT EXISTS `AccessCounter` (
    `IP` TEXT NOT NULL,
    `TIMESTAMP` DATETIME NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
FLUSH PRIVILEGES;
quit;
```

```sql
use AccessCount;
CREATE TABLE IF NOT EXISTS `Counter` (
    `ID` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `COUNT` INTEGER NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
FLUSH PRIVILEGES;
quit;
```
### 3. Insert a data
```sql
use AccessCount;
INSERT INTO Counter VALUES(1, 0);
FLUSH PRIVILEGES;
quit;
```

### 4. Install dependencies
```bash
pip install -U -r requirements.txt
```

## Usage

```bash
python main.py
```
