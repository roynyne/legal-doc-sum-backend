Run

pip install -r requirements.txt (present in frontend and backend)

# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Start frontend
cd frontend
streamlit run streamlit_app.py
