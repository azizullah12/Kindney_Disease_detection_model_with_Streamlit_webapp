import joblib
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

# Set page config FIRST
st.set_page_config(
    page_title="Kidney Disease Prediction",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "AI Kidney Prediction App developed with Streamlit"}
)

# Custom background color
st.markdown("""
    <style>
        body {
            background-color: #f0f8ff;
        }
        .stApp {
            background-color: #f0f8ff;
        }
        .main-title {
            text-align: center;
            font-size: 40px;
            color: #1e3d59;
        }
        .subtext {
            text-align: center;
            font-size: 18px;
            color: #4f6d7a;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    selected_tab = option_menu(
        "Prediction Menu",
        ["Kidney Disease Prediction"],
        icons=["droplet"],
        menu_icon="stethoscope",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#e6f2ff"},
            "icon": {"color": "#1e3d59", "font-size": "20px"},
            "nav-link": {"font-size": "18px", "text-align": "left", "margin": "5px"},
            "nav-link-selected": {"background-color": "#1e90ff", "color": "white"},
        }
    )

# Load kidney model with joblib
@st.cache_resource
def load_model():
    try:
        model = joblib.load('kidney_model.pkl')
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

kidney_model = load_model()

# Main interface
if selected_tab == "Kidney Disease Prediction":
    st.markdown('<div class="main-title">Kidney Disease Prediction App</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">Predict the likelihood of kidney disease based on health parameters</div><br>', unsafe_allow_html=True)

    # Optional: Add a health-related banner image
    try:
        banner = Image.open("kidney_banner.jpg")
        st.image(banner, use_column_width=True)
    except:
        pass

    if kidney_model:
        with st.form("kidney_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                age = st.number_input("Age", min_value=0, step=1)
                bp = st.number_input("Blood Pressure", min_value=0, step=1)
                sg = st.selectbox("Specific Gravity", [1.005, 1.010, 1.015, 1.020, 1.025])
                al = st.number_input("Albumin", min_value=0, step=1)
                su = st.number_input("Sugar", min_value=0, step=1)

            with col2:
                rbc = st.selectbox("Red Blood Cells", ["normal", "abnormal"])
                pc = st.selectbox("Pus Cell", ["normal", "abnormal"])
                pcc = st.selectbox("Pus Cell Clumps", ["notpresent", "present"])
                ba = st.selectbox("Bacteria", ["notpresent", "present"])
                bgr = st.number_input("Blood Glucose Random", min_value=0, step=1)

            with col3:
                bu = st.number_input("Blood Urea", min_value=0, step=1)
                sc = st.number_input("Serum Creatinine", min_value=0.0, step=0.1)
                sod = st.number_input("Sodium", min_value=0.0, step=0.1)
                pot = st.number_input("Potassium", min_value=0.0, step=0.1)
                hemo = st.number_input("Hemoglobin", min_value=0.0, step=0.1)

            col4, col5, col6 = st.columns(3)

            with col4:
                pcv = st.number_input("Packed Cell Volume", min_value=0, step=1)
                wc = st.number_input("White Blood Cell Count", min_value=0, step=1)
                rc = st.number_input("Red Blood Cell Count", min_value=0.0, step=0.1)

            with col5:
                htn = st.selectbox("Hypertension", ["no", "yes"])
                dm = st.selectbox("Diabetes Mellitus", ["no", "yes"])
                cad = st.selectbox("Coronary Artery Disease", ["no", "yes"])

            with col6:
                appet = st.selectbox("Appetite", ["good", "poor"])
                pe = st.selectbox("Pedal Edema", ["no", "yes"])
                ane = st.selectbox("Anemia", ["no", "yes"])

            submitted = st.form_submit_button("Predict Kidney Disease 🚀")

        if submitted:
            try:
                input_data = [[
                    age, bp, sg, al, su,
                    1 if rbc == "abnormal" else 0,
                    1 if pc == "abnormal" else 0,
                    1 if pcc == "present" else 0,
                    1 if ba == "present" else 0,
                    bgr, bu, sc, sod, pot, hemo, pcv, wc, rc,
                    1 if htn == "yes" else 0,
                    1 if dm == "yes" else 0,
                    1 if cad == "yes" else 0,
                    1 if appet == "poor" else 0,
                    1 if pe == "yes" else 0,
                    1 if ane == "yes" else 0
                ]]

                prediction = kidney_model.predict(input_data)[0]
                confidence = kidney_model.predict_proba(input_data)[0][prediction]

                result = "Positive" if prediction == 1 else "Negative"
                st.success(f"Kidney Disease Prediction: {result}")
                st.info(f"Confidence Level: {confidence * 100:.2f}%")

            except Exception as e:
                st.error(f"Prediction error: {e}")
