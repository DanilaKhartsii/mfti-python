
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date, datetime
from typing import List, Literal
import json
import re
from pathlib import Path

app = FastAPI(title="Customer Appeal Service")

DATA_PATH = Path("appeals.json")


class Appeal(BaseModel):
    last_name: str = Field(..., description="Фамилия", example="Иванов")
    first_name: str = Field(..., description="Имя", example="Пётр")
    birth_date: date = Field(..., description="Дата рождения", example="1990-05-14")
    phone: str = Field(..., description="Номер телефона", example="+79991234567")
    email: EmailStr = Field(..., description="E-mail", example="user@example.com")
    reasons: List[Literal["нет доступа к сети", "не работает телефон", "не приходят письма"]] | None = Field(default=None, description="Причина обращения", example=["не работает телефон"])
    detected_at: datetime | None = Field(default=None, description="Дата и время обнаружения проблемы", example="2025-11-12T15:45:00",)

    @validator("last_name", "first_name")
    def validate_cyrillic(cls, value):
        if not re.match(r"^[А-ЯЁ][а-яё]+$", value):
            raise ValueError("Поле должно содержать только кириллицу и начинаться с заглавной буквы")
        return value

    @validator("phone")
    def validate_phone(cls, value):
        if not re.match(r"^\+7\d{10}$", value):
            raise ValueError("Телефон должен быть в формате +7XXXXXXXXXX (11 цифр)")
        return value


@app.post("/appeal")
def create_appeal(appeal: Appeal):
    try:
        if DATA_PATH.exists():
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        data.append(appeal.dict())

        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return {"message": "Обращение сохранено", "total": len(data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/appeals")
def get_all_appeals():
    if not DATA_PATH.exists():
        return {"message": "Пока нет обращений", "appeals": []}

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {"total": len(data), "appeals": data}


@app.get("/")
def root():
    return {"message": "Customer Appeals API", "docs": "/docs"}
