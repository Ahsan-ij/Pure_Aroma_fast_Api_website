from fastapi import FastAPI, Depends, Request, Form,HTTPException,Response
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from passlib.context import CryptContext
from models import User, Product, CartItem  
from database import SessionLocal  
from pydantic import BaseModel, EmailStr
import crud
import bcrypt

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/login_signup", response_class=HTMLResponse)
async def get_login_signup(request: Request):
    user_email = request.cookies.get("user_email")
    user = None
    if user_email:
        db = SessionLocal()
        user = db.query(User).filter(User.email == user_email).first()
    return templates.TemplateResponse("login_signup.html", {"request": request, "user": user})

@app.post("/login", response_class=HTMLResponse)
async def post_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    query = select(User).filter(User.email == email)
    existing_user = db.execute(query).scalar_one_or_none()

    if existing_user and verify_password(password, existing_user.password): # type: ignore
        response = RedirectResponse(url="/index.html", status_code=303)
        response.set_cookie(key="user_email", value=existing_user.email) # type: ignore
        return response
    else:
        return templates.TemplateResponse("login_signup.html", {"request": request, "message": "Invalid email or password"})
    
@app.post("/signup", response_class=HTMLResponse)
async def post_signup(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...), 
    db: Session = Depends(get_db)
):
    query = select(User).filter(User.email == email)
    existing_user = db.execute(query).scalar_one_or_none()

    if existing_user:
        return templates.TemplateResponse("login_signup.html", {"request": request, "message": "Email already exists. Please choose another one."})
    
    hashed_password = hash_password(password)
    new_user = User(email=email, password=hashed_password, name=name) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

   
    return templates.TemplateResponse("login_signup.html", {"request": request, "signup_success": True})


@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/login_signup", status_code=303)
    response.delete_cookie(key="user_email")
    return response




@app.get("/cart", response_class=HTMLResponse)
async def get_cart(request: Request, db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).all()
    return templates.TemplateResponse("cart.html", {"request": request, "cart_items": cart_items})



# @app.post("/remove-from-cart/{item_id}")
# async def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
#     cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
#     if cart_item:
#         db.delete(cart_item)
#         db.commit()
#         return RedirectResponse(url="/cart", status_code=303)
#     else:
#         raise HTTPException(status_code=404, detail="Cart item not found")



@app.get("/search", response_class=HTMLResponse)
async def search(query: str, request: Request, db: Session = Depends(get_db)):
    products = crud.search_products_by_name(db, query)
    return templates.TemplateResponse("search_results.html", {"request": request, "products": products, "query": query})

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# @app.get("/login")
# async def login_form(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @app.get("/signup")
# async def signup_form(request: Request):
#     return templates.TemplateResponse("signup.html", {"request": request})



@app.get("/index.html", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/product.html", response_class=HTMLResponse)
async def get_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    cart_count = db.query(CartItem).count()  
    return templates.TemplateResponse("product.html", {"request": request, "products": products, "cart_count": cart_count})



@app.get("/about.html", response_class=HTMLResponse)
async def read_about_html(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/contact.html", response_class=HTMLResponse)
async def read_contact_html(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/male.html", response_class=HTMLResponse)
async def read_male_products_html(request: Request, db: Session = Depends(get_db)):
    products = crud.get_products_by_gender(db, "men") 
    return templates.TemplateResponse("male.html", {"request": request, "products": products})

@app.get("/female.html", response_class=HTMLResponse)
async def read_female_products_html(request: Request, db: Session = Depends(get_db)):
    products = crud.get_products_by_gender(db, "women")  
    return templates.TemplateResponse("female.html", {"request": request, "products": products})

@app.get("/careers.html", response_class=HTMLResponse)
async def read_careers_html(request: Request):
    return templates.TemplateResponse("careers.html", {"request": request})


@app.get("/privacy.html", response_class=HTMLResponse)
async def read_privacy_html(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})


@app.get("/faq.html", response_class=HTMLResponse)
async def read_faq_html(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})

@app.get("/return.html", response_class=HTMLResponse)
async def read_return_html(request: Request):
    return templates.TemplateResponse("return.html", {"request": request})



