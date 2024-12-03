from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from datetime import datetime  # noqa: TCH003
from typing import Literal

from pydantic import BaseModel
from typing_extensions import TypedDict

from .typing import StrEnum

Unit = Literal[
    "cl", "cm", "dl", "l",
    "g", "hg", "kg",
    "m", "m100", "ml",
    "pair", "dosage",
    "piece", "portion", "squareMeter"
]


class PhysicalStoreGroup(StrEnum):
    MENY_NO = "MENY_NO"
    SPAR_NO = "SPAR_NO"
    JOKER_NO = "JOKER_NO"
    ODA_NO = "ODA_NO"
    ENGROSSNETT_NO = "ENGROSSNETT_NO"
    NAERBUTIKKEN = "NAERBUTIKKEN"
    BUNNPRIS = "BUNNPRIS"
    KIWI = "KIWI"
    REMA_1000 = "REMA_1000"
    EUROPRIS_NO = "EUROPRIS_NO"
    HAVARISTEN = "HAVARISTEN"
    HOLDBART = "HOLDBART"
    FUDI = "FUDI"
    COOP_NO = "COOP_NO"
    COOP_MARKED = "COOP_MARKED"
    MATKROKEN = "MATKROKEN"
    COOP_MEGA = "COOP_MEGA"
    COOP_PRIX = "COOP_PRIX"
    COOP_OBS = "COOP_OBS"
    COOP_EXTRA = "COOP_EXTRA"
    COOP_BYGGMIX = "COOP_BYGGMIX"
    COOP_OBS_BYGG = "COOP_OBS_BYGG"
    COOP_ELEKTRO = "COOP_ELEKTRO"
    ARK = "ARK"
    NORLI = "NORLI"
    ADLIBRIS = "ADLIBRIS"


class KassalappBaseModel(BaseModel):
    """Kassalapp base model."""

    _detail_attrs: set[int] | set[str] | dict[int, any] | dict[str, any] | None

    def model_dump(
        self,
        **kwargs: any,
    ):
        return super().model_dump(mode='json', exclude_none=True, exclude_unset=True, **kwargs)


class KassalappResource(KassalappBaseModel, ABC):
    """Kassalapp resource."""

    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class AllergenItem:
    code: str
    display_name: str
    contains: str


class Icon(TypedDict):
    svg: str | None
    png: str | None


@dataclass
class LabelItem:
    name: str | None
    display_name: str | None
    description: str | None
    organization: str | None
    alternative_names: str | None
    type: str | None
    year_established: int | None
    about: str | None
    note: str | None
    icon: Icon | None


@dataclass
class NutritionItem:
    code: str
    display_name: str
    amount: float
    unit: str


class OpeningHours(TypedDict):
    monday: str | None
    tuesday: str | None
    wednesday: str | None
    thursday: str | None
    friday: str | None
    saturday: str | None
    sunday: str | None


class Position(TypedDict):
    lat: float
    lng: float


class ProximitySearch(Position):
    km: float


class PhysicalStore(KassalappResource):
    id: int | None
    group: PhysicalStoreGroup | None
    name: str | None
    address: str | None
    phone: str | None
    email: str | None
    fax: str | None
    logo: str | None
    website: str | None
    detailUrl: str | None
    position: Position | None
    openingHours: OpeningHours | None

    def model_dump_essentials(self, **kwargs: any):
        return super().model_dump(
            exclude={
                "address": True,
                "phone": True,
                "email": True,
                "fax": True,
                "logo": True,
                "website": True,
                "detailUrl": True,
            },
            **kwargs,
        )


class ProductCategory(TypedDict):
    id: int
    depth: int
    name: str


class Store(TypedDict):
    name: str
    code: str | None
    url: str | None
    logo: str | None


class Price(TypedDict):
    price: float
    date: datetime


class CurrentPrice(Price):
    unit_price: float | None


class ProductBase(KassalappResource):
    name: str | None = None
    vendor: str | None = None
    brand: str | None = None
    description: str | None = None
    ingredients: str | None = None
    url: str | None = None
    image: str | None = None
    category: list[ProductCategory] | None = None
    store: Store | None = None
    weight: float | None = None
    weight_unit: Unit | None = None
    price_history: list[Price] | None = None

    def model_dump_essentials(self, **kwargs: any):
        return super().model_dump(
            exclude={
                "vendor": True,
                "ingredients": True,
                "url": True,
                "image": True,
                "category": True,
                "store": {
                    "code": True,
                    "url": True,
                    "logo": True,
                },
                "weight": True,
                "weight_unit": True,
                "price_history": True,
            },
            **kwargs,
        )


class Product(ProductBase):
    ean: str | None
    current_price: float | None
    current_unit_price: float | None
    allergens: list[AllergenItem] | None
    nutrition: list[NutritionItem] | None
    labels: list[LabelItem] | None

    def model_dump_essentials(self, **kwargs: any):
        return super().model_dump(
            exclude={
                "allergens": True,
                "nutrition": True,
                "labels": {
                    "__all__": {
                        "display_name",
                        "description",
                        "organization",
                        "alternative_names",
                        "type",
                        "year_established",
                        "about",
                        "note",
                        "icon",
                    },
                },
            },
            **kwargs,
        )


class ProductComparisonItem(ProductBase):
    current_price: CurrentPrice | None
    kassalapp: dict[str, str]


class ProductComparison(KassalappBaseModel):
    ean: str | None
    products: list[ProductComparisonItem] | None
    allergens: list[AllergenItem] | None
    nutrition: list[NutritionItem] | None
    labels: list[LabelItem] | None


class ShoppingListItem(KassalappResource):
    text: str | None
    checked: bool
    product: ProductComparison | None

    def model_dump_essentials(self, **kwargs: any):
        return super().model_dump(
            exclude={
                "product": {
                    "products": {
                        "__all__": {
                            "created_at": True,
                            "updated_at": True,
                            "vendor": True,
                            "ingredients": True,
                            "url": True,
                            "image": True,
                            "category": True,
                            "store": {
                                "code": True,
                                "url": True,
                                "logo": True,
                            },
                            "weight": True,
                            "weight_unit": True,
                            "price_history": True,
                            "kassalapp": True,
                        },
                    },
                    "allergens": True,
                    "nutrition": True,
                    "labels": True,
                    # "labels": {
                    #     "__all__": {
                    #         "display_name",
                    #         "description",
                    #         "organization",
                    #         "alternative_names",
                    #         "type",
                    #         "year_established",
                    #         "about",
                    #         "note",
                    #         "icon",
                    #     },
                    # },
                },
            },
            **kwargs,
        )


class ShoppingList(KassalappResource):
    title: str
    items: list[ShoppingListItem] | None = None

    def model_dump_essentials(self, **kwargs: any):
        return super().model_dump(
            exclude={
                "items": {
                    "__all__": {
                        "allergens": True,
                        "nutrition": True,
                        "labels": {
                            "__all__": {
                                "display_name",
                                "description",
                                "organization",
                                "alternative_names",
                                "type",
                                "year_established",
                                "about",
                                "note",
                                "icon",
                            },
                        },
                    },
                },
            },
            **kwargs,
        )


class MessageResponse(KassalappBaseModel):
    message: str


class StatusResponse(KassalappBaseModel):
    status: str


class Webhook(KassalappResource):
    name: str | None = None
    url: str
    secret: str | None = None
    eans: list[str] | None = None
    ids: list[str] | None = None
