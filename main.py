import os
import sys
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.schemas import BillExtractionRequest, BillExtractionResponse, TokenUsage
from models.extraction_engine import BillExtractionEngine

app = FastAPI(title="Bill Extraction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = BillExtractionEngine()

@app.get("/")
def root():
    return {"message": "Bill Extraction API v1.0", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "bill-extraction-api"}

@app.post("/extract-bill-data")
async def extract_bill_data(request: BillExtractionRequest):
    try:
        result = await engine.process_bill(request.document)
        
        return {
            "is_success": True,
            "token_usage": {
                "total_tokens": result['token_usage']['total'],
                "input_tokens": result['token_usage']['llm_input'],
                "output_tokens": result['token_usage']['llm_output']
            },
            "data": {
                "pagewise_line_items": result['pagewise_items'],
                "total_item_count": result['total_items']
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)










# import os
# import sys
# from dotenv import load_dotenv

# load_dotenv()

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from models.schemas import BillExtractionRequest, BillExtractionResponse, TokenUsage
# from models.extraction_engine import BillExtractionEngine

# app = FastAPI(title="Bill Extraction API", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# engine = BillExtractionEngine()

# @app.get("/")
# def root():
#     return {"message": "Bill Extraction API v1.0", "status": "running"}

# @app.get("/health")
# def health():
#     return {"status": "healthy", "service": "bill-extraction-api"}

# @app.post("/extract-bill-data", response_model=BillExtractionResponse)
# async def extract_bill_data(request: BillExtractionRequest):
#     try:
#         result = engine.process_bill(request.document)
#         token_usage = result.get('token_usage', {})
#         return BillExtractionResponse(
#             is_success=True,
#             token_usage=TokenUsage(
#                 total_tokens=token_usage.get('total', 0),
#                 input_tokens=token_usage.get('llm_input', 0),
#                 output_tokens=token_usage.get('llm_output', 0)
#             ),
#             data={
#                 'pagewise_line_items': result.get('pagewise_items', []),
#                 'total_item_count': result.get('total_items', 0)
#             }
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
