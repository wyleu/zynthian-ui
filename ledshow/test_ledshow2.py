import unittest

import ledshow2

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class TestGPIOSetup(unittest.TestCase):

    def test_constants_of_GPIO(self):
        board = ledshow2.Board()
        res = board.dir_constants()
        for k, v in res.items():
            self.assertEqual(v, ledshow2.gpio_constants[k])
        self.assertEqual(len(res), len(ledshow2.gpio_constants))

    def test_functions_of_GPIO(self):
        board = ledshow2.Board()
        res = board.dir_functions()
        for k in res:
            self.assertIn(k, ledshow2.gpio_functions)
        self.assertEqual(len(res),len(ledshow2.gpio_functions))



    # def test_warnings_mode(self):
    #     board = ledshow2.Board()
    #
    #
    #
    #
    # def run_test(self, warning):
    #     for mode in ledshow2.gpio_modes:
    #         board = ledshow2.Board()
    #         self.assertEqual(board.getmode(), mode)
    #         board.cleanup()



class TestLEDMethods(unittest.TestCase):

    def test_LED_lights(self):
        for item in ledshow2.ENCODER_LEDS:
            pass



if __name__ == '__main__':
    unittest.main()