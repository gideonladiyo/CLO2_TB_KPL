from fastapi import HTTPException

VALIDATION_RULES = {
    "price": lambda v: v >= 0,
    "stock": lambda v: v >= 0
}

def validate_item(item):
    for attr, rule in VALIDATION_RULES.items():
        if not rule(getattr(item, attr)):
            raise HTTPException(
                status_code=422, detail=f"{attr.capitalize()} tidak boleh negatif"
            )
