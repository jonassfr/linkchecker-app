# test_runner.py
from app_runner import run_link_checker

result = run_link_checker()

print("RUN FINISHED")
print(f"Scanned pages: {result['scanned_pages']}")
print(f"Broken links: {result['broken_links']}")
print(f"Cascade logins: {result['cascade_logins']}")
print(f"Affected pages: {result['affected_pages']}")
print(f"Page report: {result['page_report_path']}")
print(f"Violations report: {result['violations_report_path']}")
print(f"Summary report: {result['summary_report_path']}")