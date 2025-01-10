import streamlit as st
import whois
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import requests
import tempfile

st.title("WHOIS Lookup + Custom Image")

# Try to load a known TTF font at a larger size
# Adjust the font path if needed (e.g., "DejaVuSans.ttf", "Arial.ttf", etc.)
RAW_TTF_URL = "https://raw.githubusercontent.com/robpSF/whois/main/DejaVuSans.ttf"  # Common on many Linux systems
LARGE_FONT_SIZE = 30

response = requests.get(RAW_TTF_URL)
if response.status_code == 200:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_file:
        tmp_file.write(response.content)
        tmp_font_path = tmp_file.name

    large_title_font = ImageFont.truetype(tmp_font_path, LARGE_FONT_SIZE )
else:
    # fallback
    large_title_font = ImageFont.load_default()

# For subtitle and button text, we'll just keep the default smaller font
subtitle_font = ImageFont.load_default()
button_font = ImageFont.load_default()

# Input field for the URL
#url_input = st.text_input("URL", "https://bbc.co.uk")
url_input = st.text_input("Real URL (used for WHOIS lookup)", "https://bbc.co.uk")
fictional_url_input = st.text_input("Fictional URL (displayed on the image)", "fictional.example.com")


# Button to perform the lookup
if st.button("Lookup WHOIS Info"):
    # Extract the domain from the URL
    parsed_url = urlparse(url_input)
    domain = parsed_url.netloc or parsed_url.path  # fallback if netloc is empty

    try:
        # Perform WHOIS lookup
        domain_info = whois.whois(domain)
        
        # Instead of printing the raw dict with JSON-like symbols, 
        # create a plain-text version (key: value).
        if isinstance(domain_info, dict):
            lines = []
            for key, value in domain_info.items():
                lines.append(f"{key}: {value}")
            plain_text_output = "\n".join(lines)
        else:
            # Some WHOIS lookups might return a list or string. Handle gracefully.
            plain_text_output = str(domain_info)

        st.subheader(f"WHOIS Information for {domain}:")
        # Instead of st.text(whois_str), use plain_text_output without JSON symbols.
        st.text(plain_text_output)
        
        # --------------------------------------
        # PART 1: Create the custom image
        # --------------------------------------
        bg_color = (216, 246, 250)  # Light blue background (#D8F6FA)
        img_width, img_height = 768, 96
        img = Image.new("RGB", (img_width, img_height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Write the domain in larger font
        text_x, text_y = 20, 10
        draw.text((text_x, text_y), fictional_url_input, fill=(51, 51, 51), font=large_title_font)

        # Write the subtitle: "whois information" in smaller font
        subtitle_x, subtitle_y = 20, 45
        draw.text((subtitle_x, subtitle_y), "whois information", fill=(51, 51, 51), font=subtitle_font)

        # Draw a "Whois" button
        button_width, button_height = 70, 30
        button_x, button_y = 20, 60
        button_color = (51, 153, 255)  # Medium blue (#3399FF)
        corner_radius = 6  # set how rounded you want the corners
        # 2) Use draw.rounded_rectangle (introduced in Pillow 8.2.0)
        draw.rounded_rectangle(
            [(button_x, button_y), (button_x + button_width, button_y + button_height)],
            radius=corner_radius,
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
