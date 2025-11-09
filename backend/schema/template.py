import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
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
    QUEUE = "queued"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PaymentMethod(enum.Enum):
    PAYPAL = "paypal"
    STRIPE = "stripe"
    MOCK = "mock"


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    logoUrl = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"), unique=True)
    owner = relationship("User", back_populates="restaurant")

    food_items = relationship("Food", back_populates="restaurant")
    reviews_items = relationship("Review", back_populates="restaurant")
    reservation_items = relationship("Reservation", back_populates="restaurant")


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

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="food_items")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    content = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
    fulfillment_type = Column(String(50), nullable=False)
    address = Column(Text, nullable=True)
    total = Column(Float, nullable=False)

    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    task_id = Column(String(128), nullable=True)
    payment_id = Column(String(128), nullable=True)
    transaction_id = Column(String(128), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="orders")
    payment = relationship("Payment", back_populates="order", uselist=False)


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
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    surveys = relationship("Survey", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    seats = Column(Integer)
    occasion = Column(Enum(OccasionEnum), nullable=False)
    details = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="reservations")
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="reservation_items")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="reviews_items")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="reviews")


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True, index=True)
    question_one = Column(String, nullable=False)
    question_two = Column(String, nullable=False)
    question_three = Column(Text, nullable=False)
    question_four = Column(Text, nullable=False)

    rating = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="surveys")
