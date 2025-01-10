import streamlit as st
import whois
from urllib.parse import urlparse

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

        # Provide a download button for the WHOIS string
        st.download_button(
            label="Download WHOIS Info",
            data=whois_str,               # ← Directly pass the WHOIS string
            file_name=f"{domain}_whois.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"Error fetching WHOIS data: {e}")
