import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from resources.database_client import Base


class OccasionEnum(enum.Enum):
    BIRTHDAY = "birthday"
    ANNIVERSARY = "anniversary"
    BUSINESS = "business"
    DATE = "date"
    OTHER = "other"


class OrderStatus(enum.Enum):
    PENDING = "pending"
    QUEUED = "queued"
    PAID = "paid"
    PROCESSING = "processing"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethod(enum.Enum):
    PAYPAL = "paypal"
    STRIPE = "stripe"
    MOCK = "mock"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    restaurants = relationship(
        "Restaurant", back_populates="category", cascade="all, delete-orphan"
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    role = Column(String, nullable=False, default="user")
    provider = Column(String, nullable=False, default="local")

    google_id = Column(String, unique=True, nullable=True)
    microsoft_id = Column(String, unique=True, nullable=True)

    name = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    restaurant = relationship("Restaurant", back_populates="owner", uselist=False)
    orders = relationship(
        "Order",
        back_populates="user",
        foreign_keys="[Order.user_id]",
        cascade="all, delete-orphan",
    )
    deliveries = relationship(
        "Order", back_populates="driver", foreign_keys="[Order.driver_id]"
    )
    fulfillments = relationship(
        "Order", back_populates="employee", foreign_keys="[Order.employee_id]"
    )
    reviews = relationship(
        "Review", back_populates="user", cascade="all, delete-orphan"
    )
    surveys = relationship(
        "Survey", back_populates="user", cascade="all, delete-orphan"
    )
    reservations = relationship(
        "Reservation", back_populates="user", cascade="all, delete-orphan"
    )


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    logoUrl = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))

    owner = relationship("User", back_populates="restaurant")
    category = relationship("Category", back_populates="restaurants")
    food_items = relationship(
        "Food", back_populates="restaurant", cascade="all, delete-orphan"
    )
    reviews_items = relationship(
        "Review", back_populates="restaurant", cascade="all, delete-orphan"
    )
    reservation_items = relationship(
        "Reservation", back_populates="restaurant", cascade="all, delete-orphan"
    )


class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    foodUrl = Column(String, nullable=False)
    calories = Column(Float, nullable=True)
    tags = Column(String, nullable=True)
    ingredients = Column(String, nullable=True)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"))
    restaurant = relationship("Restaurant", back_populates="food_items")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    fulfillment_type = Column(String(50), nullable=False)
    address = Column(Text, nullable=True)

    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    task_id = Column(String(128), nullable=True)
    payment_id = Column(String(128), nullable=True)
    transaction_id = Column(String(128), nullable=True)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    driver_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    employee_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    user = relationship("User", back_populates="orders", foreign_keys=[user_id])
    driver = relationship("User", back_populates="deliveries", foreign_keys=[driver_id])
    employee = relationship(
        "User", back_populates="fulfillments", foreign_keys=[employee_id]
    )

    payment = relationship("Payment", back_populates="order", uselist=False)
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    subtotal = Column(Float, nullable=False)

    food_id = Column(Integer, ForeignKey("food.id", ondelete="CASCADE"))
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))

    food = relationship("Food")
    order = relationship("Order", back_populates="items")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    method = Column(Enum(PaymentMethod), nullable=False, default=PaymentMethod.PAYPAL)
    paypal_order_id = Column(String(128), nullable=True)
    paypal_capture_id = Column(String(128), nullable=True)
    paypal_status = Column(String(64), nullable=True)

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    order = relationship("Order", back_populates="payment")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    restaurant = relationship("Restaurant", back_populates="reviews_items")
    user = relationship("User", back_populates="reviews")


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    seats = Column(Integer, nullable=False)
    occasion = Column(Enum(OccasionEnum), nullable=False)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="reservations")
    restaurant = relationship("Restaurant", back_populates="reservation_items")


class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    question_one = Column(String, nullable=False)
    question_two = Column(String, nullable=False)
    question_three = Column(Text, nullable=False)
    question_four = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="surveys")
