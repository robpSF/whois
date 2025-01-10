import streamlit as st
import whois
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.title("WHOIS Lookup + Custom Image")

url_input = st.text_input("URL", "https://www.example.com")

if st.button("Lookup WHOIS Info"):
    parsed_url = urlparse(url_input)
    domain = parsed_url.netloc or parsed_url.path

    try:
        # WHOIS
        domain_info = whois.whois(domain)
        whois_str = str(domain_info)

        st.subheader(f"WHOIS Information for {domain}:")
        st.text(whois_str)

        # Create image
        bg_color = (216, 246, 250)  # Light blue
        img_width, img_height = 768, 96
        img = Image.new("RGB", (img_width, img_height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Load fonts (using built-in for demo)
        title_font = ImageFont.load_default()  
        subtitle_font = ImageFont.load_default()
        button_font = ImageFont.load_default()

        # Positioning
        text_x, text_y = 20, 20
        subtitle_x, subtitle_y = 20, 45
        button_width, button_height = 60, 30
        button_x, button_y = 20, 65
        button_color = (51, 153, 255)

        # Write domain
        draw.text((text_x, text_y), domain, fill=(51, 51, 51), font=title_font)

        # Write subtitle
        draw.text((subtitle_x, subtitle_y), "whois information", fill=(51, 51, 51), font=subtitle_font)

        # Draw button
        draw.rectangle(
            [(button_x, button_y), (button_x + button_width, button_y + button_height)],
            fill=button_color
        )

        # Center the button text
        whois_text = "Whois"
        w_text, h_text = title_font.getsize(whois_text)  # measure text size
        center_x = button_x + (button_width // 2) - (w_text // 2)
        center_y = button_y + (button_height // 2) - (h_text // 2)
        draw.text((center_x, center_y), whois_text, fill="white", font=button_font)

        # Convert image to BytesIO
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Show image in Streamlit
        st.image(img_buffer, caption="Custom WHOIS Image")

        # Download button
        st.download_button(
            label="Download Image",
            data=img_buffer,
            file_name=f"{domain}_image.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"Error fetching WHOIS data: {e}")
