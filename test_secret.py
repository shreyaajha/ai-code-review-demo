from scripts.secret_scanner import scan_for_secrets

sample = """

+print("Hello")
"""

results = scan_for_secrets(sample)

print(results)