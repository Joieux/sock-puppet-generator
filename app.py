import streamlit as st
import base64
import json
from io import BytesIO

# Try to import the functions, with error handling
try:
    from agents.puppet_creator import generate_sock_puppet, save_puppet_to_file
except ImportError as e:
    st.error(f"Error importing puppet creator: {e}")
    st.stop()

def main():
    st.set_page_config(
        page_title="Sock Puppet Generator",
        page_icon="🎭",
        layout="wide"
    )
    
    st.title("🎭 Sock Puppet Generator")
    st.markdown("Generate realistic sock puppet identities for authorized OSINT investigations")
    
    st.warning("⚠️ For ethical and authorized use only (e.g., security research, threat intelligence)")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Generation options
        st.subheader("Generation Options")
        use_ai_image = st.checkbox("Generate AI Face Image", value=True)
        use_detailed_bio = st.checkbox("Generate Detailed Bio", value=True)
        
        # Domain selection for email
        email_domain = st.selectbox(
            "Email Domain",
            ["tempmail.org", "guerrillamail.com", "10minutemail.com", "mailinator.com"]
        )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Generate New Identity")
        
        if st.button("🎲 Generate Sock Puppet", type="primary"):
            with st.spinner("Generating sock puppet identity..."):
                try:
                    # Generate the sock puppet
                    puppet_data = generate_sock_puppet()
                    
                    if puppet_data:
                        # Store in session state
                        st.session_state.current_puppet = puppet_data
                        st.success("✅ Sock puppet generated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to generate sock puppet")
                        
                except Exception as e:
                    st.error(f"Error generating sock puppet: {str(e)}")
    
    with col2:
        st.header("Export Options")
        
        # Only show export options if we have a puppet
        if 'current_puppet' in st.session_state:
            puppet = st.session_state.current_puppet
            
            if st.button("📄 Export as JSON"):
                try:
                    # Create JSON data (excluding non-serializable items)
                    export_data = {k: v for k, v in puppet.items() if k != 'profile_image'}
                    json_str = json.dumps(export_data, indent=2)
                    
                    st.download_button(
                        label="💾 Download JSON",
                        data=json_str,
                        file_name=f"{puppet.get('username', 'puppet')}_data.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"Error creating JSON export: {str(e)}")
        else:
            st.info("Generate a sock puppet first to see export options")
    
    # Display current puppet if available
    if 'current_puppet' in st.session_state:
        puppet = st.session_state.current_puppet
        
        st.header("Generated Identity")
        
        # Create columns for display
        display_col1, display_col2, display_col3 = st.columns([1, 1, 1])
        
        with display_col1:
            st.subheader("Personal Information")
            st.write(f"**Name:** {puppet.get('name', 'N/A')}")
            st.write(f"**Username:** {puppet.get('username', 'N/A')}")
            st.write(f"**Email:** {puppet.get('email', 'N/A')}")
            st.write(f"**Phone:** {puppet.get('phone', 'N/A')}")
            st.write(f"**Age:** {puppet.get('age', 'N/A')}")
            st.write(f"**Gender:** {puppet.get('gender', 'N/A')}")
        
        with display_col2:
            st.subheader("Location & Background")
            st.write(f"**Address:** {puppet.get('address', 'N/A')}")
            st.write(f"**City:** {puppet.get('city', 'N/A')}")
            st.write(f"**State:** {puppet.get('state', 'N/A')}")
            st.write(f"**ZIP:** {puppet.get('zip_code', 'N/A')}")
            st.write(f"**Country:** {puppet.get('country', 'N/A')}")
            st.write(f"**Occupation:** {puppet.get('occupation', 'N/A')}")
        
        with display_col3:
            st.subheader("Profile Image")
            if puppet.get('profile_image'):
                try:
                    # Display the image if available
                    st.image(puppet['profile_image'], caption="Generated Profile Image", width=200)
                except Exception as e:
                    st.write("Profile image not available")
            else:
                st.write("No profile image generated")
        
        # Bio section
        if puppet.get('bio'):
            st.subheader("Biography")
            st.write(puppet['bio'])
        
        # Technical details
        with st.expander("Technical Details"):
            st.json({
                "Email Alias Info": puppet.get('email_alias', {}),
                "Generation Timestamp": puppet.get('created_timestamp', 'N/A'),
                "Mail Utils Available": puppet.get('mail_utils_available', False)
            })
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p><small>This tool is for authorized security research and OSINT investigations only.</small></p>
        <p><small>Never use for impersonation, fraud, or violations of Terms of Service.</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
