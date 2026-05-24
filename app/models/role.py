from typing import TYPE_CHECKING # Use this to get the IDE to shut up.
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User

# Link table matching schema
role_permission_association = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("role.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(200), nullable=True)

class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True) 

    permissions: Mapped[list[Permission]] = relationship(
        secondary=role_permission_association
    )

    # Increase awareness of users in role increasing efficiency, and preventing accidental or malicious deletions
    users: Mapped[list["User"]] = relationship(
        back_populates="role",
        passive_deletes=True
    )
