from __future__ import annotations
from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SAEnum, UniqueConstraint, Index

class Rarity(str, Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    ULTRA_RARE = "Ultra Rare"
    SECRET_RARE = "Secret Rare"
    PROMO = "Promo"


class Condition(str, Enum):
    MINT = "MINT"
    NM = "NM"
    LP = "LP"
    MP = "MP"
    HP = "HP"
    DAMAGED = "Damaged"


class Language(str, Enum):
    ES = "ES"
    EN = "EN"
    JP = "JP"
    PT = "PT"
    FR = "FR"
    DE = "DE"
    IT = "IT"
    CN = "CN"
    KR = "KR"


class ComercialCondition(str, Enum):
    COLECCION = "En colección"
    INTERCAMBIO = "Para intercambio"
    VENTA = "En venta"
    RESERVADA = "Reservada"


class ItemTag(SQLModel, table=True):
    item_id: Optional[int] = Field(default=None, foreign_key="inventoryitem.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class InventoryItem(SQLModel, table=True):
    __tablename__ = "inventoryitem"
    __table_args__ = (
        UniqueConstraint(
            "game", "set_code", "set", "number_set", "language", "Condition", "variant",
            name="uq_item_variant"
        ),
        Index("ix_item_search", "name", "set", "game"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(index=True)
    game: str = Field(index=True)
    set: str = Field(index=True)
    set_code: Optional[str] = Field(default=None, index=True)
    number_set: str = Field(index=True)

    rarity: Rarity = Field(sa_column=Column(SAEnum(Rarity, name="rarity"), nullable=False))
    condition: Condition = Field(sa_column=Column(SAEnum(Condition, name="condition"), nullable=False))
    language: Language = Field(sa_column=Column(SAEnum(Language, name="language"), nullable=False))

    quantity: int = Field(default=0, ge=0, index=True)
    location: Optional[str] = None
    comercial_condition: ComercialCondition = Field(
        default=ComercialCondition.COLECCION,
        sa_column=Column(SAEnum(ComercialCondition, name="comercial_condition"), nullable=False)
    )
    variant: Optional[str] = Field(default=None, index=True)
    notes: Optional[str] = None
    image_path: Optional[str] = None

    tags: List["Tag"] = Relationship(back_populates="items", link_model=ItemTag)


class Tag(SQLModel, table=True):
    __tablename__ = "tag"
    __table_args__ = (
        UniqueConstraint("name", name="uq_tag_nombre"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)

    items: List[InventoryItem] = Relationship(back_populates="tags", link_model=ItemTag)

