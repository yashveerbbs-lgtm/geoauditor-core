from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
import json
import sqlite3
from processor import optimize_boundary

app = FastAPI()

# --- THE SECURITY BRIDGE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- THE MEMORY BANK ---
def init_db():
    conn = sqlite3.connect("geoauditor.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_plots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plot_name TEXT NOT NULL,
            boundary_data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- API ROUTE 1: The Math Engine ---
@app.post("/api/process-coordinates")
async def process_coordinates(request: Request):
    # Upgraded: No more files! We just read the pure JSON text stream
    raw_data = await request.json()
    engine_results = optimize_boundary(raw_data)
    
    return {
        "status": "success",
        "message": "Plot boundary perfectly optimized.",
        "original_data": raw_data,
        "corrected_data": engine_results
    }

# --- API ROUTE 2: Save to Database ---
@app.post("/api/save-plot")
async def save_plot(plot_name: str = Form(...), boundary_data: str = Form(...)):
    conn = sqlite3.connect("geoauditor.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO saved_plots (plot_name, boundary_data) VALUES (?, ?)", (plot_name, boundary_data))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Plot '{plot_name}' safely stored in the vault!"}

# --- API ROUTE 3: Retrieve from Database ---
@app.get("/api/saved-plots")
async def get_saved_plots():
    conn = sqlite3.connect("geoauditor.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, plot_name, boundary_data FROM saved_plots")
    rows = cursor.fetchall()
    conn.close()
    plots = [{"id": row[0], "name": row[1], "data": json.loads(row[2])} for row in rows]
    return {"status": "success", "plots": plots}