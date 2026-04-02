from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Text, DateTime, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

db = SQLAlchemy()


# USERS
class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(
        String(255), nullable=False)  # FIX seguridad
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    # Relaciones
    posts = relationship("Post", back_populates="user",
                         cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user",
                         cascade="all, delete-orphan")

    # Seguidores
    following = relationship(
        "Follower",
        foreign_keys="Follower.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan"
    )

    followers = relationship(
        "Follower",
        foreign_keys="Follower.following_id",
        back_populates="following",
        cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
        }


# POST
class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)

    # Relaciones
    user = relationship("Users", back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post",
                         cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id
        }


# COMMENT
class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id"), nullable=False, index=True)

    # Relaciones
    user = relationship("Users", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id,
            "post_id": self.post_id
        }


# LIKE
class Like(db.Model):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_like"),
    )

    # Relaciones
    user = relationship("Users", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id
        }


# FOLLOWER
class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)

    follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)
    following_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="unique_follow"),
        CheckConstraint("follower_id != following_id", name="no_self_follow"),
    )

    follower = relationship(
        "Users",
        foreign_keys=[follower_id],
        back_populates="following"
    )

    following = relationship(
        "Users",
        foreign_keys=[following_id],
        back_populates="followers"
    )

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "following_id": self.following_id
        }


# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import String, Boolean
# from sqlalchemy.orm import Mapped, mapped_column

# db = SQLAlchemy()

# class users(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(nullable=False)
#     is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }
