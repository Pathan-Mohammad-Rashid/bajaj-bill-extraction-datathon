from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class BillItem(BaseModel):
    item_name: str
    item_amount: float
    item_rate: Optional[float] = None
    item_quantity: Optional[float] = None

class PagewiseBillItem(BaseModel):
    page_no: str
    page_type: str
    bill_items: List[BillItem]

class TokenUsage(BaseModel):
    total_tokens: int
    input_tokens: int
    output_tokens: int

class BillExtractionRequest(BaseModel):
    document: str

class BillExtractionResponse(BaseModel):
    is_success: bool
    token_usage: TokenUsage
    data: Dict[str, Any]
