def is_expr(expression: str) -> bool:
    can_expr = ['+', '-', '/', '*', '%', '**', ' ', '(', ')']
    for i in can_expr:
        expression = expression.replace(i, '')
    if not expression.isdigit():
        return False
    return True
