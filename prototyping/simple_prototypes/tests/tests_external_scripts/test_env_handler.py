# -*- coding: utf-8 -*-

"""
Модуль test_env_handler представляет из себя набор модульных тестов,
для тестирования компонентов модуля env_handler.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__author__ = "HyacinthusIO"
__version__ = "1.0.0"

import unittest
import os

from typing import Dict, Any

from prototypes.external_scripts.env_handler import *


PATH_TO_TEST_DIR: str = os.path.dirname(__file__)
TEST_DATA_DIR_NAME: str = "test_data"


# ____________________________________________________________________________
class TestLoadEnvFilePositive(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unittest.TestCase.setUpClass()

        cls.path_to_env_file: str = os.path.join(
            PATH_TO_TEST_DIR, TEST_DATA_DIR_NAME, "keys.env"
        )

        cls.path_to_empty_env_file: str = os.path.join(
            PATH_TO_TEST_DIR, TEST_DATA_DIR_NAME, "empty.env"
        )

        # Пары должны соответствовать парам в файле
        cls.expected_env_file_key_values: Dict[str, Any] = {
            "FIRST_KEY": "1010",
            "SECOND_KEY": "Banana",
            "THIRD_KEY": "True",
        }

    # ------------------------------------------------------------------------
    def test_correct_filepath(self) -> None:
        load_env_file(filepath=self.path_to_env_file)

    # ------------------------------------------------------------------------
    def test_load_env_file_return_true(self) -> None:
        result: bool = load_env_file(filepath=self.path_to_env_file)

        self.assertTrue(result)

    # ------------------------------------------------------------------------
    def test_load_empty_env_file_not_raise_exception(self) -> None:
        load_env_file(filepath=self.path_to_empty_env_file)

    # ------------------------------------------------------------------------
    def test_load_empty_env_file_return_false(self) -> None:
        result: bool = load_env_file(filepath=self.path_to_empty_env_file)

        self.assertFalse(result)

    # ------------------------------------------------------------------------
    def test_key_values_after_loading(self) -> None:
        load_env_file(filepath=self.path_to_env_file)

        for key, value in self.expected_env_file_key_values.items():
            with self.subTest(msg=f"Key: {key}, Value: {value}"):
                self.assertEqual(first=value, second=os.getenv(key=key))


# ____________________________________________________________________________
class TestLoadEnvFileNegative(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unittest.TestCase.setUpClass()

        cls.incorrect_path_to_env_file: str = os.path.join(
            PATH_TO_TEST_DIR, "banan", "strawberry.env"
        )

    # ------------------------------------------------------------------------
    def test_file_is_not_found(self) -> None:
        self.assertRaises(
            FileNotFoundError, load_env_file, self.incorrect_path_to_env_file
        )

    # ------------------------------------------------------------------------
    @unittest.expectedFailure
    def test_incorrect_filepath_raise_exception(self) -> None:
        load_env_file(filepath=self.incorrect_path_to_env_file)


# ____________________________________________________________________________
class TestGetKeyValueFromEnvironmentPositive(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unittest.TestCase.setUpClass()

        cls.test_key_correct_name: str = "TEST_KEY"
        cls.test_key_value: str = "I_LIKE_EAT_CHERRY"

    # ------------------------------------------------------------------------
    def test_get_correct_value_from_environment_key(self) -> None:
        os.environ[self.test_key_correct_name] = self.test_key_value

        self.assertEqual(
            first=self.test_key_value,
            second=get_key_value_from_environment(key=self.test_key_correct_name),
        )


# ____________________________________________________________________________
class TestGetKeyValueFromEnvironmentNegative(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unittest.TestCase.setUpClass()

        cls.incorrect_test_key: str = "BANANA_KEY"

    # ------------------------------------------------------------------------
    def test_incorrect_environment_key(self) -> None:
        self.assertRaises(
            KeyError, get_key_value_from_environment, self.incorrect_test_key
        )

    # ------------------------------------------------------------------------
    @unittest.expectedFailure
    def test_incorrect_environment_key_raise_exception(self) -> None:
        get_key_value_from_environment(key=self.incorrect_test_key)


# ____________________________________________________________________________
class TestNormalizeEnvValueTypePositive(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unittest.TestCase.setUpClass()

        cls.test_data: Dict[str, type] = {
            "14155262": int,
            "TRUE": bool,
            "true": bool,
            "FaLsE": bool,
            "false": bool,
            "CupCake155": str,
            "True2": str,
            "BaNan": str,
        }  # <value> : <correct_value_type>

    # ------------------------------------------------------------------------
    def test_correct_return_normalize_env_value_type(self) -> None:
        for value, correct_value_type in self.test_data.items():
            with self.subTest(msg=f"Test: {value} {correct_value_type}"):
                self.assertIsInstance(
                    obj=normalize_env_value_type(env_value=value),
                    cls=correct_value_type,
                )


# ____________________________________________________________________________
class TestNormalizeEnvValueTypeNegative(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unittest.TestCase.setUpClass()

        cls.test_data: Dict[str, type] = {
            "23.1": float,
            "[12, 34, 56]": list,
            "{123, 45, 66}": set,
            "('banana', 'orange', 'blueberry')": tuple,
        }  # <value> : <correct_value_type>

    # ------------------------------------------------------------------------
    def test_unsupported_value_type_return_string(self) -> None:
        for value, correct_value_type in self.test_data.items():
            with self.subTest(msg=f"Test: {value} {correct_value_type}"):
                self.assertIsInstance(
                    obj=normalize_env_value_type(env_value=value),
                    cls=str,
                )
