import streamlit as st
import whois
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import requests

st.title("WHOIS Lookup + Custom Image (Larger Domain Font)")

# Try to load a known TTF font at a larger size
# Adjust the font path if needed (e.g., "DejaVuSans.ttf", "Arial.ttf", etc.)
RAW_TTF_URL = "https://raw.githubusercontent.com/robpSF/whois/main/DejaVuSans.ttf"  # Common on many Linux systems
LARGE_FONT_SIZE = 30  # About 3× the default ~10-12px size

response = requests.get(RAW_TTF_URL)
if response.status_code == 200:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_file:
        tmp_file.write(response.content)
        tmp_font_path = tmp_file.name

    large_title_font = ImageFont.truetype(tmp_font_path, 36)
else:
    # fallback
    large_title_font = ImageFont.load_default()

# For subtitle and button text, we'll just keep the default smaller font
subtitle_font = ImageFont.load_default()
button_font = ImageFont.load_default()

# Input field for the URL
url_input = st.text_input("URL", "https://www.example.com")

# Button to perform the lookup
if st.button("Lookup WHOIS Info"):
    # Extract the domain from the URL
    parsed_url = urlparse(url_input)
    domain = parsed_url.netloc or parsed_url.path  # fallback if netloc is empty

    try:
        # Perform WHOIS lookup
        domain_info = whois.whois(domain)
        whois_str = str(domain_info)

        # Display WHOIS information
        st.subheader(f"WHOIS Information for {domain}:")
        st.text(whois_str)

        # --------------------------------------
        # PART 1: Create the custom image
        # --------------------------------------
        bg_color = (216, 246, 250)  # Light blue background (#D8F6FA)
        img_width, img_height = 768, 96
        img = Image.new("RGB", (img_width, img_height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Write the domain in larger font
        text_x, text_y = 20, 15
        draw.text((text_x, text_y), domain, fill=(51, 51, 51), font=large_title_font)

        # Write the subtitle: "whois information" in smaller font
        subtitle_x, subtitle_y = 20, 45
        draw.text((subtitle_x, subtitle_y), "whois information", fill=(51, 51, 51), font=subtitle_font)

        # Draw a "Whois" button
        button_width, button_height = 60, 30
        button_x, button_y = 20, 65
        button_color = (51, 153, 255)  # Medium blue (#3399FF)
        draw.rectangle(
            [(button_x, button_y), (button_x + button_width, button_y + button_height)],
            fill=button_color
        )

        # Center text inside the button using textbbox
        whois_text = "Whois"
        bbox = draw.textbbox((0, 0), whois_text, font=button_font)
        w_text = bbox[2] - bbox[0]  # text width
        h_text = bbox[3] - bbox[1]  # text height

        center_x = button_x + (button_width // 2) - (w_text // 2)
        center_y = button_y + (button_height // 2) - (h_text // 2)
        draw.text((center_x, center_y), whois_text, fill="white", font=button_font)

        # --------------------------------------
        # PART 2: Display & Download the image
        # --------------------------------------
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Display the image in Streamlit
        st.image(img_buffer, caption="Custom WHOIS Image", use_container_width=False)

        # Download button for the image
        st.download_button(
            label="Download Image",
            data=img_buffer,
            file_name=f"{domain}_image.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"Error fetching WHOIS data: {e}")
