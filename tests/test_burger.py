import pytest
from unittest.mock import Mock

from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient_types import (
    INGREDIENT_TYPE_FILLING,
    INGREDIENT_TYPE_SAUCE,
)


class TestBurger:

    def test_set_buns(self):
        burger = Burger()
        bun = Bun("black bun", 100)

        burger.set_buns(bun)

        assert burger.bun == bun

    def test_add_ingredient(self):
        burger = Burger()
        ingredient = Mock()

        burger.add_ingredient(ingredient)

        assert burger.ingredients == [ingredient]

    def test_remove_ingredient(self):
        burger = Burger()
        ingredient_1 = Mock()
        ingredient_2 = Mock()

        burger.add_ingredient(ingredient_1)
        burger.add_ingredient(ingredient_2)

        burger.remove_ingredient(0)

        assert burger.ingredients == [ingredient_2]

    def test_move_ingredient(self):
        burger = Burger()
        ingredient_1 = Mock()
        ingredient_2 = Mock()
        ingredient_3 = Mock()

        burger.add_ingredient(ingredient_1)
        burger.add_ingredient(ingredient_2)
        burger.add_ingredient(ingredient_3)

        burger.move_ingredient(0, 2)

        assert burger.ingredients == [
            ingredient_2,
            ingredient_3,
            ingredient_1,
        ]

    @pytest.mark.parametrize(
        "bun_price, ingredient_prices, expected_price",
        [
            (100, [], 200),
            (100, [50], 250),
            (100, [50, 25], 275),
            (200, [100, 50], 550),
        ],
    )
    def test_get_price(
        self,
        bun_price,
        ingredient_prices,
        expected_price,
    ):
        burger = Burger()

        bun = Mock()
        bun.get_price.return_value = bun_price
        burger.set_buns(bun)

        for price in ingredient_prices:
            ingredient = Mock()
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)

        assert burger.get_price() == expected_price

    @pytest.mark.parametrize(
        "ingredient_type, ingredient_name, expected_type",
        [
            (INGREDIENT_TYPE_SAUCE, "hot sauce", "sauce"),
            (INGREDIENT_TYPE_FILLING, "cutlet", "filling"),
        ],
    )
    def test_get_receipt_ingredient(
        self,
        ingredient_type,
        ingredient_name,
        expected_type,
    ):
        burger = Burger()

        bun = Mock()
        bun.get_name.return_value = "black bun"
        bun.get_price.return_value = 100
        burger.set_buns(bun)

        ingredient = Mock()
        ingredient.get_type.return_value = ingredient_type
        ingredient.get_name.return_value = ingredient_name
        ingredient.get_price.return_value = 50
        burger.add_ingredient(ingredient)

        expected_receipt = (
            "(==== black bun ====)\n"
            f"= {expected_type} {ingredient_name} =\n"
            "(==== black bun ====)\n"
            "\n"
            "Price: 250"
        )

        assert burger.get_receipt() == expected_receipt

    def test_get_receipt(self):
        burger = Burger()

        bun = Mock()
        bun.get_name.return_value = "black bun"
        bun.get_price.return_value = 100
        burger.set_buns(bun)

        ingredient_1 = Mock()
        ingredient_1.get_type.return_value = INGREDIENT_TYPE_SAUCE
        ingredient_1.get_name.return_value = "hot sauce"
        ingredient_1.get_price.return_value = 100

        ingredient_2 = Mock()
        ingredient_2.get_type.return_value = INGREDIENT_TYPE_FILLING
        ingredient_2.get_name.return_value = "cutlet"
        ingredient_2.get_price.return_value = 100

        burger.add_ingredient(ingredient_1)
        burger.add_ingredient(ingredient_2)

        expected_receipt = (
            "(==== black bun ====)\n"
            "= sauce hot sauce =\n"
            "= filling cutlet =\n"
            "(==== black bun ====)\n"
            "\n"
            "Price: 400"
        )

        assert burger.get_receipt() == expected_receipt
