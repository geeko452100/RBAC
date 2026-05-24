from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.role import Role

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True) # Allow an admin to lock the file 

    # Every user has only ONE role ID assigned
    # role_id: Mapped[int] = mapped_column(ForeignKey("role.id", ondelete="RESTRICT"))

    # Send the data back to the role model
    # role: Mapped["Role"] = relationship(back_populates="users")