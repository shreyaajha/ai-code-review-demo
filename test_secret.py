from scripts.secret_scanner import scan_for_secrets

sample = """
+password="admin123"

+OPENAI_API_KEY="sk-123456789012345678901234567890"

+print("Hello")
"""

results = scan_for_secrets(sample)

print(results)