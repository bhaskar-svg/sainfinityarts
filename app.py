import streamlit as st
import os
import pandas as pd
from datetime import datetime
import base64
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="SA Infinity Arts",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define paths for storing data
DATA_DIR = "data"
IMAGES_DIR = os.path.join(DATA_DIR, "images")
VIDEOS_DIR = os.path.join(DATA_DIR, "videos")
LEADS_FILE = os.path.join(DATA_DIR, "customer_leads.csv")
ASSETS_DIR = "assets"
FEATURED_IMAGE = os.path.join(ASSETS_DIR, "featured.jpg")

# Create directories if they don't exist
for directory in [DATA_DIR, IMAGES_DIR, VIDEOS_DIR, ASSETS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create leads CSV if it doesn't exist
if not os.path.exists(LEADS_FILE):
    pd.DataFrame(columns=["Name", "Mobile", "Email", "Place", "Date"]).to_csv(LEADS_FILE, index=False)

# Custom CSS
def local_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 1rem;
            font-family: 'Georgia', serif;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #4B5563;
            text-align: center;
            margin-bottom: 2rem;
            font-family: 'Georgia', serif;
        }
        .section-header {
            font-size: 2rem;
            color: #1E3A8A;
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-family: 'Georgia', serif;
        }
        .card {
            padding: 1.5rem;
            border-radius: 0.5rem;
            background-color: #F3F4F6;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            background-color: #F3F4F6;
            border-radius: 0.5rem;
        }
        .gallery-image {
            margin: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .form-container {
            background-color: #F9FAFB;
            padding: 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def get_image_b64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def save_uploaded_file(uploaded_file, directory):
    # Create a safe filename
    filename = uploaded_file.name
    filepath = os.path.join(directory, filename)
    
    # Save the file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return filepath

def admin_page():
    st.markdown('<h2 class="section-header">Admin Dashboard</h2>', unsafe_allow_html=True)
    
    # Admin Authentication
    admin_password = st.sidebar.text_input("Admin Password", type="password")
    if admin_password != "admin123":  # Simple password for demonstration
        st.warning("Please enter the admin password to access this page.")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["Upload Content", "Featured Image", "View Leads", "Website Settings"])
    
    with tab1:
        st.markdown('<h3 class="sub-header">Upload New Content</h3>', unsafe_allow_html=True)
        
        upload_type = st.radio("Select content type:", ["Image", "Video"])
        
        if upload_type == "Image":
            uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    file_path = save_uploaded_file(uploaded_file, IMAGES_DIR)
                    st.success(f"Saved {uploaded_file.name} successfully!")
                    # Display the uploaded image
                    image = Image.open(file_path)
                    st.image(image, caption=uploaded_file.name, width=300)
        
        else:  # Video
            uploaded_files = st.file_uploader("Upload Videos", type=["mp4", "mov", "avi"], accept_multiple_files=True)
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    file_path = save_uploaded_file(uploaded_file, VIDEOS_DIR)
                    st.success(f"Saved {uploaded_file.name} successfully!")
                    # Display the uploaded video
                    st.video(file_path)
    
    with tab2:
        st.markdown('<h3 class="sub-header">Upload Featured Image</h3>', unsafe_allow_html=True)
        
        st.info("This image will be displayed prominently on the home page")
        
        uploaded_file = st.file_uploader("Upload Featured Image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            # Save the featured image
            with open(FEATURED_IMAGE, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("Featured image uploaded successfully!")
            
            # Display the uploaded image
            image = Image.open(FEATURED_IMAGE)
            st.image(image, caption="New Featured Image", width=400)
    
    with tab3:
        st.markdown('<h3 class="sub-header">Customer Leads</h3>', unsafe_allow_html=True)
        
        # Load and display leads
        if os.path.exists(LEADS_FILE):
            leads_df = pd.read_csv(LEADS_FILE)
            if not leads_df.empty:
                st.dataframe(leads_df)
                
                # Export option
                csv = leads_df.to_csv(index=False)
                st.download_button(
                    label="Download Leads as CSV",
                    data=csv,
                    file_name="sa_infinity_arts_leads.csv",
                    mime="text/csv",
                )
            else:
                st.info("No customer leads yet.")
        else:
            st.info("No customer leads yet.")
    
    with tab4:
        st.markdown('<h3 class="sub-header">Website Settings</h3>', unsafe_allow_html=True)
        st.info("This feature will be available in future updates.")

def home_page():
    # Header
    st.markdown('<h1 class="main-header">SA Infinity Arts</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Unleashing Creativity, Inspiring Imagination</p>', unsafe_allow_html=True)
    
    # Featured Image
    if os.path.exists(FEATURED_IMAGE):
        st.image(FEATURED_IMAGE, use_column_width=True)
    else:
        st.info("No featured image found. Please upload one via the Admin > Featured Image panel.")
    
    # About Section
    st.markdown('<h2 class="section-header">About Us</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <p>SA Infinity Arts is dedicated to promoting and nurturing artistic talent across various mediums. 
        We believe in the power of art to transform lives and communities. Our mission is to provide a platform 
        for artists to showcase their work and connect with art enthusiasts.</p>
        
        <p>Founded in 2022, we have quickly established ourselves as a hub for creative expression and artistic growth.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Services
    st.markdown('<h2 class="section-header">Our Services</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Art Classes</h3>
            <p>Learn various art forms from experienced instructors.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Exhibitions</h3>
            <p>Regular showcases of artwork from talented artists.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>Custom Artwork</h3>
            <p>Commission unique pieces tailored to your vision.</p>
        </div>
        """, unsafe_allow_html=True)

def gallery_page():
    st.markdown('<h2 class="section-header">Our Gallery</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Images", "Videos"])
    
    with tab1:
        if os.path.exists(IMAGES_DIR):
            image_files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            if image_files:
                # Display images in a grid
                cols = st.columns(3)
                for i, image_file in enumerate(image_files):
                    image_path = os.path.join(IMAGES_DIR, image_file)
                    with cols[i % 3]:
                        st.image(image_path, caption=image_file, use_column_width=True, 
                                 output_format="JPEG", channels="RGB")
            else:
                st.info("No images uploaded yet. Check back soon!")
        else:
            st.info("Gallery is being set up. Check back soon!")
    
    with tab2:
        if os.path.exists(VIDEOS_DIR):
            video_files = [f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
            
            if video_files:
                for video_file in video_files:
                    video_path = os.path.join(VIDEOS_DIR, video_file)
                    st.video(video_path)
            else:
                st.info("No videos uploaded yet. Check back soon!")
        else:
            st.info("Video gallery is being set up. Check back soon!")

def contact_page():
    st.markdown('<h2 class="section-header">Contact Us</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3>Get in Touch</h3>', unsafe_allow_html=True)
        
        # Contact Form
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Name*")
            mobile = st.text_input("Mobile Number*")
            email = st.text_input("Email*")
            place = st.text_input("Place*")
            message = st.text_area("Your Message (Optional)")
            
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                if name and mobile and email and place:
                    # Validate fields
                    if not mobile.isdigit() or len(mobile) < 10:
                        st.error("Please enter a valid mobile number.")
                    elif "@" not in email:
                        st.error("Please enter a valid email address.")
                    else:
                        # Save lead information
                        new_lead = pd.DataFrame({
                            "Name": [name],
                            "Mobile": [mobile],
                            "Email": [email],
                            "Place": [place],
                            "Message": [message],
                            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                        })
                        
                        if os.path.exists(LEADS_FILE):
                            leads_df = pd.read_csv(LEADS_FILE)
                            leads_df = pd.concat([leads_df, new_lead], ignore_index=True)
                        else:
                            leads_df = new_lead
                        
                        leads_df.to_csv(LEADS_FILE, index=False)
                        
                        st.success("Thank you for contacting us! We will get back to you soon.")
                else:
                    st.error("Please fill in all required fields.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Contact Information</h3>
            <p>📧 Email: info@sainfinityarts.in</p>
            <p>📱 Phone: +91 7995902919</p>
            <p>📍 Address:#9-34/H Ravindranagar,Habsiguda,Hyderabad, India #2-45 Village Manadamarri,Mancherial District</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Apply custom CSS
    local_css()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    pages = {
        "Home": home_page,
        "Gallery": gallery_page,
        "Contact Us": contact_page,
        "Admin": admin_page
    }
    
    page = st.sidebar.radio("Go to", list(pages.keys()))
    
    # Display selected page
    pages[page]()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 SA Infinity Arts. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()