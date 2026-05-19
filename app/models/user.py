from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.rbac import Base, Role

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # For Security, store the hashed password string
    hashed_password: Mapped[str] = mapped_column(String(255))

    # For added security, allow an admin to lock an account's access immediately
    is_active: Mapped[bool] = mapped_column(default=True)

    # Every user has only ONE role ID assigned
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"))

    role: Mapped["Role"] = relationship()