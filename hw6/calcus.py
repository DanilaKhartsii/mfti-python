from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import ast

app = FastAPI(title="Версионированный АПИ калькулятор")

class Operation(BaseModel):
    a: float
    b: float
    op: str

class Expression(BaseModel):
    expression: str

def save_eval(expression: str) -> float:
    allowed_nodes = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
        ast.Mod, ast.FloorDiv,
        ast.USub, ast.UAdd,
        ast.Constant,
        ast.Load
    }

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)

            if type(node.op) == ast.Add:
                return left + right
            elif type(node.op) == ast.Sub:
                return left - right
            elif type(node.op) == ast.Mult:
                return left * right
            elif type(node.op) == ast.Div:
                return left / right
            elif type(node.op) == ast.Mod:
                return left % right
            elif type(node.op) == ast.FloorDiv:
                return left // right
            elif type(node.op) == ast.Pow:
                return left ** right
            else:
                raise ValueError(f"Неподдерживаемый оператор: {type(node.op).__name__}")

        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)

            if type(node.op) == ast.UAdd:
                return +operand
            elif type(node.op) == ast.USub:
                return -operand
            else:
                raise ValueError(f"Неподдерживаемый оператор: {type(node.op).__name__}")

        elif isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Ошибочный тип константы: {type(node.value).__name__}")

        else:
            raise ValueError(f"Ошибочный или неподдерживаемый элемент выражения: {type(node).__name__}")

    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Ошибка синтаксиса в выражении: {e}")

    for node in ast.walk(parsed):
        if type(node) not in allowed_nodes:
            raise ValueError(f"Недопустимый элемент в выражении: {type(node).__name__}")

    return _eval(parsed)

# ----- Версия 1 -----

router_v1 = APIRouter(prefix="/v1", tags=["v1 calc"])
current_expression_v1 = ""

@router_v1.post("/add")
def add_v1(op: Operation):
    return {"result": op.a + op.b}

@router_v1.post("/expression/set")
def set_expr_v1(expr: Expression):
    global current_expression_v1
    current_expression_v1 = expr.expression
    return {"expression": current_expression_v1}

@router_v1.post("/expression/evaluate")
def eval_expr_v1():
    if not current_expression_v1:
        raise HTTPException(status_code=400, detail="No expression set")
    return {"result": save_eval(current_expression_v1)}

# ----- Версия 2 -----

router_v2 = APIRouter(prefix="/v2", tags=["v2 calc"])
expression_history_v2 = []

@router_v2.post("/calculate")
def calculate_v2(expr: Expression):
    try:
        result = save_eval(expr.expression)
        expression_history_v2.append({"expr": expr.expression, "result": result})
        return {"expression": expr.expression, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_v2.post("/history")
def get_history_v2():
    return {"history": expression_history_v2}

app.include_router(router_v1)
app.include_router(router_v2)

@app.get("/")
def root():
    return {
        "msg": "Добро пожаловать в версионированный АПИ калькулятор",
        "versions": ["/v1", "/v2"],
        "docs": "/docs"
    }