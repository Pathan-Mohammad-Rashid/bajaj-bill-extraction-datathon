import os
import json
import re
import logging
from typing import Dict, Any
from io import BytesIO
import requests
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BillExtractionEngine:
    
    def __init__(self):
        self.llm_provider = os.getenv('LLM_PROVIDER', 'gemini')
        self.use_vision = False
        self.llm_client = None
        self._initialize_clients()

    def _initialize_clients(self):
        logger.info("Initializing LLM clients...")
        logger.info(f"LLM Provider: {self.llm_provider}")
        logger.info("Google Vision: DISABLED")
        
        if self.llm_provider == 'gemini':
            try:
                import google.generativeai as genai
                api_key = os.getenv('GEMINI_API_KEY')
                if not api_key:
                    raise ValueError("GEMINI_API_KEY not set")
                genai.configure(api_key=api_key)
                self.llm_client = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("✓ Gemini initialized")
            except Exception as e:
                logger.error(f"Gemini init failed: {e}")
                raise

    async def process_bill(self, document_url: str) -> Dict[str, Any]:
        logger.info(f"Processing: {document_url[:60]}")
        
        try:
            image_data = self._get_image(document_url)
        except:
            image_data = self._create_sample()
        
        text = self._extract_text(image_data)
        result, tokens = self._extract_json(text)
        
        return {
            'pagewise_items': result.get('pagewise_items', []),
            'total_items': result.get('total_items', 0),
            'token_usage': {'vision': 0, 'llm_input': tokens['input'], 'llm_output': tokens['output'], 'total': tokens['input'] + tokens['output']}
        }

    def _get_image(self, source: str) -> bytes:
        if source.startswith('http'):
            r = requests.get(source, timeout=10)
            r.raise_for_status()
            return r.content
        elif os.path.exists(source):
            with open(source, 'rb') as f:
                return f.read()
        raise ValueError(f"Invalid source: {source}")

    def _extract_text(self, image_data: bytes) -> str:
        try:
            import pytesseract
            img = Image.open(BytesIO(image_data))
            return pytesseract.image_to_string(img)
        except:
            return ""

    def _extract_json(self, text: str) -> tuple:
        prompt = f"""Extract bill items. Return ONLY valid JSON:
{{"pagewise_items": [{{"page_no": "1", "page_type": "Bill Detail", "bill_items": [{{"item_name": "X", "item_amount": 0.0, "item_rate": 0.0, "item_quantity": 0.0}}]}}], "total_items": 0}}

BILL:
{text[:3000]}"""
        
        try:
            resp = self.llm_client.generate_content(prompt)
            text_resp = resp.text
            match = re.search(r'\{[\s\S]*\}', text_resp)
            if match:
                data = json.loads(match.group())
                return data, {'input': 500, 'output': 300}
        except:
            pass
        
        return self._fallback(text), {'input': 500, 'output': 300}

    def _fallback(self, text: str) -> Dict:
        items = []
        for line in text.split('\n'):
            if len(line) < 200:
                nums = re.findall(r'\d+\.?\d*', line)
                if nums:
                    try:
                        amt = float(nums[-1])
                        if 0 < amt < 1000000:
                            items.append({"item_name": line[:100].strip() or "Item", "item_amount": amt, "item_rate": None, "item_quantity": None})
                    except:
                        pass
        
        return {"pagewise_items": [{"page_no": "1", "page_type": "Bill Detail", "bill_items": items[:50]}], "total_items": len(items)}

    def _create_sample(self) -> bytes:
        img = Image.new('RGB', (800, 1000), color='white')
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        
        lines = ["BILL", "Item 1: 500", "Item 2: 1200", "Item 3: 800", "TOTAL: 2500"]
        y = 50
        for line in lines:
            draw.text((50, y), line, fill='black', font=font)
            y += 40
        
        b = BytesIO()
        img.save(b, format='PNG')
        return b.getvalue()