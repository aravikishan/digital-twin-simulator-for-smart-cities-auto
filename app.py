from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./smart_city.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class CityData(Base):
    __tablename__ = "city_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    population = Column(Integer)
    area = Column(Float)
    gdp = Column(Float)

class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id = Column(Integer, primary_key=True, index=True)
    theme = Column(String)
    default_view = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
def seed_data():
    db = SessionLocal()
    if not db.query(CityData).first():
        demo_city_data = [
            CityData(id=1, name="Metropolis", population=1000000, area=500.5, gdp=30000.0),
            CityData(id=2, name="Gotham", population=1500000, area=700.2, gdp=45000.0)
        ]
        db.add_all(demo_city_data)
        db.commit()
    if not db.query(UserSettings).first():
        demo_user_settings = UserSettings(user_id=1, theme="light", default_view="overview")
        db.add(demo_user_settings)
        db.commit()
    db.close()

seed_data()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/data", response_class=HTMLResponse)
async def get_data_explorer(request: Request):
    return templates.TemplateResponse("data.html", {"request": request})

@app.get("/api-docs", response_class=HTMLResponse)
async def get_api_docs(request: Request):
    return templates.TemplateResponse("api_docs.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# API Endpoints
@app.get("/api/city-data")
async def get_city_data():
    db = SessionLocal()
    data = db.query(CityData).all()
    db.close()
    return data

@app.get("/api/user-settings")
async def get_user_settings():
    db = SessionLocal()
    settings = db.query(UserSettings).all()
    db.close()
    return settings

@app.post("/api/data-filter")
async def post_data_filter():
    # Implement filtering logic here
    return {"message": "Filtered data"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
