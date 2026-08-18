def estimate_cabinet_mbao(h, w, d, t, shelves=0):
    """
    h=height, w=width, d=depth, t=thickness (all in mm)
    Returns list of parts and total sheets required.
    """
    # 1. Calculate individual panels
    # Side panels run the full height
    side_panels = {"name": "Sides", "qty": 2, "h": h, "w": d}
    
    # Top and Bottom sit BETWEEN the sides
    top_bottom = {"name": "Top/Bottom", "qty": 2, "h": w - (2 * t), "w": d}
    
    # Back panel covers the whole rear
    back_panel = {"name": "Backing", "qty": 1, "h": h, "w": w}
    
    parts = [side_panels, top_bottom, back_panel]
    
    # 2. Add Shelves if needed (usually 2mm shallower to clear doors)
    if shelves > 0:
        parts.append({"name": "Shelves", "qty": shelves, "h": w - (2 * t), "w": d - 2})

    # 3. Calculate Total Area (m²)
    total_mm2 = sum([p['qty'] * p['h'] * p['w'] for p in parts])
    total_m2 = total_mm2 / 1_000_000
    
    # 4. Convert to Standard 8x4 Sheets (~2.97 m²)
    # We add 15% for cutting waste (saw blade kerf and mistakes)
    m2_with_waste = total_m2 * 1.15
    sheets = m2_with_waste / 2.97
    
    return {
        "cut_list": parts,
        "total_m2": round(total_m2, 2),
        "sheets_to_buy": round(sheets, 1)
    }

# Example: 1.8m High, 0.9m Wide Cabinet using 18mm board
result = estimate_cabinet_mbao(1800, 900, 600, 18, shelves=3)
print(f"You need approx {result['sheets_to_buy']} sheets of mbao.")

def calculate_cabinet_cost(h, w, d, t, price_per_sheet, shelves=0):
    # Reuse your previous logic to get the number of sheets
    result = estimate_cabinet_mbao(h, w, d, t, shelves)
    
    # Calculate costs
    material_cost = result['sheets_to_buy'] * price_per_sheet
    
    # Add a 'Fundi' (Labor) and Transport estimate (e.g., 20% of materials)
    labor_cost = material_cost * 0.20
    total_project_cost = material_cost + labor_cost
    
    return {
        "sheets": result['sheets_to_buy'],
        "material_tsh": round(material_cost, -2), # Round to nearest 100
        "labor_tsh": round(labor_cost, -2),
        "total_tsh": round(total_project_cost, -2)
    }

# Example: 18mm MDF at TSh 75,000 per sheet
estimate = calculate_cabinet_cost(1800, 900, 600, 18, 75000, shelves=3)
print(f"Materials: TSh {estimate['material_tsh']:,}")
print(f"Total Estimate: TSh {estimate['total_tsh']:,}")

from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.anchorlayout import AnchorLayout

class FurnitureApp(MDApp):
    def show_cabinet_results(self, h, w, d, t, price, shelves):
        # 1. Get the data from our calculation functions
        calc_data = estimate_cabinet_mbao(h, w, d, t, shelves)
        cost_data = calculate_cabinet_cost(h, w, d, t, price, shelves)
        
        # 2. Format the Cut List for the table rows
        # Format: (Part Name, Quantity, Height mm, Width mm)
        table_rows = [
            (p['name'], str(p['qty']), f"{p['h']}mm", f"{p['w']}mm") 
            for p in calc_data['cut_list']
        ]
        
        # 3. Create the MDDataTable
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("Part Name", dp(30)),
                ("Qty", dp(15)),
                ("Height", dp(25)),
                ("Width", dp(25)),
            ],
            row_data=table_rows
        )
        
        # Add to your screen (using an AnchorLayout to center it)
        layout = AnchorLayout()
        layout.add_widget(self.data_tables)
        return layout

from kivymd.uix.textfield import MDTextField

# In your Screen class:
def create_inputs(self):
    self.h_input = MDTextField(
        hint_text="Urefu wa msumari (inchi)",
        helper_text="ni tarakimu tu ndo zinzhitajika",
        helper_text_mode="on_error",
        input_filter="float",  # Restricts keyboard to numbers/decimals
        pos_hint={"center_x": .5, "center_y": .8},
        size_hint_x=.8,
        max_text_length=3
    )
    return self.h_input

def validate_and_calculate(self):
    # Check if fields are empty
    if not self.h_input.text or not self.w_input.text:
        self.h_input.error = True
        self.h_input.helper_text = "This field is required!"
        return False
    
    try:
        height = float(self.h_input.text)
        # Proceed to your calculation logic...
        self.show_results(height)
    except ValueError:
        self.h_input.error = True
        return False

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

def create_summary_card(self, total_tsh, total_sheets):
    card = MDCard(
        orientation='vertical',
        padding="16dp",
        size_hint=(0.8, None),
        height="120dp",
        pos_hint={"center_x": .5, "center_y": .2},
        style="filled", # Material 3 style
        theme_bg_color="Custom",
        md_bg_color=(0.2, 0.2, 0.2, 1) # Dark grey background
    )
    
    card.add_widget(MDLabel(
        text=f"Total Cost: TSh {total_tsh:,}",
        theme_text_color="Primary",
        font_style="Headline",
        role="medium"
    ))
    
    card.add_widget(MDLabel(
        text=f"Estimate: {total_sheets} Sheets of Mbao",
        theme_text_color="Secondary",
        font_style="Title",
        role="small"
    ))
    
    return card

def estimate_finishing(total_m2_wood, paint_price_per_litre):
    # Total surface area is wood area * 2 (both sides) + 15% waste
    finishing_area = (total_m2_wood * 2) * 1.15
    
    # 2 coats of paint at 12m2 per litre
    litres_required = (finishing_area * 2) / 12
    paint_cost = litres_required * paint_price_per_litre
    
    return {
        "finishing_area_m2": round(finishing_area, 2),
        "litres_needed": round(litres_required, 2),
        "paint_cost_tsh": round(paint_cost, -2)
    }

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

def generate_cabinet_pdf(filename, calc_results, cost_summary):
    # 1. Path setup (Use internal app storage for Android 8/11 compatibility)
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # 2. Title and Summary
    elements.append(Paragraph("Karakana: Furniture Estimate Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total Cost Estimate: TSh {cost_summary['total_tsh']:,}", styles['Normal']))
    elements.append(Paragraph(f"Materials: {cost_summary['sheets']} Sheets of Mbao", styles['Normal']))
    elements.append(Spacer(1, 20))

    # 3. Cut List Table
    data = [["Part Name", "Qty", "Height (mm)", "Width (mm)"]]
    for p in calc_results['cut_list']:
        data.append([p['name'], str(p['qty']), f"{p['h']}", f"{p['w']}"])

    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    elements.append(t)

    # 4. Save
    doc.build(elements)

from jnius import autoclass, cast
from kivy.utils import platform

def share_pdf_to_whatsapp(file_path):
    if platform == 'android':
        # 1. Get Android Java classes
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        String = autoclass('java.lang.String')
        Uri = autoclass('android.net.Uri')
        File = autoclass('java.io.File')
        
        # 2. Create the File and Uri
        # Note: Android 11+ requires FileProvider. For Android 8, Uri.fromFile works.
        report_file = File(file_path)
        uri = Uri.fromFile(report_file)

        # 3. Build the Intent
        share_intent = Intent()
        share_intent.setAction(Intent.ACTION_SEND)
        share_intent.setType('application/pdf') #
        share_intent.putExtra(Intent.EXTRA_STREAM, uri)
        
        # 4. Optional: Force WhatsApp only
        # share_intent.setPackage("com.whatsapp") 

        # 5. Start the Chooser
        chooser = Intent.createChooser(share_intent, String("Share Cabinet Report"))
        PythonActivity.mActivity.startActivity(chooser)
    else:
        print(f"Sharing is only supported on Android. File is at: {file_path}")

from kivymd.uix.button import MDFloatingActionButton

# Inside your Screen class:
share_btn = MDFloatingActionButton(
    icon="whatsapp",
    pos_hint={"center_x": .8, "center_y": .1},
    on_release=lambda x: self.share_pdf_to_whatsapp(self.pdf_path)
)

from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDCheckbox:
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_active: app.on_checkbox_active(*args)
'''

class Example(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_checkbox_active(self, checkbox, value):
        if value:
            print("Checkbox is active")
        else:
            print("Checkbox is inactive")

Example().run()

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.selectioncontrol import MDCheckbox

KV = '''
MDBoxLayout:
    orientation: "vertical"
    padding: "20dp"
    spacing: "10dp"
    md_bg_color: self.theme_cls.backgroundColor

    MDBoxLayout:
        adaptive_height: True
        MDCheckbox:
            id: parent_check
            size_hint: None, None
            size: "48dp", "48dp"
            on_release: app.on_parent_click(self.active)
        MDLabel:
            text: "Select All Tasks"
            adaptive_height: True
            pos_hint: {"center_y": .5}

    MDBoxLayout:
        orientation: "vertical"
        padding: ["48dp", 0, 0, 0]
        adaptive_height: True
        id: children_container
'''

class Example(MDApp):
    def build(self):
        screen = Builder.load_string(KV)
        # Adding children dynamically
        for i in range(3):
            child_box = MDBoxLayout(adaptive_height=True)
            check = MDCheckbox(size_hint=(None, None), size=("48dp", "48dp"))
            check.bind(active=self.on_child_click)
            child_box.add_widget(check)
            child_box.add_widget(MDLabel(text=f"Task {i+1}", pos_hint={"center_y": .5}))
            screen.ids.children_container.add_widget(child_box)
        return screen

    def on_parent_click(self, active):
        for child_box in self.ids.children_container.children:
            for widget in child_box.children:
                if isinstance(widget, MDCheckbox):
                    widget.active = active

    def on_child_click(self, instance, value):
        # Logic to update parent state based on children can be added here
        pass

Example().run()
