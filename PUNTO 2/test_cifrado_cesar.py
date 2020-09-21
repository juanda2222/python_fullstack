

from unittest import TestCase, main
from functools import partial
from cifrado_cesar import cifrar_string, StringInputError

class TestEncription(TestCase):
    def test_basic_example(self):
        """
        Test that cifrar_string("abc",3) returns "def"
        """
        print("Testing simple example")
        cifrado = cifrar_string("abc", 3)
        self.assertEqual(cifrado, "def")

    def test_long_input(self):
        """
        test a long string to mantain format
        """
        print("Testing long string")
        input_value = "esteesunstringmuylargodeprueba"
        cifrado = cifrar_string(input_value, 34)
        print("Input: ", input_value, " returns: ", cifrado)
        self.assertEqual(len(cifrado), len(input_value))

    def test_decryption(self):
        """
        Test decryption
        """
        print("Testing decryption cases")
        input_value = "somelongstring"
        cifrado = cifrar_string(input_value, 12)
        decryption = cifrar_string(cifrado, -12)

        print("Input: ", input_value, " returns: ", cifrado, " decryption: ", decryption)
        self.assertEqual(input_value, decryption)

    def test_edge_cases(self):
        """
        Test edge cases
        """
        print("Testing space case")
        input_value = "string with space"
        self.assertRaises(
            StringInputError, 
            partial(cifrar_string, input_value, 12)
        )


if __name__ == '__main__':
    main()