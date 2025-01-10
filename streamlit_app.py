import streamlit as st
import whois
from urllib.parse import urlparse

st.title("WHOIS Lookup")

st.write("Enter a URL to retrieve its WHOIS information.")

# User input
url_input = st.text_input("URL", "https://www.example.com")

# Button to perform lookup
if st.button("Lookup WHOIS Info"):
    # Parse the URL
    parsed_url = urlparse(url_input)
    domain = parsed_url.netloc or parsed_url.path  # fallback if netloc is empty
    
    try:
        # Perform WHOIS lookup
        domain_info = whois.whois(domain)
        # Display the results
        st.subheader(f"WHOIS Information for {domain}:")
        st.write(domain_info)
    except Exception as e:
        # Handle errors (e.g., invalid domain)
        st.error(f"Error fetching WHOIS data: {e}")
