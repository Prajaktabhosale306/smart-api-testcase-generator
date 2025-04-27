import streamlit as st
import json
from app.swagger_loader import SwaggerLoader
from app.test_generator import TestGenerator

def save_test_cases_to_csv(test_cases):
    import csv
    keys = test_cases[0].keys()
    with open("test_cases.csv", "w", newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(test_cases)

# Main Streamlit Application
def main():
    st.title("Swagger-based Test Case Generator")

    url = st.text_input("Enter Swagger URL")

    if st.button("Generate Test Cases") and url:
        try:
            # Load Swagger data from the URL
            swagger_loader = SwaggerLoader(url)
            # Instantiate the TestGenerator class
            test_generator = TestGenerator(swagger_loader)

            # Generate test cases based on the Swagger data and user's choice
            test_cases = test_generator.generate_tests()

            # Show success message and number of test cases generated
            st.success(f"{len(test_cases)} test cases generated!")

            # Display the generated test cases as JSON
            st.json(test_cases)

            # Option to download the test cases as JSON
            st.download_button("Download JSON", json.dumps(test_cases, indent=2), "test_cases.json", "application/json")

            # Option to save the test cases as CSV
            save_as_csv = st.checkbox("Save as CSV")
            if save_as_csv:
                save_test_cases_to_csv(test_cases)
                st.success("Test cases saved as CSV!")

        except requests.exceptions.RequestException as e:
            st.error(f"Error loading Swagger data: {e}")
        except ValueError as e:
            st.error(f"Error: {e}")  # This will handle errors like missing 'paths' or malformed data
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
