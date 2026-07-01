from scripts.quality_checker import check_code_quality

sample = """
+print("Debug")

+# TODO: Remove this later

+breakpoint()

+console.log("Hello")
"""

results = check_code_quality(sample)

for issue in results:
    print(issue)