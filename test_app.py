from scripts.ai_reviewer import ai_review

sample = """
+password = "admin123"

+def login():
+    print(password)
"""

result = ai_review(sample)

print(result)