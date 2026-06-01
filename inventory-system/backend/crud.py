from sqlalchemy.orm import Session
import models, schemas

# ── Products ──────────────────────────────────────────────
def get_products(db: Session):
    return db.query(models.Product).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_sku(db: Session, sku: str):
    return db.query(models.Product).filter(models.Product.sku == sku).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    data = product.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(db_product, k, v)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True

# ── Customers ─────────────────────────────────────────────
def get_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return False
    db.delete(db_customer)
    db.commit()
    return True

# ── Orders ────────────────────────────────────────────────
def get_orders(db: Session):
    return db.query(models.Order).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def create_order(db: Session, order: schemas.OrderCreate):
    customer = get_customer(db, order.customer_id)
    if not customer:
        raise ValueError("Customer not found")

    total = 0.0
    items_data = []
    for item in order.items:
        product = get_product(db, item.product_id)
        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        if product.quantity < item.quantity:
            raise ValueError(
                f"Insufficient stock for '{product.name}'. "
                f"Available: {product.quantity}, Requested: {item.quantity}"
            )
        total += product.price * item.quantity
        items_data.append((product, item.quantity))

    db_order = models.Order(customer_id=order.customer_id, total_amount=total)
    db.add(db_order)
    db.flush()

    for product, qty in items_data:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            quantity=qty,
            unit_price=product.price,
        )
        db.add(db_item)
        product.quantity -= qty

    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if not db_order:
        return False
    # Restore stock
    for item in db_order.items:
        item.product.quantity += item.quantity
    db.delete(db_order)
    db.commit()
    return True

# ── Dashboard ─────────────────────────────────────────────
def get_dashboard(db: Session):
    total_products = db.query(models.Product).count()
    total_customers = db.query(models.Customer).count()
    total_orders = db.query(models.Order).count()
    low_stock = db.query(models.Product).filter(models.Product.quantity <= 5).all()
    return {
        "total_products": total_products,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "low_stock_products": [
            {"id": p.id, "name": p.name, "sku": p.sku, "quantity": p.quantity}
            for p in low_stock
        ],
    }
