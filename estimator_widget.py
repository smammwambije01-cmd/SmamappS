from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton,MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.clock import Clock
#from kivymd.uix.spinner import MDSpinner
from kivy.metrics import dp
from kivy.clock import Clock
import threading
import os

# Jaribu ku-import fpdf toka folder la project
try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

class FurnitureEstimatorWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(8)
        self.size_hint_y = None
        self.height = dp(650) # Inatosha kwenye screens nyingi

        # 1. Data & Prices
        self.wood_types = {"MDF (18mm)": 55000, "Plywood (12mm)": 75000, "Blockboard": 65000}
        self.selected_wood = "MDF (18mm)"

        # 2. UI Elements
        self.h_in = MDTextField(mode='filled', input_filter="float")
        self.w_in = MDTextField(hint_text="Upana (mm)", mode='filled', input_filter="float")
        self.doors_in = MDTextField(hint_text="Milango", mode='filled', input_filter="int")
        self.drawers_in = MDTextField(hint_text="Droo", mode='filled', input_filter="int")
        self.h_in.add_widget(MDTextFieldHintText(text="Urefu (mm)"))
        self.w_in.add_widget(MDTextFieldHintText(text="Upana (mm)"))
        self.doors_in.add_widget(MDTextFieldHintText(text="Milango"))
        self.drawers_in.add_widget(MDTextFieldHintText(text="Droo"))
        self.wood_btn = MDButton(MDButtonText(text=f"Mbao: {self.selected_wood}"), pos_hint={'center_x': .5}, on_release=self.open_menu)
        
        # Checkbox ya Ufundi
        labor_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        self.labor_check = MDCheckbox(active=True, size_hint=(None, None), size=(dp(40), dp(40)))
        labor_box.add_widget(self.labor_check)
        labor_box.add_widget(MDLabel(text="Gharama ya ufundi", theme_text_color="Secondary"))

        # Spinner & Results
        #self.spinner = MDSpinner(size_hint=(None, None), size=(dp(30), dp(30)), pos_hint={'center_x': .5}, active=False)
        self.result_label = MDLabel(text="Gharama: TSh 0", halign="center")

        # Buttons
        calc_btn = MDButton(MDButtonText(text="PIGA HESABU"), md_bg_color="green", pos_hint={'center_x': .5}, on_release=self.start_calc)
        pdf_btn = MDButton(MDButtonText(text="SAVE PDF"), md_bg_color="blue", pos_hint={'center_x': .5}, on_release=self.start_pdf)
        reset_btn = MDButton(MDButtonText(text="RESET"), md_bg_color="red", pos_hint={'center_x': .5}, on_release=self.clear_all)

        # Build Layout
        for w in [self.h_in, self.w_in, self.doors_in, self.drawers_in, self.wood_btn, labor_box, calc_btn, pdf_btn, reset_btn, self.result_label]:
            self.add_widget(w)

        # Menu Setup
        menu_items = [{"viewclass": "OneLineListItem", "text": x, "on_release": lambda x=x: self.set_wood(x)} for x in self.wood_types.keys()]
        self.menu = MDDropdownMenu(caller=self.wood_btn, items=menu_items, width_mult=4)

    def set_wood(self, item):
        self.selected_wood = item
        self.wood_btn.text = f"Mbao: {item}"
        self.menu.dismiss()

    def open_menu(self, inst): self.menu.open()

    def start_calc(self, *args):
        #self.spinner.active = True
        Clock.schedule_once(self.calculate, 0.5)

    def calculate(self, dt):
        try:
            h, w = float(self.h_in.text), float(self.w_in.text)
            d, dr = int(self.doors_in.text or 0), int(self.drawers_in.text or 0)
            sheets = round(((h * w) * 1.15) / (2400 * 1200), 1)
            mat_total = (sheets * self.wood_types[self.selected_wood]) + (d * 3000) + (dr * 8000)
            labor = mat_total * 0.20 if self.labor_check.active else 0
            self.result_label.text = f"Material: {mat_total:,.0f}\nUfundi: {labor:,.0f}\nJUMLA: TSh {mat_total+labor:,.0f}"
        except: self.result_label.text = "Jaza vipimo!"
        #self.spinner.active = False

    def start_pdf(self, *args):
        if not FPDF: 
            self.result_label.text = "FPDF missing!"
            return
        threading.Thread(target=self.generate_pdf).start()

    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="QUOTATION YA KABATI", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Maelezo: {self.result_label.text}", ln=True)
        pdf.output("Quotation.pdf")
        Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', "PDF Saved!"), 0)

    def clear_all(self, *args):
        self.h_in.text = ""; self.w_in.text = ""; self.doors_in.text = ""; self.drawers_in.text = ""
        self.result_label.text = "Gharama: TSh 0"; self.labor_check.active = True
