from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Order, OrderItem, Product, User
from app.schemas import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderOut])
def list_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not order_in.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must contain at least one item")

    order = Order(user_id=current_user.id)
    for item in order_in.items:
        product = db.get(Product, item.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Not enough stock for {product.name}")

        product.stock -= item.quantity
        order.items.append(OrderItem(product_id=product.id, quantity=item.quantity, unit_price=product.price))

    db.add(order)
    db.commit()
    db.refresh(order)
    return order
