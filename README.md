# DFENCY Workflow Automation – Selenium (Python)

This project automates the **DFENCY application workflow** using **Selenium with Python and PyTest**.  
It covers functional automation of major modules including inventory, production, employees, machines, operations, rejection reasons, and more.


---


## ✅ Features Implemented

- Deterministic test execution (no random selection)
- Stable MUI dropdown handling
- JavaScript-based submit clicks to avoid UI overlay issues
- Post-submit stabilization waits
- Reusable UI helper utilities
- Structured test organization
- Inventory inward/outward & stock adjustment coverage
- Production entry automation
- Rejection reason workflow automation

---

## 🔧 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Jagasri04/Dfency_test.git
cd Dfency_test
```

### 2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

Run all tests:
python -m pytest -v

Run specific test:
python -m pytest tests/test_rejection_reasons.py -v

