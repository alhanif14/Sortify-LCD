import enum
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class RedeemStatus(enum.Enum):
    AVAILABLE = "available"
    REDEEMED = "redeemed"
    EXPIRED = "expired"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column("password_hash", String, nullable=False)
    point = Column(Integer, default=0, nullable=False)

    redeemed_vouchers = relationship("UserVoucherRedeem", back_populates="user")

class WasteDetectionLog(Base):
    __tablename__ = "waste_detection_log" 

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    waste_type = Column(String, nullable=False)
    qr_code = Column(String, nullable=True)
    username = Column(String, nullable=True)
    point = Column(Integer, default=0)

class Voucher(Base):
    __tablename__ = "vouchers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    terms_conditions = Column(String)
    point_cost = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

class UserVoucherRedeem(Base):
    __tablename__ = "user_voucher_redeem"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    voucher_id = Column(Integer, ForeignKey("vouchers.id"), nullable=False)
    redeem_date = Column(DateTime, default=datetime.utcnow)
    status = Column(SQLAlchemyEnum(RedeemStatus), default=RedeemStatus.REDEEMED, nullable=False)
    
    user = relationship("User", back_populates="redeemed_vouchers")
    voucher = relationship("Voucher")