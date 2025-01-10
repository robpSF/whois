import streamlit as st
import whois
from urllib.parse import urlparse
import io

st.title("WHOIS Lookup with Download")

st.write("Enter a URL to retrieve its WHOIS information and download the results as a text file.")

# Input field for the URL
url_input = st.text_input("URL", "https://www.example.com")

# Button to perform the lookup
if st.button("Lookup WHOIS Info"):
    # Extract the domain from the URL
    parsed_url = urlparse(url_input)
    domain = parsed_url.netloc or parsed_url.path  # fallback if netloc is empty

    try:
        # Perform the WHOIS lookup
        domain_info = whois.whois(domain)

        # Convert the result to a string for display
        whois_str = str(domain_info)

        # Display the WHOIS information on the page
        st.subheader(f"WHOIS Information for {domain}:")
        st.text(whois_str)

        # Create an in-memory text buffer
        with io.StringIO() as buffer:
            buffer.write(whois_str)
            # Move the cursor back to the start of the buffer
            buffer.seek(0)

            # Add a download button so the user can save the WHOIS info locally
            st.download_button(
                label="Download WHOIS Info",
                data=buffer,
                file_name=f"{domain}_whois.txt",
                mime="text/plain"
            )

    except Exception as e:
        # Handle any errors (invalid domain, network issues, etc.)
        st.error(f"Error fetching WHOIS data: {e}")
