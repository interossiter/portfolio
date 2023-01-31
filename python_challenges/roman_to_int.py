import unittest
import roman
class RomanNumeral:

    def roman_to_int(self, s):

# This function takes in a string s representing a Roman numeral.
# It first creates a dictionary that maps each Roman numeral character to its corresponding integer value. Then, it initializes a variable result to store the integer value of the Roman numeral.
# The function then iterates through the characters in the string.
# If the current character has a higher value than the previous character,
# the function subtracts twice the value of the previous character from
# the result (to account for the previous character being added in the previous iteration).
# Otherwise, it simply adds the value of the current character to the result.
# Finally, the function returns the integer value of the Roman numeral.

        roman_dict = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
        result = 0
        for i in range(len(s)):
            if i > 0 and roman_dict[s[i]] > roman_dict[s[i - 1]]:
                result += roman_dict[s[i]] - 2 * roman_dict[s[i - 1]]
            else:
                result += roman_dict[s[i]]
        return result

    def int_to_roman(self, num):
        values = [ 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1 ]
        symbols = [ "M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I" ]
        roman = ""
        for i, val in enumerate(values):
            while num >= val:
                num -= val
                roman += symbols[i]
        return roman


    def calcDaysBetweenDates(self, year1, month1, day1, year2, month2, day2):
        daysInMonth = [31,28,31,30,31,30,31,31,30,31,30,31]
        days = 0
        if year1 == year2:
            if month1 == month2:
                days = day2 - day1
            else:
                for i in range(month1, month2):
                    days += daysInMonth[i-1]
                days += day2 - day1
        else:
            for i in range(month1, 13):
                days += daysInMonth[i-1]
            days += day2 - day1
            for i in range(year1+1, year2):
                if i % 4 == 0:
                    days += 366
                else:
                    days += 365
            for i in range(1, month2):
                days += daysInMonth[i-1]
        return days



class Test(unittest.TestCase):
    def test_romanToInt(self):
        # https://leetcode.com/problems/roman-to-integer/description/

        s = 'VI'
        # nReturn = Solution.romanToInt(self, s)
        nReturn = RomanNumeral.roman_to_int(self, s)

        print ('nReturn = ' + str(nReturn))

        self.assertEqual(nReturn, roman.fromRoman(s))

if __name__ == '__main__':
    unittest.main()