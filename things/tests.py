from django.test import TestCase
from things.models import Thing
from django.core.exceptions import ValidationError


class ThingModelTest(TestCase):
    def setUp(self):
        self.thing = Thing(
            name='a thing',
            description='This is the description of a thing',
            quantity=5
        )
        self.thing.save()

    def test_valid_thing(self):
        self._assert_thing_is_valid()

    def test_name_must_be_unique(self):
        self.another_thing = Thing(
            name='another thing',
            description='This is the description of the other thing',
            quantity=5
        )
        self.another_thing.save()
        self.thing.name = 'another thing'
        self._assert_thing_is_invalid()

    def test_name_must_not_be_blank(self):
        self.thing.name = ''
        self._assert_thing_is_invalid()

    def test_name_may_be_30_characters(self):
        self.thing.name = 'x' * 30
        self._assert_thing_is_valid()

    def test_name_may_not_be_31_characters(self):
        self.thing.name = 'x' * 31
        self._assert_thing_is_invalid()

    def test_description_can_be_not_unique(self):
        self.another_thing = Thing(
            name='another thing',
            description='This is the description of the other thing',
            quantity=5
        )
        self.another_thing.save()
        self.thing.description = 'This is the description of the other thing'
        self._assert_thing_is_valid()

    def test_description_may_be_blank(self):
        self.thing.description = ''
        self._assert_thing_is_valid()

    def test_description_may_be_120_characters(self):
        self.thing.description = 'x' * 120
        self._assert_thing_is_valid()

    def test_description_may_not_be_121_characters(self):
        self.thing.description = 'x' * 121
        self._assert_thing_is_invalid()

    def test_quality_can_be_not_unique(self):
        self.another_thing = Thing(
            name='another thing',
            description='This is the description of the other thing',
            quantity=10
        )
        self.another_thing.save()
        self.thing.quantity = 10
        self._assert_thing_is_valid()

    def test_quantity_may_be_0(self):
        self.thing.quantity = 0
        self._assert_thing_is_valid()

    def test_quantity_may_be_100(self):
        self.thing.quantity = 100
        self._assert_thing_is_valid()

    def test_quantity_may_not_be_negative(self):
        self.thing.quantity = -1
        self._assert_thing_is_invalid()

    def test_quantity_may_not_be_101(self):
        self.thing.quantity = 101
        self._assert_thing_is_invalid()

    def _assert_thing_is_valid(self):
        try:
            self.thing.full_clean()
        except ValidationError:
            self.fail('Test thing object should be valid')

    def _assert_thing_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.thing.full_clean()
