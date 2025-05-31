import streamlit as st
from agents.puppet_creator import generate_sock_puppet
import base64

st.set_page_config(page_title="Sock Puppet Generator", layout="centered")

st.title("Sock Puppet Generator")

if st.button("Generate Sock Puppet"):
    with st.spinner("Generating sock puppet..."):
        puppet = generate_sock_puppet()
        if puppet:
            st.success("Sock puppet generated!")
            st.markdown(f"**Name:** {puppet['name']}")
            st.markdown(f"**Date of Birth:** {puppet['dob']}")
            st.markdown(f"**Location:** {puppet['location']}")
            st.markdown(f"**Email:** {puppet['email']}")
            st.markdown(f"**Interests:** {', '.join(puppet['interests'])}")
            st.markdown(f"**Bio:** {puppet['bio']}")

            # Show image if available
            if puppet.get("photo"):
                image_bytes = puppet['photo'].getvalue()
                encoded = base64.b64encode(image_bytes).decode()
                st.image(f"data:image/jpeg;base64,{encoded}", caption="Sock Puppet Face", use_column_width=True)
        else:
            st.error("Failed to generate a sock puppet. Please check your configuration and try again.")
