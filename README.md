README: Running Tests and Generating Reports in Multiple Formats

This automation suite includes test cases for the /login endpoint and supports multiple report formats (XML, HTML, and CSV) for easier test result analysis.
Requirements

    Python 3.x
    requests, pytest, pytest-html, pytest-csv libraries:

    pip install requests pytest pytest-html pytest-csv

File Structure

    test_login_api.py: Main script with test cases for the /login endpoint.

Running the Tests and Generating Reports

To execute the tests and generate reports in different formats, use the following commands:

    XML Report:

pytest test_login_api.py --junitxml=test_results.xml -v

HTML Report:

pytest test_login_api.py --html=test_results.html -v

CSV Report:

    pytest test_login_api.py --csv=test_results.csv -v

These commands will generate test_results.xml, test_results.html, or test_results.csv in the current directory, depending on the chosen format.
Viewing the Reports

    XML Report: Open test_results.xml in any text editor or view it in CI/CD tools that support JUnit reports.
    HTML Report: Open test_results.html in a web browser to view a formatted report of each test case.
    CSV Report: Open test_results.csv in spreadsheet software (e.g., Excel or Google Sheets) to analyze test results.

Customization

To add or modify test cases, update the test_data in test_login_api.py. Rerun the commands to regenerate reports with updated results.