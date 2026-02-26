# DFENCY Workflow Automation – Selenium (Python)

This project automates the **DFENCY application workflow** using **Selenium with Python and PyTest**.  
It validates a flow starting from login, user management, and finally production data entry.

---

## Automated Workflow 

The automation follows this exact sequence:

1. **Login** to the DFENCY application  
2. Navigate to **Users section**
3. **Add a new user** and validate user creation
4. Navigate to **Production Data Entry**
5. Fill **Basic Information**
6. Fill **Component Information**
7. Enter **Production Schedule**
8. Enter **Quantity Tracking values**
9. Click **Add Material** and fill
10. Click **Add Idle Time** and fill
11. Submit production entry and validate successful completion


## 🚀 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Jagasri04/Dfency_test.git
cd microvsta
```

2️⃣ (Optional) Create virtual environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ Run
python -m pytest tests/test_dfency_flow.py
