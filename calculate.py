import re


class expressionCalculator:
    def xor(self, a, b):
        return bool((a and not b) or (b and not a))

    def stringToNumber(self, numberMatch: re.Match[str], expression: str):
        if numberMatch.group(2):
            return float(expression)
        return int(expression)

    def parseParentheses(self, expression: str):
        ifLeftParentheses = expression[0] == "("
        ifRightParentheses = expression[-1] == ")"
        singleParentheses = self.xor("(" in expression, ")" in expression)
        if singleParentheses:
            raise SyntaxError(f"Unexpected parentheses -> {expression}")
        if ifLeftParentheses and ifRightParentheses:
            return self.parseExpression(expression[1:-1])
        return None

    def parsePowerOf(self, expression: str):
        match = re.match(r"\s*(.+?)(\*\*)(.+)", expression)
        if match:
            left = self.parseExpression(match.group(1))
            right = self.parseExpression(match.group(3))
            return left**right
        return None

    def parseMultiplicationDivisoinRemainder(self, expression: str):
        match = re.match(r"\s*(.+?)(\*|\/\/|\/|%)(.+)", expression)
        ifmultiplication = match and match.group(2) == "*"
        ifdivision = match and match.group(2) == "/"
        ifremainder = match and match.group(2) == "%"
        ifdivisor = match and match.group(2) == "//"
        if match and ifmultiplication:
            left = self.parseExpression(match.group(1))
            right = self.parseExpression(match.group(3))
            return left * right
        if match and ifdivision:
            left = self.parseExpression(match.group(1))
            right = self.parseExpression(match.group(3))
            return left / right
        if match and ifremainder:
            left = self.parseExpression(match.group(1))
            right = self.parseExpression(match.group(3))
            return left % right
        if match and ifdivisor:
            left = self.parseExpression(match.group(1))
            right = self.parseExpression(match.group(3))
            return left / right
        return None

    def parseAdditionAndSubtraction(self, expression: str):
        match = re.match(r"\s*(.*?)(\+|\-)(.+)", expression)
        isAddition = match and match.group(2) == "+" and match.group(1) and match.group(2)
        isSubtraction = match and match.group(2) == "-" and match.group(1) and match.group(2)
        isPositive = match and match.group(2) == "+" and (not match.group(1)) and match.group(2)
        isNegative = match and match.group(2) == "-" and (not match.group(1)) and match.group(2)
        if match and isAddition:
            left = self.parseExpression(match.group(1))
            right = self.parseExpression(match.group(3))
            return left + right

        if match and isSubtraction:
            left = self.parseExpression(match.group(1))
            right = self.parseExpression(match.group(3))
            return left - right

        if match and isPositive:
            return self.parseExpression(match.group(3))
        if match and isNegative:
            return -1 * self.parseExpression(match.group(3))
        return None

    def parseNumber(self, expression: str):
        match = re.match(r"\s*(\d+)(\.\d+)?\s*$", expression)
        """
        12355.1234
        numberMatch.group(1):Interger part -> 12355
        numberMatch.group(2):Float Part -> .1234
        """
        if match:
            return self.stringToNumber(match, expression)
        else:
            raise SyntaxError(f'Unexpected number -> "{expression}"')

    def parseExpression(self, expression: str):
        stack = [
            self.parseParentheses,
            self.parsePowerOf,
            self.parseMultiplicationDivisoinRemainder,
            self.parseAdditionAndSubtraction,
        ]
        for func in stack:
            if (result := func(expression)) is not None:
                return result
        return self.parseNumber(expression)

    def __init__(self, expression: str):
        self.result = self.parseExpression(expression)
