import streamlit as st
import whois
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.title("WHOIS Lookup + Custom Image")

st.write("Enter a URL to retrieve WHOIS information, generate a custom image, and download it.")

# Input field for the URL
url_input = st.text_input("URL", "https://www.example.com")

# Button to perform the lookup
if st.button("Lookup WHOIS Info"):
    # Extract the domain from the URL
    parsed_url = urlparse(url_input)
    domain = parsed_url.netloc or parsed_url.path  # fallback if netloc is empty

    # WHOIS Lookup
    try:
        domain_info = whois.whois(domain)
        whois_str = str(domain_info)

        # Display WHOIS on screen
        st.subheader(f"WHOIS Information for {domain}:")
        st.text(whois_str)

        # -------------------------------
        # PART 1: Create the custom image
        # -------------------------------
        # 1. Create a blank image with the desired background color
        #    (width=768, height=96 to match your example)
        bg_color = (216, 246, 250)  # a light blue (#D8F6FA)
        img_width, img_height = 768, 96
        img = Image.new("RGB", (img_width, img_height), color=bg_color)

        # 2. Get a drawing context
        draw = ImageDraw.Draw(img)

        # 3. Define fonts (you may need to specify a path if default isn't good enough)
        #    For demonstration, we use a built-in PIL font.
        #    On some systems, you can install fonts and specify TTF paths.
        title_font = ImageFont.load_default()       # For "domain" text
        subtitle_font = ImageFont.load_default()    # For "whois information"
        button_font = ImageFont.load_default()      # For "Whois" button

        # 4. Write domain text (e.g., "dass.com" -> user domain)
        #    Let's place it near the left edge with some margin
        text_x = 20
        text_y = 20
        draw.text((text_x, text_y), domain, fill=(51, 51, 51), font=title_font)

        # 5. Write "whois information" under it
        subtitle_x = 20
        subtitle_y = 45  # a bit lower
        draw.text((subtitle_x, subtitle_y), "whois information", fill=(51, 51, 51), font=subtitle_font)

        # 6. Draw a "Whois" button on the left side
        #    For simplicity, we'll draw a rectangle + text
        button_width, button_height = 60, 30
        button_x = 20
        button_y = 65  # position below the text
        button_color = (51, 153, 255)  # A medium-blue (#3399FF)
        draw.rectangle([  # top-left, bottom-right
            (button_x, button_y),
            (button_x + button_width, button_y + button_height)
        ], fill=button_color)

        # Write "Whois" text inside the rectangle
        # We'll center it horizontally and vertically in that rectangle
        whois_text = "Whois"
        wt_x = button_x + (button_width // 2)
        wt_y = button_y + (button_height // 2)
        # To center the text exactly, measure it:
        w_text, h_text = draw.textsize(whois_text, font=button_font)
        draw.text(
            (wt_x - w_text / 2, wt_y - h_text / 2),
            whois_text,
            fill="white",
            font=button_font
        )

        # ------------------------------------------
        # PART 2: Display & Download the custom image
        # ------------------------------------------
        # Convert the image to a BytesIO for Streamlit
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Display the image in Streamlit
        st.image(img_buffer, caption="Custom WHOIS Image", use_column_width=False)

        # Download button for the image
        st.download_button(
            label="Download Image",
            data=img_buffer,
            file_name=f"{domain}_image.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"Error fetching WHOIS data: {e}")
