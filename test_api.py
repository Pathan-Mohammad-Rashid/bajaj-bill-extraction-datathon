import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("\n" + "="*70)
    print("BILL EXTRACTION API - TEST")
    print("="*70)
    
    print("\n[TEST 1] Health Check")
    try:
        r = requests.get(f"{base_url}/health", timeout=5)
        print(f"✓ Status: {r.status_code}")
        print(f"✓ Response: {r.json()}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    print("\n[TEST 2] Extract Bill (with fallback)")
    try:
        payload = {"document": "test_url_will_use_fallback"}
        start = time.time()
        r = requests.post(f"{base_url}/extract-bill-data", json=payload, timeout=30)
        elapsed = time.time() - start
        
        print(f"✓ Status: {r.status_code}")
        print(f"✓ Time: {elapsed:.2f}s")
        data = r.json()
        print(f"✓ Success: {data.get('is_success')}")
        print(f"✓ Tokens: {data['token_usage']['total_tokens']}")
        print(f"✓ Items: {data['data']['total_item_count']}")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

if __name__ == "__main__":
    test_api()
    print("\n" + "="*70)
    print("✓ ALL TESTS COMPLETED")
    print("="*70 + "\n")
import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("\n" + "="*70)
    print("BILL EXTRACTION API - TEST")
    print("="*70)
    
    print("\n[TEST 1] Health Check")
    try:
        r = requests.get(f"{base_url}/health", timeout=5)
        print(f"✓ Status: {r.status_code}")
        print(f"✓ Response: {r.json()}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    print("\n[TEST 2] Extract Bill (with fallback)")
    try:
        payload = {"document": "test_url_will_use_fallback"}
        start = time.time()
        r = requests.post(f"{base_url}/extract-bill-data", json=payload, timeout=30)
        elapsed = time.time() - start
        
        print(f"✓ Status: {r.status_code}")
        print(f"✓ Time: {elapsed:.2f}s")
        data = r.json()
        print(f"✓ Success: {data.get('is_success')}")
        print(f"✓ Tokens: {data['token_usage']['total_tokens']}")
        print(f"✓ Items: {data['data']['total_item_count']}")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

if __name__ == "__main__":
    test_api()
    print("\n" + "="*70)
    print("✓ ALL TESTS COMPLETED")
    print("="*70 + "\n")
