import streamlit as st
from fpdf import FPDF
import tempfile
import os
from datetime import datetime

# ---------------------------
# Ice Cream Items Grouped by Category
# ---------------------------
ice_cream_categories = {
    "Bricks": ["Vanilla", "Alphanzo Mango", "Chocolate", "Chocchips", "Butterscotch", "Strawberry", "Blackcurrant", "Kesar Pista", "Rajbhog", "American Nuts", "Kaju Draksh", "Afgandry Fruits", "Tutti Frutti"],
    "Cones": ["Choco Crunch cone", "Blackcurrant cone","Vanilla cone 30 Rs.", "Butterscotch cone", "DarkChocolate cone", "Vanilla cone 10 Rs."],
    "Cups": ["Strawberry Cup", "Vanilla cup"],
    "Family Packs 2 L": ["Butterscotch 2 L", "Vanilla 2 L"],
    "Stick": ["Chocobar 10 Rs.", "Chocobar 20 Rs.", "Frostik", "Mango Duet", "Raspberry", "Asli Aam", "Rajbhog Kulfi", "Pista Malai Kulfi", "Badshahi Kulfi", "Rabdi Kulfi", "Punjabi        Kulfi", "Bombay Kulfi", "Rajwadi Kulfi", "Ice licky mango 5 Rs."],
    "Tub": ["Vanilla Tub" ,"Butterscotch Tub", "Fruit n Nuts Tub"]
}

# ---------------------------
# Streamlit App UI
# ---------------------------
st.title("Devansh Parashar")
st.markdown("Order your AMUL ICE CREAM")

st.markdown("Select quantity for each item by category:")

quantities = {}

# Loop through categories
for category, items in ice_cream_categories.items():
    st.subheader(category)
    for item in items:
        qty = st.number_input(f"{item}", min_value=0, max_value=100, value=0, step=1, key=item)
        quantities[item] = qty

# ---------------------------
# Generate PDF Button
# ---------------------------
if st.button("Generate PDF Order"):
    order_items = {k: v for k, v in quantities.items() if v > 0}

    if not order_items:
        st.warning("Please select at least one item to generate PDF.")
    else:
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt="MAA GANGA DAIRY AND SWEET", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Gorakhpur Shahnagar, Dehradun, Uttarakhand", ln=True, align="C")
        pdf.ln(10)

        # Title
        pdf.set_font("Arial", style="B", size=13)
        pdf.cell(200, 10, txt="Ice Cream Order Summary", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.ln(5)

        # Date
        today = datetime.now().strftime("%d-%m-%Y %H:%M")
        pdf.cell(200, 10, txt=f"Date: {today}", ln=True)
        pdf.ln(5)

        # Add items by category
        for category, items in ice_cream_categories.items():
            category_printed = False
            for item in items:
                if item in order_items:
                    if not category_printed:
                        pdf.set_font("Arial", style="B", size=12)
                        pdf.cell(200, 10, txt=f"{category}:", ln=True)
                        category_printed = True
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt=f"{item} - {order_items[item]}", ln=True)
            if category_printed:
                pdf.ln(3)

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            pdf.output(tmpfile.name)
            tmpfile_path = tmpfile.name

        st.success("PDF generated successfully!")
        st.download_button(
            label="Download PDF",
            data=open(tmpfile_path, "rb"),
            file_name="ice_cream_order.pdf",
            mime="application/pdf"
        )

        os.remove(tmpfile_path)
