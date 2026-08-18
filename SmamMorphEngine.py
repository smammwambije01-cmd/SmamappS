import math
import json
import sqlite3
import base64
import io
from kivy.uix.floatlayout import FloatLayout
import traceback
from kivy.properties import (
    NumericProperty, 
    ListProperty, 
    ObjectProperty, 
    StringProperty, 
    BooleanProperty  # <--- Ongeza hii hapa!
)

from kivy.metrics import dp
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line, Mesh
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.scrollview import MDScrollView
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, StringProperty

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
# Futa MDMenuItem hapo juu
import random
from kivy.app import App
app=App.get_running_app()
from kivymd.uix.dialog import (
    MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldHelperText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, Rectangle, Line, Mesh # ONGEZA HII
from kivy.core.text import Label as CoreLabel
from Mahesabu_ya_kabati import Chagua_malighafi
Window.softinput_mode='below_target'
# ==========================================
# 🪵 MASTER BONGO CATALOG (OFFICIAL DATABASE)
# ==========================================
BONGO_WOOD_CATALOG = {
    # --- MBAO ZA ASILI (NATURAL TIMBER) ---
    "Mligoti (Pole/Eucalyptus)": {"color": [0.88, 0.82, 0.65, 1], "shade": 0.05},
    "Mninga (Bloodwood)": {"color": [0.55, 0.15, 0.08, 1], "shade": 0.09},
    "Mtiki (Teak)": {"color": [0.48, 0.38, 0.22, 1], "shade": 0.07},
    "Mpingo (Ebony)": {"color": [0.05, 0.05, 0.05, 1], "shade": 0.02},
    "Seplasi (Cypress)": {"color": [0.82, 0.75, 0.52, 1], "shade": 0.04},

    "Mvule (Iroko)": {"color": [0.72, 0.55, 0.28, 1], "shade": 0.08},
    "Mkaratusi (Eucalyptus)": {"color": [0.78, 0.68, 0.58, 1], "shade": 0.06},
    "Msindano (Pine)": {"color": [0.92, 0.85, 0.6, 1], "shade": 0.03},
    "Mkongo": {"color": [0.38, 0.12, 0.08, 1], "shade": 0.10},
    "Mvange": {"color": [0.3, 0.2, 0.15, 1], "shade": 0.07},
    "Muwa": {"color": [0.85, 0.8, 0.7, 1], "shade": 0.04},
    "Membule": {"color": [0.6, 0.4, 0.3, 1], "shade": 0.06},
    "Mbao za Dawa (Treated)": {"color": [0.35, 0.42, 0.32, 1], "shade": 0.05},
    "Mbao za Machame (Soft)": {"color": [0.85, 0.78, 0.65, 1], "shade": 0.04},

    # --- MBAO ZA VIWANDANI (ENGINEERED WOOD) ---
    "MDF (Medium Density Fiberboard)": {"color": [0.82, 0.71, 0.55, 1], "shade": 0.04},
    "HDF (High Density Fiberboard)": {"color": [0.45, 0.35, 0.25, 1], "shade": 0.06},
    "LDF (Low Density Fiberboard)": {"color": [0.9, 0.85, 0.75, 1], "shade": 0.03},
    "Marine Board (Waterproof)": {"color": [0.3, 0.15, 0.1, 1], "shade": 0.08},
    "Plywood (Kiwanjani/Ordinary)": {"color": [0.8, 0.72, 0.55, 1], "shade": 0.03},
    "Blockboard": {"color": [0.85, 0.75, 0.6, 1], "shade": 0.04},
    "Chipboard (Particulate Board)": {"color": [0.8, 0.75, 0.65, 1], "shade": 0.05},
    "Veneer (Oak Finish)": {"color": [0.75, 0.6, 0.4, 1], "shade": 0.07},
    "Melamine Board (Grey)": {"color": [0.7, 0.7, 0.7, 1], "shade": 0.04},
    "Laminate (Formica - White)": {"color": [0.98, 0.98, 0.98, 1], "shade": 0.02},

    # --- VIOO (GLASS & MIRRORS) ---
    "Kioo Clear (Clear Mirror)": {"color": [0.95, 0.98, 1.0, 1], "shade": 0.01},
    "Kioo cha Moshi (Smoked Mirror)": {"color": [0.2, 0.2, 0.2, 1], "shade": 0.05},
    "Kioo cha Tinted (Bronze)": {"color": [0.45, 0.35, 0.25, 0.8], "shade": 0.03},

    # --- RANGI ZA MSINGI (PAINTS) ---
    "Rangi Nyeupe (Pure White)": {"color": [1.0, 1.0, 1.0, 1], "shade": 0.01},
    "Rangi Nyeusi (Jet Black)": {"color": [0.0, 0.0, 0.0, 1], "shade": 0.02},
    "Rangi ya Kijivu (Cool Grey)": {"color": [0.5, 0.5, 0.5, 1], "shade": 0.05},
    "Rangi Nyekundu (Bright Red)": {"color": [0.8, 0.0, 0.0, 1], "shade": 0.06},
    "Rangi ya Bluu (Royal Blue)": {"color": [0.0, 0.2, 0.6, 1], "shade": 0.05},
    "Charcoal Grey": {"color": [0.2, 0.2, 0.2, 1], "shade": 0.03},
    "Cream / Off-White": {"color": [0.98, 0.96, 0.89, 1], "shade": 0.02},
    "Navy Blue": {"color": [0.0, 0.0, 0.3, 1], "shade": 0.04},

    # --- RANGI ZA METALI (METALLICS) ---
    "Gold (Dhahabu)": {"color": [0.83, 0.68, 0.21, 1], "shade": 0.02},
    "Silver (Fedha/Chrome)": {"color": [0.75, 0.75, 0.75, 1], "shade": 0.01},
    "Bronze (Shaba)": {"color": [0.5, 0.29, 0.14, 1], "shade": 0.04},
    "Rose Gold": {"color": [0.72, 0.45, 0.42, 1], "shade": 0.03},

    # --- VARNISH NA WOOD STAINS ---
    "Clear Varnish": {"color": [0.95, 0.9, 0.8, 0.5], "shade": 0.02},
    "Mahogany Stain": {"color": [0.4, 0.1, 0.1, 0.9], "shade": 0.08},
    "Walnut Stain": {"color": [0.27, 0.18, 0.11, 0.9], "shade": 0.10},
    "Oak Stain": {"color": [0.8, 0.6, 0.3, 0.9], "shade": 0.06}
}
    #CATALOG_NATURAL_TIMBER = {
BONGO_WOOD_CATALOG={
    "Mninga (Bloodwood)": {"color": [0.30, 0.14, 0.08, 1], "shade": 0.07},
    "Mpingo (Ebony)": {"color": [0.05, 0.05, 0.05, 1], "shade": 0.02},
    "Mvule (Iroko)": {"color": [0.72, 0.55, 0.28, 1], "shade": 0.08},
    "Seplasi (Cypress)": {"color": [0.82, 0.75, 0.52, 1], "shade": 0.04},
    "Mligoti (Pole/Eucalyptus)": {"color": [0.88, 0.82, 0.65, 1], "shade": 0.05},
    "Mkaratusi (Eucalyptus Smooth)": {"color": [0.78, 0.68, 0.58, 1], "shade": 0.06},
    "Msindano (Pine)": {"color": [0.92, 0.85, 0.6, 1], "shade": 0.03},
    "Mkongo": {"color": [0.38, 0.12, 0.08, 1], "shade": 0.10},
    "Mvange": {"color": [0.3, 0.2, 0.15, 1], "shade": 0.07},
    "Mkuruti": {"color": [0.25, 0.14, 0.08, 1], "shade": 0.09},
    "Mbambakofi": {"color": [0.52, 0.22, 0.12, 1], "shade": 0.08},
    "Mbao za Machame (Soft)": {"color": [0.85, 0.78, 0.65, 1], "shade": 0.04},
    "Muwa": {"color": [0.85, 0.8, 0.7, 1], "shade": 0.04},
    "Membule": {"color": [0.6, 0.4, 0.3, 1], "shade": 0.06},
    "Mwembe (Mango Wood)": {"color": [0.65, 0.52, 0.38, 1], "shade": 0.06},
    "Mkorosho (Cashew Wood)": {"color": [0.76, 0.58, 0.44, 1], "shade": 0.05},
    "Mgunga (Acacia Wood)": {"color": [0.50, 0.35, 0.22, 1], "shade": 0.09},
    "Mkwaju (Tamarind Hardwood)": {"color": [0.32, 0.18, 0.12, 1], "shade": 0.11},
    "Mparachichi (Avocado Wood)": {"color": [0.82, 0.76, 0.62, 1], "shade": 0.04},
    "Mharita": {"color": [0.58, 0.45, 0.32, 1], "shade": 0.07},
    "Msandali (Sandalwood)": {"color": [0.74, 0.59, 0.42, 1], "shade": 0.05},
    "Mkenge": {"color": [0.42, 0.28, 0.18, 1], "shade": 0.08},
    "Msufi-Pori": {"color": [0.89, 0.84, 0.73, 1], "shade": 0.03},
    "Mvumo (Palmyra Wood)": {"color": [0.22, 0.18, 0.15, 1], "shade": 0.06},
    "Mvula (African Plum)": {"color": [0.68, 0.42, 0.28, 1], "shade": 0.07},
    "Rosewood (Mbao ya Waridi)": {"color": [0.40, 0.12, 0.14, 1], "shade": 0.08},
    "White Oak (Mwaloni Mweupe)": {"color": [0.84, 0.76, 0.63, 1], "shade": 0.05},
    "Red Oak (Mwaloni Mwekundu)": {"color": [0.77, 0.61, 0.50, 1], "shade": 0.06},
    "American Walnut": {"color": [0.28, 0.21, 0.16, 1], "shade": 0.09},
    "Maple Wood (Kileo Soft)": {"color": [0.94, 0.88, 0.78, 1], "shade": 0.03},
    "Mbao za Dawa (Treated Pine)": {"color": [0.35, 0.42, 0.32, 1], "shade": 0.05},
    #}
    #CATALOG_ENGINEERED_WOOD = {
    "MDF (Plain Board)": {"color": [0.82, 0.71, 0.55, 1], "shade": 0.04},
    "HDF (High Density Board)": {"color": [0.45, 0.35, 0.25, 1], "shade": 0.06},
    "LDF (Low Density Board)": {"color": [0.9, 0.85, 0.75, 1], "shade": 0.03},
    "Marine Board (Waterproof)": {"color": [0.3, 0.15, 0.1, 1], "shade": 0.08},
    "Plywood (Ordinary/Ordinary)": {"color": [0.8, 0.72, 0.55, 1], "shade": 0.03},
    "Blockboard (Plain Sheet)": {"color": [0.85, 0.75, 0.6, 1], "shade": 0.04},
    "Chipboard (Particulate Board)": {"color": [0.8, 0.75, 0.65, 1], "shade": 0.05},
    "Melamine Board (Grey)": {"color": [0.7, 0.7, 0.7, 1], "shade": 0.04},
    "Melamine (Super White Gloss)": {"color": [0.99, 0.99, 1.0, 1], "shade": 0.01},
    "Melamine (Matt Black)": {"color": [0.12, 0.12, 0.12, 1], "shade": 0.02},
    "Melamine (Wenge Pattern)": {"color": [0.20, 0.15, 0.12, 1], "shade": 0.07},
    "Melamine (Oak Grain Finish)": {"color": [0.74, 0.62, 0.45, 1], "shade": 0.05},
    "Melamine (Walnut Texture)": {"color": [0.36, 0.26, 0.18, 1], "shade": 0.08},
    "Laminate (Formica - White)": {"color": [0.98, 0.98, 0.98, 1], "shade": 0.02},
    "Laminate (Formica - Matt Black)": {"color": [0.15, 0.15, 0.15, 1], "shade": 0.02},
    "High Gloss Polygloss (Beige)": {"color": [0.94, 0.89, 0.80, 1], "shade": 0.03},
    "High Gloss Polygloss (Anthracite)": {"color": [0.22, 0.24, 0.26, 1], "shade": 0.04},
    "Eurodekor Particleboard": {"color": [0.78, 0.70, 0.58, 1], "shade": 0.04},
    "Plywood (Fancy Red Oak Veneer)": {"color": [0.65, 0.42, 0.35, 1], "shade": 0.05},
    "Blockboard (White Polyester Finish)": {"color": [0.96, 0.96, 0.96, 1], "shade": 0.02},
    "Compact Laminate (HPL Kitchen Top)": {"color": [0.25, 0.25, 0.26, 1], "shade": 0.04},
    "Acoustic Slatted Panel Board": {"color": [0.40, 0.32, 0.25, 1], "shade": 0.06},
    "OSB Board (Oriented Strand)": {"color": [0.78, 0.66, 0.46, 1], "shade": 0.05},
    "Gypsum Board (Water Resistant Green)": {"color": [0.75, 0.82, 0.76, 1], "shade": 0.02},
    #}
    #CATALOG_GLASS_MIRRORS = {
    "Kioo Clear (Clear Mirror)": {"color": [0.95, 0.98, 1.0, 1], "shade": 0.01},
    "Kioo cha Moshi (Smoked Mirror)": {"color": [0.2, 0.2, 0.2, 1], "shade": 0.05},
    "Kioo cha Tinted (Bronze Mirror)": {"color": [0.45, 0.35, 0.25, 0.8], "shade": 0.03},
    "Kioo cha Frosted (Kigaga/Barafu)": {"color": [0.88, 0.93, 0.95, 0.7], "shade": 0.02},
    "Kioo Fluted (Masingasinga/Ribbed)": {"color": [0.90, 0.94, 0.96, 0.65], "shade": 0.03},
    "Kioo cha Tinted (Grey/Black Glass)": {"color": [0.25, 0.25, 0.25, 0.75], "shade": 0.04},
    "Kioo cha Kale (Antique Mirror FX)": {"color": [0.70, 0.68, 0.62, 0.9], "shade": 0.06},
    "Kioo One-Way (Spy Mirror)": {"color": [0.30, 0.35, 0.40, 0.95], "shade": 0.03},
    "Reed Glass (Uso wa Mawimbi)": {"color": [0.92, 0.95, 0.97, 0.6], "shade": 0.02},
    "Wired Glass (Kioo cha Nyavu za Chuma)": {"color": [0.85, 0.88, 0.90, 0.85], "shade": 0.04},
    #}
    #CATALOG_METALS = {
    "Gold (Dhahabu ya Kishua)": {"color": [0.83, 0.68, 0.21, 1], "shade": 0.02},
    "Silver (Fedha/Chrome ya Kioo)": {"color": [0.75, 0.75, 0.75, 1], "shade": 0.01},
    "Bronze (Shaba ya Kitambo)": {"color": [0.5, 0.29, 0.14, 1], "shade": 0.04},
    "Rose Gold (Dhahabu ya Waridi)": {"color": [0.72, 0.45, 0.42, 1], "shade": 0.03},
    "Aluminium (Anodized Black)": {"color": [0.18, 0.18, 0.20, 1], "shade": 0.02},
    "Chuma cha Kawaida (Raw Steel Frame)": {"color": [0.28, 0.30, 0.31, 1], "shade": 0.05},
    "Stainless Steel (Brushed Metal)": {"color": [0.68, 0.70, 0.72, 1], "shade": 0.02},
    "Brass (Shaba ya Manjano/Kupiga)": {"color": [0.78, 0.68, 0.28, 1], "shade": 0.03},
    "Copper (Shaba Nyekundu)": {"color": [0.72, 0.38, 0.22, 1], "shade": 0.04},
    "Iron (Cast Iron Matt Black)": {"color": [0.08, 0.08, 0.09, 1], "shade": 0.01},
    "Gunmetal Gray (Rangi ya Bunduki)": {"color": [0.33, 0.35, 0.37, 1], "shade": 0.04},
    "Wrought Iron (Chuma cha Kuchomelea)": {"color": [0.15, 0.15, 0.16, 1], "shade": 0.03},
    #}
    #CATALOG_WOOD_STAINS = {
    "Clear Varnish (Kung'arisha Tupu)": {"color": [0.95, 0.9, 0.8, 0.5], "shade": 0.02},
    "Mahogany Stain (Dawa Nyekundu)": {"color": [0.4, 0.1, 0.1, 0.9], "shade": 0.08},
    "Walnut Stain (Dawa ya Kahawia)": {"color": [0.27, 0.18, 0.11, 0.9], "shade": 0.10},
    "Oak Stain (Rangi ya Mwaloni)": {"color": [0.8, 0.6, 0.3, 0.9], "shade": 0.06},
    "Teak Oil Coating (Mafuta ya Mtiki)": {"color": [0.53, 0.42, 0.28, 0.8], "shade": 0.07},
    "Antique Wenge Stain (Dawa ya Giza)": {"color": [0.15, 0.10, 0.08, 0.95], "shade": 0.11},
    "Charcoal Eco-Stain": {"color": [0.18, 0.18, 0.19, 0.85], "shade": 0.05},
    "Cherry Wood Finish": {"color": [0.58, 0.22, 0.15, 0.9], "shade": 0.07},
    "Ebony Stain (Nyeusi ya Kupaka)": {"color": [0.08, 0.08, 0.08, 0.98], "shade": 0.02},
    "Linseed Oil Polish": {"color": [0.90, 0.82, 0.55, 0.4], "shade": 0.04},
    #}
    #CATALOG_ALL_PAINTS = {
    # --- RANGI NYEUPE NA OFF-WHITES (THE WHITES) ---
    "Pure White (Nyeupe Safi)": {"color": [1.0, 1.0, 1.0, 1], "shade": 0.01},
    "Ivory (Pembe ya Tembo)": {"color": [1.0, 1.0, 0.94, 1], "shade": 0.01},
    "Cream / Off-White": {"color": [0.98, 0.96, 0.89, 1], "shade": 0.02},
    "Alabaster White": {"color": [0.94, 0.94, 0.90, 1], "shade": 0.02},
    "Chalk White (Chaki)": {"color": [0.96, 0.96, 0.96, 1], "shade": 0.02},
    "Linen White": {"color": [0.96, 0.94, 0.88, 1], "shade": 0.02},
    "Pearl White (Lulu)": {"color": [0.98, 0.97, 0.93, 1], "shade": 0.01},

    # --- RANGI NYEUSI NA KIJIVU (THE MONOCHROMES) ---
    "Jet Black (Nyeusi Giza)": {"color": [0.0, 0.0, 0.0, 1], "shade": 0.02},
    "Matt Black (Nyeusi Isiyong'aa)": {"color": [0.08, 0.08, 0.08, 1], "shade": 0.02},
    "Charcoal Grey (Kijivu Kilichokoza)": {"color": [0.2, 0.2, 0.2, 1], "shade": 0.03},
    "Cool Grey (Kijivu Safi)": {"color": [0.5, 0.5, 0.5, 1], "shade": 0.05},
    "Anthracite (Kijivu cha Makaa)": {"color": [0.23, 0.25, 0.27, 1], "shade": 0.04},
    "Slate Grey": {"color": [0.44, 0.47, 0.49, 1], "shade": 0.05},
    "Light Grey (Kijivu Chepesi)": {"color": [0.75, 0.75, 0.75, 1], "shade": 0.03},
    "Graphite (Rangi ya Penseli)": {"color": [0.15, 0.17, 0.18, 1], "shade": 0.02},

    # --- TONI ZA UDONGO NA KAHAWIA (THE EARTHY TONES) ---
    "Taupe (Warm Earthy Grey)": {"color": [0.70, 0.65, 0.60, 1], "shade": 0.04},
    "Beige Luxury Matt": {"color": [0.89, 0.85, 0.76, 1], "shade": 0.03},
    "Terracotta (Udongo Mwekundu)": {"color": [0.72, 0.38, 0.24, 1], "shade": 0.05},
    "Chocolate Brown": {"color": [0.26, 0.16, 0.11, 1], "shade": 0.08},
    "Khaki Finish": {"color": [0.76, 0.70, 0.55, 1], "shade": 0.04},
    "Caramel": {"color": [0.76, 0.53, 0.28, 1], "shade": 0.06},
    "Espresso (Kahawa Nzito)": {"color": [0.19, 0.13, 0.11, 1], "shade": 0.09},
    "Sand (Mchanga)": {"color": [0.86, 0.80, 0.67, 1], "shade": 0.03},
    "Camel (Rangi ya Ngamia)": {"color": [0.76, 0.60, 0.42, 1], "shade": 0.05},

    # --- RANGI NYEKUNDU NA ZABIBU (THE REDS & PINKS) ---
    "Bright Red (Nyekundu ya Alama)": {"color": [0.8, 0.0, 0.0, 1], "shade": 0.06},
    "Burgundy (Mvinyo Mzito)": {"color": [0.42, 0.05, 0.15, 1], "shade": 0.07},
    "Crimson Red": {"color": [0.68, 0.05, 0.12, 1], "shade": 0.06},
    "Soft Pink (Blush Matt)": {"color": [0.92, 0.75, 0.75, 1], "shade": 0.02},
    "Rose Pink": {"color": [0.90, 0.40, 0.55, 1], "shade": 0.04},
    "Coral (Rangi ya Matumbawe)": {"color": [0.97, 0.47, 0.36, 1], "shade": 0.05},
    "Salmon": {"color": [0.98, 0.50, 0.45, 1], "shade": 0.04},
    "Magenta": {"color": [0.8, 0.0, 0.5, 1], "shade": 0.06},

    # --- RANGI ZA BLUU NA ZAMBARAU (THE BLUES & PURPLES) ---
    "Royal Blue (Bluu ya Kifalme)": {"color": [0.0, 0.2, 0.6, 1], "shade": 0.05},
    "Navy Blue (Bluu Nzito ya Shaba)": {"color": [0.0, 0.0, 0.3, 1], "shade": 0.04},
    "Teal Blue (Bluu-Kijani)": {"color": [0.0, 0.45, 0.48, 1], "shade": 0.05},
    "Sky Blue (Bluu ya Angani)": {"color": [0.53, 0.81, 0.92, 1], "shade": 0.03},
    "Baby Blue": {"color": [0.68, 0.85, 0.90, 1], "shade": 0.02},
    "Midnight Blue": {"color": [0.10, 0.10, 0.24, 1], "shade": 0.04},
    "Indigo": {"color": [0.29, 0.0, 0.51, 1], "shade": 0.05},
    "Purple (Zambarau Safi)": {"color": [0.5, 0.0, 0.5, 1], "shade": 0.06},
    "Lavender Mist": {"color": [0.84, 0.82, 0.90, 1], "shade": 0.02},
    "Plum (Zambaraubuni)": {"color": [0.35, 0.14, 0.28, 1], "shade": 0.07},

    # --- KISHUA KIJANI (THE GREENS) ---
    "Emerald Green (Kijani Kibichi)": {"color": [0.05, 0.35, 0.22, 1], "shade": 0.06},
    "Sage Green (Modern Kitchen Matt)": {"color": [0.54, 0.62, 0.52, 1], "shade": 0.03},
    "Olive Green (Kijani ya Mzeituni)": {"color": [0.38, 0.42, 0.28, 1], "shade": 0.04},
    "Mint Green (Kijani Laini)": {"color": [0.78, 0.90, 0.83, 1], "shade": 0.02},
    "Forest Green (Kijani ya Mwitu)": {"color": [0.13, 0.30, 0.15, 1], "shade": 0.05},
    "Army Green (Kijani ya Jeshi)": {"color": [0.29, 0.33, 0.19, 1], "shade": 0.04},
    "Lime Green": {"color": [0.30, 0.85, 0.10, 1], "shade": 0.04},
    "Seafoam Green": {"color": [0.62, 0.88, 0.75, 1], "shade": 0.02},

    # --- NJANO NA MACHUNGWA (THE YELLOWS & ORANGES) ---
    "Mustard Yellow (Njano iliyoiva)": {"color": [0.88, 0.68, 0.12, 1], "shade": 0.04},
    "Bright Yellow (Njano Safi)": {"color": [1.0, 0.85, 0.0, 1], "shade": 0.03},
    "Burnt Orange (Chungwa Lililoungua)": {"color": [0.78, 0.32, 0.10, 1], "shade": 0.06},
    "Peach": {"color": [1.0, 0.85, 0.73, 1], "shade": 0.02},
    "Tangerine (Chungwa Safi)": {"color": [0.95, 0.52, 0.0, 1], "shade": 0.05},
    "Lemon Yellow": {"color": [0.98, 0.93, 0.36, 1], "shade": 0.02},
    "Gold Paint (Rangi ya Dhahabu ya Brashi)": {"color": [0.83, 0.68, 0.21, 1], "shade": 0.02},

    # --- METALLIC GLOW FINISHES (FOR LUXURY TRIMS) ---
    "Champagne Gold": {"color": [0.95, 0.87, 0.73, 1], "shade": 0.02},
    "Rose Gold Paint": {"color": [0.72, 0.45, 0.42, 1], "shade": 0.03},
    "Metallic Silver Paint": {"color": [0.75, 0.75, 0.75, 1], "shade": 0.01},
    "Bronze Paint": {"color": [0.50, 0.29, 0.14, 1], "shade": 0.04},
    "Copper Paint": {"color": [0.72, 0.38, 0.22, 1], "shade": 0.04}
}
#BONGO_WOOD_CATALOG={}
'''BONGO_WOOD_CATALOG = {
    **CATALOG_NATURAL_TIMBER,
    **CATALOG_ENGINEERED_WOOD,
    **CATALOG_ALL_PAINTS,
    **CATALOG_GLASS_MIRRORS,
    **CATALOG_METALS,
    **CATALOG_WOOD_STAINS
}'''
def parse_steps(text_val):
    """Inageuza '0.4, 0.8' kuwa [0.4, 0.8]"""
    if not text_val.strip(): return [0.0]
    try:
        return [float(x.strip()) for x in text_val.split(",")]
    except:
        return [0.0]

class SmamMorphEngine(FloatLayout):
    ##print("\n\n\n\nkimeumanaaaaaaaaaaaa!\n\n\n\n")
    scene_objects = ListProperty([])
    selected_obj = ObjectProperty(None, allownone=True)
    is_constructed = BooleanProperty(False)
    show_labels = BooleanProperty(True)
    
    # World Rotation (Dunia/Uwanja)
    world_rot_x = NumericProperty(0)
    world_rot_y = NumericProperty(0)
    world_rot_z = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.app import App
        app = App.get_running_app()
        self._rendering_now = False
        # Default View: Jicho mita 8 nyuma, kimetulia mbele (Coordinate Fix)
        self.cam_x, self.cam_y, self.cam_z = 0.0, 1450, -5000 
        self.cam_rx, self.cam_ry = 0.0, 0.0
        self.f = 700
        self.speed=250
        self.focal=self.f 
        self.maboresho_sort='0'
        self.light_x, self.light_y = 0.5, 1.0
        self.touches = {}
        self.status = ""
        self.precision=0.005
        self.halisi={}
        self.eneo_=2
        self.rangi_zote=marangi={}
        # PRE-LOAD: Jenga Workshop mapema ili iwe fasta ikibonyezwa (Zero Lag)
        Clock.schedule_once(self._build_workshop_ui, 0.2)
        Clock.schedule_once(self._preload_catalog, 0)
        Clock.schedule_interval(self.run_engine_cycle, 1/30)
        #Clock.schedule_interval(self.malizana,0)
        self.bind(size=self.render_arch_scene)
        self.mahesabu=Chagua_malighafi(path=app.get_database_path(),mhitaji=self)
        self.current_mteja_id=''
        self.current_mteja=''
        self.project_name=''
        self.sample=[]
        self.vyote=''
        self.clip_plane_A = 0.0
        self.clip_plane_B = 0.0
        self.clip_plane_C = 0.0
        self.clip_plane_D = 999999.0
        self.is_constructed=True
        self.kazi=[]
        self.camera=[]
        self.status_label = MDLabel(
            text="", 
            markup=True,  # <--- HII NI MUHIMU!
            role='small'
            # ... zingine ...
        )
        self.add_widget(self.status_label)
        #Clock.schedule_interval(self.mahesabu.mbao_zinazohitajika,0)
        self.popup = MDDialog(
            MDDialogHeadlineText(text="Mpangilio wa namna panels zitakatwa kutoka kwenye BOARD",role='small'),
            MDDialogContentContainer(
                self.mahesabu.boards,
                orientation='vertical'
            ),
            radius=(7,7,7,7),
            theme_height='Custom',
            adaptive_height=True,
            height=0.5*Window.height,
            opacity=0
        )
        

    def kazi_ya_mwisho(self):
        db_path = os.path.join(self.db_path, 'kazi.sqlite')
            
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        query="""
            CREATE TABLE IF NOT EXIST Kazi ya mwisho(
            kazi_id TEXT PRIMARY KEY,)
        """
        
        query1 = """
            SELECT 
                COALESCE([jina maarufu], [jina la kwanza]) AS jina_chaguo,
                mahali, 
                anachohitaji,
                Namba 
            FROM Mteja
        """
        cursor.execute(query)
        rows = cursor.fetchall()

    def update_status(self, ujumbe, is_error=False):
        """Inaripoti hali bila kuzuia engine kurender"""
        try:
            # 1. Print kwanza kwenye terminal (Daima inafanya kazi)
            print(f"Algorithm Log: {ujumbe}")

            # 2. Tafuta label kitalamu bila kulazimisha mzunguko mrefu
            color= 'FF5252' if is_error else 'F0ADB5'
            prefix = "\n\n\nKimeumana...!!!\n" if is_error else ""
            # Jaribu kupata app moja kwa moja kama shortcut
            app = App.get_running_app()
            
            # Kama app ipo na ina label, itumie hiyo (Hii ni njia ya haraka zaidi)
            if hasattr(app, 'status_label'):
                try:
                    if is_error:
                        app.onyesha_error_popup(f"[color={color}]{prefix}{ujumbe}[/color]")
                    else:
                        app.status_label.text = f"[color={color}]{prefix}{ujumbe}[/color]"
                except Exception as e:
                    #app.part_label.text = "\nTunaendelea...!"
                    print(traceback.format_exc())
                    app.status_label.text = f"[color={color}]{prefix}{ujumbe}[/color]"
                    print('error popup imefeli pia')
                return # Tumemaliza hapa

            # 3. Kama shortcut imefeli, panda juu mara chache tu
            curr = self
            for _ in range(5): # Panda ngazi 5 tu, usizidishe
                if not curr.parent: break
                curr = curr.parent
                if hasattr(curr, 'status_label'):
                    curr.status_label.text = f"{ujumbe}"
                    break
        except Exception as e:
            #print(f" ")
            pass # Usiruhusu status iue uwanja

    def create_field(self, hint, helper, val="0.0", readonly=False):
        """Inajenga TextFields kwa asilimia ya screen - No DP"""
        f = MDTextField(mode="outlined", readonly=readonly, size_hint_x=0.95)
        f.pos_hint = {"center_x": 0.5}
        f.text = str(val)
        # Font size sasa inategemea urefu wa kioo
        f.font_size = Window.height * 0.022 
        f.add_widget(MDTextFieldHintText(text=hint))
        #f.add_widget(MDTextFieldHelperText(text=helper, mode="on_focus"))
        return f

    def _build_workshop_ui(self, *args):
        """Builds and caches the entire BIM Workshop UI for instant access"""
        if hasattr(self, 'workshop_layout'): return

        v_gap = Window.height * 0.015
        h_pad = Window.width * 0.05
        self.workshop_layout = MDBoxLayout(
            orientation="vertical", spacing=v_gap, 
            padding=[h_pad, v_gap, h_pad, Window.height * 0.15], 
            size_hint_y=None
        )
        self.workshop_layout.bind(minimum_height=self.workshop_layout.setter('height'))

        # --- TENGENEZA FIELDS ZOTE (Class Properties) ---
        import sqlite3, json, os
        from kivy.app import App
        app = App.get_running_app()
        db_path = os.path.join(app.db_path, "BIM_Factory.sqlite")
        con=sqlite3.connect(db_path)
        csr=con.cursor() 
        try:
            try:
                csr.execute('''
                    CREATE TABLE IF NOT EXISTS miradi_ya_fenicha (
                        mteja_id TEXT PRIMARY KEY, jina_la_mteja TEXT,
                        aina_ya_fenicha TEXT, data_ya_mchoro TEXT,
                        data_ya_kamera TEXT, tarehe_ya_kazi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                try:
                    csr.execute("ALTER TABLE miradi_ya_fenicha ADD COLUMN status INTEGER")
                    All_ids=cursor.execute("SELECT mteja_id FROM miradi_ya_fenicha").fetchall()
                    for i in range (len(All_ids)-1):
                        i=i+1
                        cursor.execute(f"UPDATE miradi_ya_fenicha SET status = ? WHERE mteja_id = ?",(i,f"{All_ids[i][0]}"))
                        print(f"ssss {All_ids[i][0]}")

                except:
                    #cursor.execute("ALTER TABLE miradi_ya_fenicha ADD COLUMN status INTEGER")
                    pass
            except: pass
            michoro=csr.execute(f"SELECT data_ya_mchoro FROM miradi_ya_fenicha").fetchall() 
            if len (michoro)>0:
                try:
                    data=csr.execute(f"SELECT data_ya_mchoro FROM miradi_ya_fenicha WHERE mteja_id = ?",str(self.current_mteja_id)).fetchone()
                    last=json.loads(data[0])
                    mteja=csr.execute(f"SELECT jina_la_mteja FROM miradi_ya_fenicha WHERE mteja_id = ?",str(self.current_mteja_id)).fetchone()
                    print(f'Tumepata data za kazi ya {mteja[0]}')
                except:
                    data=csr.execute(f"SELECT data_ya_mchoro FROM miradi_ya_fenicha WHERE status = {int(len(michoro))}").fetchone()
                    last=json.loads(data[0])
                    mteja=csr.execute(f"SELECT jina_la_mteja FROM miradi_ya_fenicha WHERE status = {int(len(michoro))}").fetchone()
                    print(f'Tumetumia data za kazi ya {mteja[0]}')

                last=last[-1]
                if len(last)>0:
                    id = last['id']
                    wood=last['wood_type']
                    parent=last["parent"]
                    asili=last["asili"]
                    self.halisi=last["halisi"]
                    upana=last['dim'][0]
                    kimo=last['dim'][1]
                    kina=last['dim'][2]
                    x=last['pos'][0]
                    y=last['pos'][1]
                    z=last['pos'][2]
                    #print(f"whoooo {self.f_w.text,last['dim'][0]}")
                    #print(f"\n\n\nNmetumia values za kazi ya {mteja[0]} za {last['id']}\n\n\n")
                    self.update_status(f"Karibu tena katika ulimwengu wa fenicha. Nakumbuka mara ya mwisho tulikuwa tunachora {last['id']} kwaajili ya kazi ya {mteja[0]}")
                else:
                    id = "Ubao"
                    wood="Seplasi (Cypress)"
                    parent=self.project_name
                    asili="Mbao"
                    #self.halisi=last["halisi"]
                    upana=20
                    kimo=2000
                    kina=600
                    x=0
                    y=0
                    z=0
                    print("\n\n\nNmetumia default values\n\n\n")
            else:
                id = "Ubao"
                wood="Seplasi (Cypress)"
                parent=self.project_name
                asili="Mbao"
                #self.halisi=last["halisi"]
                upana=20
                kimo=2000
                kina=600
                x=0
                y=0
                z=0
                print("\n\n\nNmetumia default values\n\n\n")
        except:
            id = "Ubao"
            wood="Seplasi (Cypress)"
            parent=self.project_name
            asili="Mbao"
            #self.halisi=last["halisi"]
            upana=20
            kimo=2000
            kina=600
            x=0
            y=0
            z=0
            print("\n\n\nNmetumia default values\n\n\n")
        con.close()

        self.f_id = self.create_field("ID ya Mbao", "Jina la kipekee (Unique ID)", id)
        self.f_parent = self.create_field("Parent ID", "Mbao mama ", parent)
        self.f_wood = self.create_field("Mwonekano wa nje", "Catalog ya vifaa", wood, readonly=True)
        self.f_asili=self.create_field("Asili","Mfano: mbao ao marineboard",asili, readonly=True)
        self.f_asili.bind(on_touch_up=lambda i, t: self.open_asili_menu(i) if i.collide_point(*t.pos) else None)
        self.f_wood.bind(on_touch_up=lambda i, t: self.open_wood_menu(i) if i.collide_point(*t.pos) else None)
        
        self.f_w = self.create_field("Upana (X)", "Mita (mfano: 0.6)", upana)
        self.f_h = self.create_field("Urefu (Y)", "Mita (mfano: 2.0)", kimo)
        self.f_d = self.create_field("Unene (Z)", "Mita (mfano: 0.02)", kina)
        
        self.f_x = self.create_field("Pos X", "Nafasi ya mhimili wa X", x)
        self.f_y = self.create_field("Pos Y", "Nafasi ya mhimili wa Y (Sakafu)", y)
        self.f_z = self.create_field("Pos Z", "Nafasi ya mhimili wa Z", z)
        
        self.f_px = self.create_field("Pivot X", "Bawaba: Kituo cha mzunguko X", "0.0")
        self.f_py = self.create_field("Pivot Y", "Bawaba: Kituo cha mzunguko Y", "0.0")
        self.f_pz = self.create_field("Pivot Z", "Bawaba: Kituo cha mzunguko Z", "0.0")
        
        self.f_axis = self.create_field("Mzunguko Axis", "Chagua mhimili (X/Y/Z)", "Y", readonly=True)
        self.f_axis.bind(on_touch_up=self.open_axis_menu)
        
        self.f_slide_axis = self.create_field("Mtembeo Axis", "Mwelekeo wa kuslide", "Y", readonly=True)
        self.f_slide_axis.bind(on_touch_up=self.open_slide_axis_menu)
        
        self.f_anim_type = self.create_field("Miondoko", "static/rotate/slide/both", "static", readonly=True)
        self.f_anim_type.bind(on_touch_up=self.open_anim_menu)
        
        self.f_speed = self.create_field("Speed", "Kasi ya kuslide (m/s)", "400")
        self.f_limit = self.create_field("Limit", "Umbali wa kuslide (m)", "800")
        
        self.f_ang_speed = self.create_field("Ang Speed", "Kasi ya kugeuka (deg/s)", "50.0")
        self.f_ang_limit = self.create_field("Ang Limit", "Ukomo wa kugeuka (deg)", "90.0")
        
        self.f_back_speed = self.create_field("Back Speed", "Kasi ya kuslide kurudi", "0.4")
        self.f_back_limit = self.create_field("Back Limit", "Ukomo wa kurudi (m)", "0.0")
        
        self.f_back_ang = self.create_field("Back Ang Speed", "Kasi ya kugeuka kurudi", "50.0")
        self.f_back_ang_limit = self.create_field("Back Ang Limit", "Ukomo wa kurudi (deg)", "0.0")
        
        self.f_t_start = self.create_field("Delay Start", "Muda kabla ya kuanza (sec)", "0.0")
        self.f_t_return = self.create_field("Delay Return", "Muda kabla ya kurudi (sec)", "2.0")
        
        self.f_loop = self.create_field("Loop Mode", "ping-pong/once", "ping-pong", readonly=True)
        self.f_loop.bind(on_touch_up=self.open_loop_menu)
        
        self.f_marudio = self.create_field("Marudio", "idadi", "0")
    
        self.f_marudio_axis = self.create_field("Mhimili wa marudio", "0,1 au 2", "0")

        self.f_marudio_interval = self.create_field("Umbali wa marudio", "Kila baada ya umbali gani", "1000")

        self.f_render = self.create_field("Chora", "Ssasisha mchoro", "0")

        self.f_loop.bind(on_touch_up=self.open_loop_menu)
        
        
        self.f_fl = self.create_field("Focal length", "Milimita", self.focal)
        self.f_cx = self.create_field("Camera X", "Milimita", f'{self.cam_x}')
        self.f_cy = self.create_field("Camera Y", "Milimita", f'{self.cam_y}')
        self.f_cz = self.create_field("Camera Z", "Milimita", f'{self.cam_z}')
        self.f_yaw = self.create_field("PITCH","Tuangalie juu au chini", f'{self.cam_rx}')
        self.f_ptch = self.create_field("YAW", "Tuangalie kushoto au kulia", f'{self.cam_ry}')
        
        
        self.f_color = self.create_field("Rangi", "Bado haijakamilika", x)
        self.f_sort = self.create_field("maboresho sorting", "0 au 1", 0)
        self.f_eneo = self.create_field("coat ", "Ujazo wa rangi", self.eneo_)
        self.f_speed = self.create_field("Speed", "Speed ya kamera",self.speed )
        

        # --- PANGA KWENYE LAYOUT ---
        all_fields = [
            self.f_id, self.f_parent, self.f_asili, self.f_wood, self.f_w, self.f_h, self.f_d,
            self.f_x, self.f_y, self.f_z, self.f_px, self.f_py, self.f_pz,
            self.f_axis, self.f_slide_axis, self.f_anim_type, self.f_speed,
            self.f_limit, self.f_ang_speed, self.f_ang_limit, self.f_back_speed,
            self.f_back_limit, self.f_back_ang, self.f_back_ang_limit,
            self.f_t_start, self.f_t_return, self.f_loop,
            self.f_marudio, self.f_marudio_axis, self.f_marudio_interval,
            self.f_render
        ]
        
        self.constantss=[
            self.f_fl,
            self.f_cx,
            self.f_cy ,
            self.f_cz ,
            self.f_yaw ,
            self.f_ptch,
            self.f_color,
            self.f_sort,
            self.f_eneo,
            self.f_speed
        ]
        for f in all_fields:
            self.workshop_layout.add_widget(f)

        v_gap = Window.height * 0.015
        h_pad = Window.width * 0.05
        self.constanti = MDBoxLayout(
            orientation="vertical", spacing=v_gap, 
            padding=[h_pad, v_gap, h_pad, Window.height * 0.15], 
            size_hint_y=None
        )
        self.constanti.bind(minimum_height=self.constanti.setter('height'))
        #print(self.constanti, self.painter.constantss)

        for f in self.constantss:
            try:
                try:
                    try:self.constanti.add_widget(f[0])
                    except:
                        f[0].parent.remove_widget(f[0])
                        self.constanti.add_widget(f[0])
                except:
                    try:self.constanti.add_widget(f)
                    except:
                        f.parent.remove_widget(f)
                        self.constanti.add_widget(f)
            except:self.update_status(f"{f}\n{traceback.format_exc()}",True)

        # Weka kwenye MDScrollView (72% ya kimo cha kioo)
        self.workshop_scroll = MDScrollView(
            size_hint=(1, None), 
            height=Window.height * 0.72, 
            do_scroll_x=False,
            scroll_timeout=500,
            #effect_cls='ScrollEffect'
        )
        self.workshop_scroll.add_widget(self.workshop_layout)
    # ==========================================
    # ⚙️ 3D ENGINE CORE (MATH & PHYSICS)
    # ==========================================

    def rotate_3d(self, x, y, z, rx, ry, rz):
        """Mzunguko wa vitu (Objects) - XYZ Order bila kupoteza unyama"""
        ax, ay, az = math.radians(rx), math.radians(ry), math.radians(rz)
        # Rotate X
        ty = y * math.cos(ax) - z * math.sin(ax)
        tz = y * math.sin(ax) + z * math.cos(ax)
        y, z = ty, tz
        # Rotate Y
        tx = x * math.cos(ay) + z * math.sin(ay)
        tz = -x * math.sin(ay) + z * math.cos(ay)
        x, z = tx, tz
        # Rotate Z
        tx = x * math.cos(az) - y * math.sin(az)
        ty = x * math.sin(az) + y * math.cos(az)
        return tx, ty, z


    def project(self, x, y, z):
        """Master Projector: Inazungusha Dunia na Jicho, inafanya Y-Inversion ya Tkinter"""
        try:
            cx, cy, cz = float(self.cam_x), float(self.cam_y), float(self.cam_z)
            f_val = float(self.focal)
            
            # 1. TRANSLATION (Relative to Camera)
            tx, ty, tz = x - cx, y - cy, z - cz

            # 2. WORLD ROTATION (Orbit Mode ya Dunia)
            w_ay = math.radians(float(self.world_rot_y))
            wx = tx * math.cos(w_ay) + tz * math.sin(w_ay)
            wz = -tx * math.sin(w_ay) + tz * math.cos(w_ay)
            tx, tz = wx, wz

            w_ax = math.radians(float(self.world_rot_x))
            wy = ty * math.cos(w_ax) - tz * math.sin(w_ax)
            wz = ty * math.sin(w_ax) + tz * math.cos(w_ax)
            ty, tz = wy, wz

            # 3. CAMERA ROTATION (Yaw na Pitch za Jicho)
            ay = math.radians(-float(self.cam_ry))
            rx_y = tx * math.cos(ay) + tz * math.sin(ay)
            rz_y = -tx * math.sin(ay) + tz * math.cos(ay)
            
            ax = math.radians(-float(self.cam_rx))
            ry_f = ty * math.cos(ax) - rz_y * math.sin(ax)
            rz_f = ty * math.sin(ax) + rz_y * math.cos(ax)

            # Near Plane Guard
            if rz_f < 0.1: return None 
            
            # 4. SCREEN MAPPING (Dawa ya Chini-Kushoto vs Juu-Kushoto)
            px = (rx_y * f_val / rz_f) + (self.width / 2.0)
            py = (self.height * 0) + (ry_f * f_val / rz_f) # Hapa imebadilika kuwa '-' ya Tkinter!
            
            return px, py
        except:
            return None

    def project(self, x, y, z):
        """Master Projector: Imenyoshwa kwa ajili ya Kivy bila weaver complications"""
        try:
            cx, cy, cz = float(self.cam_x), float(self.cam_y), float(self.cam_z)
            f_val = float(self.focal)
            
            # 1. TRANSLATION (Relative to Camera)
            tx, ty, tz = x - cx, y - cy, -z - cz

            # 2. WORLD ROTATION (Orbit Mode ya Dunia)
            w_ay = math.radians(float(self.world_rot_y))
            wx = tx * math.cos(w_ay) + tz * math.sin(w_ay)
            wz = -tx * math.sin(w_ay) + tz * math.cos(w_ay)
            tx, tz = wx, wz

            w_ax = math.radians(float(self.world_rot_x))
            wy = ty * math.cos(w_ax) - tz * math.sin(w_ax)
            wz = ty * math.sin(w_ax) + tz * math.cos(w_ax)
            ty, tz = wy, wz

            # 3. CAMERA ROTATION (Yaw na Pitch za Jicho)
            ay = math.radians(-float(self.cam_ry))
            rx_y = tx * math.cos(ay) + tz * math.sin(ay)
            rz_y = -tx * math.sin(ay) + tz * math.cos(ay)
            
            ax = math.radians(-float(self.cam_rx))
            ry_f = ty * math.cos(ax) - rz_y * math.sin(ax)
            rz_f = ty * math.sin(ax) + rz_y * math.cos(ax)

            # 🔥 FIX 1: Kama kitu kiko upande wa hasi wa Z kulingana na cam_z = -4125,
            # weka hesabu isikatae pointi (Near Plane Guard Optimization)
            #if abs(rz_f) < 0.1: return None 
            
            # 4. SCREEN MAPPING (Dawa ya Kivy Center Offset)
            px = (rx_y * f_val / rz_f) + (self.width / 2.0)
            
            # 🔥 FIX 2: Badala ya Tkinter ya (self.height * 2/3) iliyokuwa inatupa vitu chini ya kioo,
            # weka mfumo wa Kivy wa kwenda juu (+ nusu ya screen) ili mchoro utokee katikati!
            py = (self.height * 0.75) + (ry_f * f_val / rz_f)
            
            return px, py
        except:
            return None


    def smam_3vp_solver(self, obj_pos, obj_dim, obj_rot=0.0):
        """
        Smam-3VP Solver (Ultimate Eye-Centric Edition)
        Nafasi na orientation ya jicho ndio reference ya kila kitu.
        Inafanya kazi hata uwanja urotate au jicho lihame axis yoyote.
        """
        try:
            # 1. DATA PARSING
            cx, cy, cz = float(self.cam_x), float(self.cam_y), float(self.cam_z)
            ox, oy, oz = [float(n) for n in obj_pos]
            w, h, d = [float(n) for n in obj_dim]
            
            # 2. VECTOR TO EYE (Miale kutoka kitu kwenda jichoni)
            dx, dy, dz = cx - ox, cy - oy, cz - oz

            # 3. WORLD ORBIT COMPENSATION (Zungusha Jicho kulingana na Uwanja)
            # Y-Axis (Yaw)
            w_ay = math.radians(float(self.world_rot_y))
            wx = dx * math.cos(w_ay) + dz * math.sin(w_ay)
            wz = -dx * math.sin(w_ay) + dz * math.cos(w_ay)
            
            # X-Axis (Pitch)
            w_ax = math.radians(float(self.world_rot_x))
            wy = dy * math.cos(w_ax) - wz * math.sin(w_ax)
            wz = dy * math.sin(w_ax) + wz * math.cos(w_ax)

            # 4. LOCAL OBJECT ROTATION (Zungusha Jicho kulingana na Mbao)
            # Hapa tunatumia 'obj_rot' kumuweka observer kwenye coordinate ya mbao
            obj_a = math.radians(obj_rot)
            local_x = wx * math.cos(-obj_a) - wz * math.sin(-obj_a)
            local_z = wx * math.sin(-obj_a) + wz * math.cos(-obj_a)
            local_y = wy # Vertical position

            visible = []

            # 5. PERSPECTIVE-CORRECT DECISION LOGIC
            # Tunatumia thresholds za kijiometri (Bounding Box boundaries)
            # Mbele (0) / Nyuma (1)
            if local_z < (d / 2.0): 
                visible.append(0)
            elif local_z > -(d / 2.0): 
                visible.append(1)

            # Kulia (2) / Kushoto (3)
            if local_x < (w / 2.0): 
                visible.append(2)
            elif local_x > -(w / 2.0): 
                visible.append(3)

            # Juu (4) / Chini (5)
            # Tunatumia kimo cha mbao (h) kama reference ya juu
            if local_y > h: 
                visible.append(4)
            elif local_y < 0: 
                visible.append(5)

            # 6. FAIL-SAFE (Usiruhusu kioo kiwe kitupu)
            if not visible: 
                visible = [0] # Default on mbele
                
            return visible, "Eye-Reference-Verified"

        except Exception as e:
            self.update_status(f"SolverErr: {traceback.format_exc()}",is_error=True)
            return [0], "Err"

    def internal_draw(self, obj, v_u, f_map, eye_3vp):
        """Logic yako ya asili: Adaptive Sorting, Shading & Hit-Box"""
        try:
            dim, pos = [float(n) for n in obj['dim']], [float(n) for n in obj['pos']]
            w, h, d, ox, oy, oz = dim[0], dim[1], dim[2], pos[0], pos[1], pos[2]
            piv = [float(n) for n in obj.get('pivot', [0,0,0])]
            a, base_color = obj.get("anim", {}), obj.get("color", [0.8, 0.8, 0.8, 1])
            val, ang = float(a.get("val", 0.0)), float(a.get("ang_val", 0.0)) % 360
            s_vec = [float(n) for n in obj.get("slide_vec", [0,0,0])]
            cx, cy, cz = eye_3vp['pos']
            
            obj['hit_area'] = []
            
            # Solver & Sorting (Logic yako kali uliyoiandika)
            indices, _ = self.smam_3vp_solver(pos, dim, ang)
            f_normals = [(0,0,1), (0,0,-1), (1,0,0), (-1,0,0), (0,1,0), (0,-1,0)]
            f_midpoints = [(0,0.5,0.5),(0,0.5,-0.5),(0.5,0.5,0),(-0.5,0.5,0),(0,1,0),(0,0,0)]
            
            face_prio = []
            for f_idx in indices:
                mx, my, mz = f_midpoints[f_idx]
                lx, ly, lz = (mx-0.5)*w - piv[0], my*h - piv[1], (mz-0.5)*d - piv[2]
                # Hapa ndipo nguvu yako ya rotation ilipo
                cos_a, sin_a = math.cos(math.radians(ang)), math.sin(math.radians(ang))
                rx = lx * cos_a - lz * sin_a
                rz = lx * sin_a + lz * cos_a
                wx, wy, wz = rx + ox + piv[0] + (val*s_vec[0]), ly + oy + piv[1] + (val*s_vec[1]), rz + oz + piv[2] + (val*s_vec[2])
                ray_dist = math.sqrt((wx-cx)**2 + (wy-cy)**2 + (wz-cz)**2)
                face_prio.append({'idx': f_idx, 'n': f_normals[f_idx], 'dist': ray_dist})

            face_prio.sort(key=lambda x: x['dist'], reverse=True)

            from kivy.graphics import Color, Mesh, Line
            with self.canvas:
                for f_data in face_prio:
                    f_idx, n_v = f_data['idx'], f_data['n']
                    pts = []
                    for i in f_map[f_idx]:
                        vx, vy, vz = (v_u[i][0]-0.5)*w - piv[0], v_u[i][1]*h - piv[1], (v_u[i][2]-0.5)*d - piv[2]
                        rx_v = vx * cos_a - vz * sin_a
                        rz_v = vx * sin_a + vz * cos_a
                        p = self.project(rx_v+ox+piv[0]+(val*s_vec[0]), vy+oy+piv[1]+(val*s_vec[1]), rz_v+oz+piv[2]+(val*s_vec[2]))
                        if p: pts.append(p)
                    
                    if len(pts) >= 3:
                        obj['hit_area'].append(pts)
                        v_l = []
                        for pt in pts: v_l.extend([float(pt[0]), float(pt[1]), 0, 0])
                        shade = 0.4 + (abs(n_v[0])*0.2) + (abs(n_v[1])*0.4) + (abs(n_v[2])*0.1)
                        Color(*[(base_color[j]*shade) for j in range(3)], 1.0)
                        idx_l = [0, 1, 2, 2, 3, 0] if len(pts)==4 else [0, 1, 2]
                        Mesh(vertices=v_l, indices=idx_l, mode="triangles")
                        
                        Color(0,0,0, 0.1)
                        Line(points=[c for p in pts for c in p] + [pts[0][0], pts[0][1]], width=1)
            return obj.get('id')
        except Exception as e:
           self.update_status(f"DrawErr:{traceback.format_exc()}",is_error=True)


    def internal_draw(self, obj, screen_pts):
        """
        Ultra-Performance Render: Inachukua amri ya Kanda 9 
        na kuipusha moja kwa moja kwenye GPU bila lag (No Ghosting)
        """
        try:
            # 1. Pata rangi na vigezo vya ubao
            base_color = obj.get("color", [0.8, 0.4, 0.2, 1])
            
            # 2. PIGA HAFU YA KANDA 9 ON THE SPOT (Tkinter Concept)
            # Inarudisha mfuatano wa face pekee (Mfano: [5, 3, 0])
            chora_order = self.smam_9zone_perspective_solver(obj, screen_pts)
            
            # Ramani ya vertices za nyuso 6 za mbao (Zilizotoka kwenye project())
            # Kila face ina index 4 za pembe zake
            faces_map = {
                0: [0, 1, 2, 3],  # Mbele
                1: [4, 5, 6, 7],  # Nyuma
                2: [0, 4, 7, 3],  # Kushoto
                3: [1, 5, 6, 2],  # Kulia
                4: [3, 2, 6, 7],  # Juu
                5: [0, 1, 5, 4]   # Chini
            }
            
            # Shading ya asili (Dawa yako ya kutoa mistari migumu)
            shade_factors = {0: 1.0, 4: 0.85, 2: 0.70, 3: 0.70, 1: 0.50, 5: 0.40}

            from kivy.graphics import Color, Mesh
            
            # Tunafungua canvas instruction moja tu ya chuma
            with self.canvas:
                for face_idx in chora_order:
                    indices = faces_map[face_idx]
                    s_factor = shade_factors.get(face_idx, 0.8)
                    
                    # Badili rangi kulingana na shading ya ukanda
                    Color(*[(c * s_factor) for c in base_color[:3]], base_color[3])
                    
                    # Kusanya pointi 4 za 2D screen zilizopigwa inversion ya Y-axis
                    v_list = []
                    for idx in indices:
                        px, py = screen_pts[idx]
                        v_list.extend([float(px), float(py), 0.0, 0.0]) # Vertex array format
                        
                    # Triangle Fan: Inachora mstatili wa uso kwa herufi (GPU Accelerated)
                    i_list = [0, 1, 2, 2, 3, 0]
                    Mesh(vertices=v_list, indices=i_list, mode="triangles")
                    
            return True
        except Exception as e:
            self.update_status(f"Instant Render Error: {traceback.format_exc()}",is_error=True)
            return False

    def smam_solid_subtraction_engine(self):
        """
        METHOD 1: Injini ya Chuma (CSG). Inakata mbao zilizochomekana.
        Inaitwa mara moja tu baada ya ujenzi au uhariri (Zero Lag during animation).
        """
        try:
            precision = self.precision
            for i, obj_A in enumerate(self.scene_objects):
                if not obj_A.get('visible', True): continue
                w_A, h_A, d_A = obj_A['dim'][0], obj_A['dim'][1], obj_A['dim'][2]
                x_A, y_A, z_A = obj_A['pos'][0], obj_A['pos'][1], obj_A['pos'][2]

                for j, obj_B in enumerate(self.scene_objects):
                    if i == j or not obj_B.get('visible', True): continue
                    w_B, h_B, d_B = obj_B['dim'][0], obj_B['dim'][1], obj_B['dim'][2]
                    x_B, y_B, z_B = obj_B['pos'][0], obj_B['pos'][1], obj_B['pos'][2]

                    # ⚙️ SENSA: Kagua kama mbao zimechomekana pande zote (AABB Overlap)
                    gongana_x = abs(x_A - x_B) < (w_A / 2.0 + w_B / 2.0) - precision
                    gongana_y = (y_A < y_B + h_B - precision) and (y_A + h_A > y_B + precision)
                    gongana_z = abs(z_A - z_B) < (d_A / 2.0 + d_B / 2.0) - precision

                    if gongana_x and gongana_y and gongana_z:
                        # Akili ya uamuzi: Mbao mama (Parent) au yenye ID ndogo inakata nyingine
                        if obj_A.get('parent') == obj_B['id'] or obj_A['id'] < obj_B['id']:
                            
                            # A. Kata Upana (X-Axis)
                            if x_B > x_A and (x_A + w_A/2.0) > (x_B - w_B/2.0):
                                overlap_x = (x_A + w_A/2.0) - (x_B - w_B/2.0)
                                obj_B['dim'][0] = max(0.01, w_B - overlap_x)
                                obj_B['pos'][0] = x_B + (overlap_x / 2.0)
                            elif x_A > x_B and (x_B + w_B/2.0) > (x_A - w_A/2.0):
                                overlap_x = (x_B + w_B/2.0) - (x_A - w_A/2.0)
                                obj_B['dim'][0] = max(0.01, w_B - overlap_x)
                                obj_B['pos'][0] = x_B - (overlap_x / 2.0)

                            # B. Kata Kimo/Urefu (Y-Axis)
                            if y_B > y_A and (y_A + h_A) > y_B:
                                overlap_y = (y_A + h_A) - y_B
                                obj_B['dim'][1] = max(0.01, h_B - overlap_y)
                                obj_B['pos'][1] = y_B + overlap_y

                            # C. Kata Unene (Z-Axis)
                            if z_B > z_A and (z_A + d_A/2.0) > (z_B - d_B/2.0):
                                overlap_z = (z_A + d_A/2.0) - (z_B - d_B/2.0)
                                obj_B['dim'][2] = max(0.01, d_B - overlap_z)
                                obj_B['pos'][2] = z_B + (overlap_z / 2.0)
            return True
        except Exception as e:
            self.update_status(f"CSG Error: {traceback.format_exc()}",is_error=True)
            return False




    def draw_cast_shadow(self, obj, v_u, f_map):
        """Shadow Logic yako ya asili"""
        try:
            ground_y = -1.49 
            dim = [float(x) for x in obj.get('dim', [0.6, 2.0, 0.02])]
            pos = [float(x) for x in obj.get('pos', [0, -1.45, 0])]
            piv = [float(x) for x in obj.get('pivot', [0, 0, 0])]
            w, h, d, ox, oy, oz, px, py, pz = dim[0], dim[1], dim[2], pos[0], pos[1], pos[2], piv[0], piv[1], piv[2]
            
            a = obj.get("anim", {})
            val, ang = float(a.get("val", 0.0)), float(a.get("ang_val", 0.0)) % 360
            s_vec = obj.get("slide_vec", [0, 0, 1])

            with self.canvas:
                from kivy.graphics import Color, Mesh
                Color(0, 0, 0, 0.15)
                for face in f_map:
                    s_pts = []
                    for i in face:
                        vx, vy, vz = (v_u[i][0]-0.5)*w - px, v_u[i][1]*h - py, (v_u[i][2]-0.5)*d - pz
                        cos_a, sin_a = math.cos(math.radians(ang)), math.sin(math.radians(ang))
                        rx = vx * cos_a - vz * sin_a
                        rz = vx * sin_a + vz * cos_a
                        tx = rx + ox + px + (val * s_vec[0])
                        tz = rz + oz + pz + (val * s_vec[2])
                        p = self.project(tx, ground_y, tz)
                        if p: s_pts.append(p)
                    
                    if len(s_pts) >= 3:
                        v_l = []
                        for pt in s_pts: v_l.extend([pt[0], pt[1], 0, 0])
                        idx_l = [0, 1, 2, 2, 3, 0] if len(s_pts) == 4 else [0, 1, 2]
                        Mesh(vertices=v_l, indices=idx_l, mode="triangles")
        except: pass
    def draw_single_face(self, obj, f_idx):
        """Uchoraji wa BIM: Rangi tupu, No Lines, na Jina la Uso kitalamu"""
        try:
            from kivy.graphics import Color, Mesh
            v_u = [(-0.5,0,-0.5),(0.5,0,-0.5),(0.5,1,-0.5),(-0.5,1,-0.5),
                   (-0.5,0,0.5),(0.5,0,0.5),(0.5,1,0.5),(-0.5,1,0.5)]
            f_map = [(0,1,2,3),(4,5,6,7),(0,4,7,3),(1,5,6,2),(3,2,6,7),(0,1,5,4)]
            
            # --- DAWA YA MAJINA YA NYUSO ---
            f_names = ["Mbele", "Nyuma", "Kushoto", "Kulia", "Juu", "Chini"]
            obj_id = obj.get('id', 'M1')
            full_face_id = f"{obj_id}_{f_names[f_idx]}"

            dim = [float(n) for n in obj.get('dim', [600, 2000, 300])]
            pos = [float(n) for n in obj.get('pos', [0, -1450, 0])]
            piv = [float(n) for n in obj.get('pivot', [0,0,0])]
            
            a = obj.get("anim", {})
            val, ang = float(a.get("val", 0.0)), math.radians(float(a.get("ang_val", 0.0)))
            s_vec = [float(n) for n in obj.get("slide_vec", [0,0,0])]
            base_color = obj.get("color", [0.8, 0.8, 0.8, 1])
            
            pts = []
            for i in f_map[f_idx]:
                vx, vy, vz = (v_u[i][0])*dim[0]-piv[0], (v_u[i][1])*dim[1]-piv[1], (v_u[i][2])*dim[2]-piv[2]
                rx = vx * math.cos(ang) - vz * math.sin(ang)
                rz = vx * math.sin(ang) + vz * math.cos(ang)
                wx, wy, wz = rx + pos[0] + piv[0] + (val * s_vec[0]), vy + pos[1] + piv[1] + (val * s_vec[1]), rz + pos[2] + piv[2] + (val * s_vec[2])
                
                p = self.project(wx, wy, wz)
                if p: pts.append(p)
                else: return None

            if len(pts) >= 3:
                if 'hit_area' not in obj: obj['hit_area'] = []
                # Tunahifadhi face_id ili ukigusa ijulikane ni upande gani
                obj['hit_area'].append({'pts': pts, 'f_idx': f_idx, 'face_id': full_face_id})

                # Shading (Dawa ya kutofautisha pembeni na mbele bila lines)
                shade_map = {0: 1.0, 4: 0.9, 2: 0.75, 3: 0.75, 1: 0.5, 5: 0.4}
                s_factor = shade_map.get(f_idx, 0.8)
                Color(*[(c * s_factor) for c in base_color[:3]], base_color[3])
                
                v_list = []
                for pt in pts: v_list.extend([float(pt[0]), float(pt[1]), 0.0, 0.0])
                i_list = [0, 1, 2, 2, 3, 0] if len(pts) == 4 else [0, 1, 2]
                Mesh(vertices=v_list, indices=i_list, mode="triangles")
                
                # Rudisha jina la kipekee la uso
                return full_face_id
            return None
        except: return None

    def smam_radial_sorter(self, obj):
        """
        Radial Sorter: Inachambua plane zote (x,y,z) radialy.
        Inahakikisha dominance ya kweli kulingana na miale ya jicho.
        """
        try:
            cx, cy, cz = float(self.cam_x), float(self.cam_y), float(self.cam_z)
            # Pata Position na Dimension
            o_pos = obj.get('pos', [0, -1.45, 0])
            o_dim = obj.get('dim', [0.6, 2.0, 0.3])
            ox, oy, oz = [float(n) for n in o_pos]
            ow, oh, od = [float(n) for n in o_dim]
            
            # 1. TAFUTA CENTER YA OBJECT (Geometric Midpoint)
            mid_x, mid_y, mid_z = ox, oy + (oh / 2.0), oz

            # 2. RELATIVE DISPLACEMENT (Translation)
            dx, dy, dz = mid_x - cx, mid_y - cy, mid_z - cz

            # 3. 3-PLANE ORBIT SYNC (Matrix Rotation)
            # Y-Axis (Yaw)
            w_ay = math.radians(float(self.world_rot_y))
            wx = dx * math.cos(w_ay) + dz * math.sin(w_ay)
            wz = -dx * math.sin(w_ay) + dz * math.cos(w_ay)
            
            # X-Axis (Pitch)
            w_ax = math.radians(float(self.world_rot_x))
            wy = dy * math.cos(w_ax) - wz * math.sin(w_ax)
            wz = dy * math.sin(w_ax) + wz * math.cos(w_ax)

            # 4. FINAL RADIAL MAGNITUDE (Pythagoras)
            # Hapa ndipo tunapata 'The Dominant Distance'
            radial_dist = math.sqrt(wx**2 + wy**2 + wz**2)
            
            # 5. Z-FIGHTING BIAS (Kinga ya vitu vilivyo bapa/karibu)
            # Tunapunguza bias kidogo kulingana na unene wa object
            return radial_dist - (float(obj.get('id', '0')[-1:]) * 0.0001 if obj.get('id') else 0)

        except:
            return 999.0 # Ipeleke mbali kama kuna kosa


    def draw_all_shadows(self):
        """Injini ya Chuma: Inafuta vivuli vya zamani na kuchora vipya bila Ghosting"""
        try:
            from kivy.graphics import Color, Mesh
            
            # 1. SAFISHA KIKUNDI CHA ZAMANI (Dawa ya Ghosting)
            self.shadow_layer.clear()
            
            # 2. HESABU JUA (Angle ya 180 deg)
            muda = float(getattr(self, 'light_y', 5.0)) # 5.0 ni saa sita mchana
            angle = math.pi * (muda / 10.0)
            
            sun_x = math.cos(angle) * 5.0
            sun_y = math.sin(angle) * 5.0
            sun_z = float(getattr(self, 'light_z', 0.5))
            if sun_y < 0.1: sun_y = 0.1

            # Rangi moja ya kivuli kwa group zima
            self.shadow_layer.add(Color(0, 0, 0, 0.25))

            v_u = [(-0.5,0,-0.5),(0.5,0,-0.5),(0.5,1,-0.5),(-0.5,1,-0.5),
                   (-0.5,0,0.5),(0.5,0,0.5),(0.5,1,0.5),(-0.5,1,0.5)]
            f_map = [(0,1,2,3),(4,5,6,7),(0,4,7,3),(1,5,6,2),(3,2,6,7),(0,1,5,4)]

            for obj in self.scene_objects:
                if not obj.get('visible', True): continue
                dim, pos, piv = obj['dim'], obj['pos'], obj.get('pivot',)
                ang = math.radians(obj.get('anim', {}).get('ang_val', 0.0))

                for f_idx in [0, 4, 2, 3]: # Mbele, Juu, Kulia, Kushoto
                    s_pts = []
                    for i in f_map[f_idx]:
                        # A. Pointi ya mbao
                        vx, vy, vz = (v_u[i][0])*dim[0]-piv[0], (v_u[i][1])*dim[1]-piv[1], (v_u[i][2])*dim[2]-piv[2]
                        rx = vx * math.cos(ang) - vz * math.sin(ang)
                        rz = vx * math.sin(ang) + vz * math.cos(ang)
                        wx, wy, wz = rx + pos[0] + piv[0], vy + pos[1] + piv[1], rz + pos[2] + piv[2]

                        # B. COLLISION (Kivuli juu ya mbao nyingine)
                        target_y = -1.45
                        for other in self.scene_objects:
                            if other['id'] == obj['id']: continue
                            o_p, o_d = other['pos'], other['dim']
                            # Piga chabo kama mbao nyingine ipo chini ya mionzi hii
                            if (o_p[0]-o_d[0]/2 < wx < o_p[0]+o_d[0]/2) and \
                               (o_p[2]-o_d[2]/2 < wz < o_p[2]+o_d[2]/2):
                                if (o_p[1] + o_d[1]) < wy:
                                    target_y = max(target_y, o_p[1] + o_d[1] + 0.002)

                        # C. PROJECTION
                        ratio = (wy - target_y) / sun_y
                        sx, sz = wx - (sun_x * ratio), wz - (sun_z * ratio)
                        
                        p = self.project(sx, target_y, sz)
                        if p: s_pts.append(p)

                    if len(s_pts) >= 3:
                        v_l = []
                        for pt in s_pts: v_l.extend([float(pt[0]), float(pt[1]), 0, 0])
                        i_l = [0, 1, 2, 2, 3, 0] if len(s_pts) == 4 else [0, 1, 2]
                        # Ongeza kwenye layer yetu
                        self.shadow_layer.add(Mesh(vertices=v_l, indices=i_l, mode="triangles"))

            # 3. ONGEZA LAYER KWENYE CANVAS (Kama haipo tayari)
            if self.shadow_layer not in self.canvas.children:
                self.canvas.add(self.shadow_layer)
                
        except Exception as e: self.update_status(f"Shadow Error: {traceback.format_exc()}",is_error=True)



    def smam_occlusion_clipping(self, face_midpoint, other_obj):
        """
        Eclipse Occlusion:
        Inachunguza kama miale ya jicho inaweza kuona hii point 
        au kama imezikwa ndani ya object nyingine (Immersed).
        """
        try:
            # 1. Pata Mipaka ya Object ya pili (The Occluder)
            o_pos = other_obj.get('pos', [0,0,0])
            o_dim = other_obj.get('dim', [0,0,0])
            o_ang = math.radians(float(other_obj.get('anim', {}).get('ang_val', 0.0)))
            
            # 2. Hamisha face_midpoint kwenda kwenye 'Local Space' ya Object ya pili
            # Hii ni muhimu ili tujue kama point ipo 'ndani' ya box lake
            dx, dy, dz = face_midpoint[0] - o_pos[0], face_midpoint[1] - o_pos[1], face_midpoint[2] - o_pos[2]
            
            # Reverse Rotation (Kufidia mzunguko wa object ya pili)
            lx = dx * math.cos(-o_ang) - dz * math.sin(-o_ang)
            lz = dx * math.sin(-o_ang) + dz * math.cos(-o_ang)
            ly = dy

            # 3. CHECK KAMA POINT IPO NDANI (Immersed Check)
            # Tunatumia nusu ya dimensions (Half-extents)
            hw, hh, hd = o_dim[0]/2.0, o_dim[1]/2.0, o_dim[2]/2.0
            
            # Kama point ipo ndani ya box kwa plane zote x, y, z
            if (-hw < lx < hw) and (0 < ly < o_dim[1]) and (-hd < lz < hd):
                return True # Point imezikwa (Immersed)
                
            return False # Point inaonekana
        except:
            return False




    def run_engine_cycle(self, dt):
        if not self.is_constructed: return
        needs_render = False

        for obj in self.scene_objects:
            a = obj.get("anim", {})
            if not a or a.get("type") == "static": continue

            # 1. TIMERS (Pausing)
            state = a.get("state", "opening")
            if "paused" in state:
                a["timer"] = a.get("timer", 0) + dt
                t_limit = 2.0 if state == "paused_open" else 0.5 # Muda wa kusubiri
                if a["timer"] >= t_limit:
                    a["state"] = "closing" if state == "paused_open" else "opening"
                    a["timer"] = 0
                continue

            # 2. DATA (Safisha kila kitu kiwe namba)
            def to_f(v, d):
                if isinstance(v, list): return float(v[0]) if v else d
                try: return float(v)
                except: return d

            limit = to_f(a.get("limit"), 0.8)
            ang_limit = to_f(a.get("ang_limit"), 90.0)
            spd = to_f(a.get("spd"), 0.4)
            
            # 3. HARAKATI (Direct Steps)
            needs_render = True
            direction = 1 if state == "opening" else -1
            
            # Step ya mzunguko (Rotate) - Tunaitumia kulingana na kasi ya spd
            # Tunahakikisha r_step inafuata ang_limit kwa uaminifu
            r_step = (ang_limit * (spd / limit if limit > 0 else 1)) * dt * direction
            v_step = spd * dt * direction

            # 4. EXECUTION (The Hard Clamp)
            # Slide
            if a["type"] in ["slide", "both"]:
                val = to_f(a.get("val"), 0.0) + v_step
                a["val"] = max(0.0, min(val, limit))
            else: a["val"] = 0.0

            # Rotate
            if a["type"] in ["rotate", "both"]:
                # Kama ni rotate pekee, kasi iwe spd ya kawaida
                if a["type"] == "rotate": r_step = (ang_limit * 0.5) * dt * direction
                
                ang = to_f(a.get("ang_val"), 0.0) + r_step
                a["ang_val"] = max(0.0, min(ang, ang_limit))
            else: a["ang_val"] = 0.0

            # 5. THE TOGGLE (Dawa ya kero)
            if state == "opening":
                # Ikishagusa ukuta wowote, pause!
                if (a["val"] >= limit) or (a["ang_val"] >= ang_limit):
                    a["state"], a["timer"] = "paused_open", 0
            else: # closing
                if (a["val"] <= 0) and (a["ang_val"] <= 0):
                    a["state"], a["timer"] = "paused_closed", 0

        if needs_render:
            Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)
    # --- METHODS ZA NYONGEZA ZA ENGINE ---

    def run_engine_cycle(self, dt):
        """
        MZUNGUKO MKUU WA FIZIKA: Unasimamia Velocity (Kasi), 
        Mhimili wa Mzunguko, na Timers za mbao zote uwanjani mara 30 kwa sekunde.
        """
        if not self.is_constructed: return
        needs_render = False

        for obj in self.scene_objects:
            a = obj.get("anim", {})
            # Kama mbao haina animation au ni static, iruke isiingie kwenye mzigo wa hesabu
            if not a or a.get("type") == "static": continue

            state = a.get("state", "paused_closed")
            
            # =====================================================================
            # 1. ⏱️ USIMAMIZI WA TIMERS (Delay Start na Delay Return)
            # =====================================================================
            if "paused" in state:
                a["timer"] = a.get("timer", 0.0) + dt
                
                # Soma muda wa kuchelewa kutoka kwenye Workshop Form yako
                if state == "paused_open":
                    t_limit = float(a.get("time_before_return", 2.0))
                else:  # paused_closed
                    t_limit = float(a.get("time_before_start", 0.0))
                
                # Muda ukitimia, geuza mwelekeo wa mbao kitalamu
                if a["timer"] >= t_limit:
                    a["state"] = "closing" if state == "paused_open" else "opening"
                    a["timer"] = 0.0
                continue

            # =====================================================================
            # 2. 🧮 VUTA SEQUENCE YA MIONDOKO (Opening vs Closing Steps Chains)
            # =====================================================================
            # Inasoma mnyororo uliouandika kuzuia ubao usiyumbe mwelekeo
            steps = a.get("opening_steps", []) if state == "opening" else a.get("closing_steps", [])
            if not steps:
                # Fallback ya chuma kama mtumiaji hakuweka step kwenye fomu
                steps = [{
                    'spd': float(a.get('spd', 0.4)), 'limit': float(a.get('limit', 0.8)),
                    'ang_spd': float(a.get('ang_spd', 50.0)), 'ang_limit': float(a.get('ang_limit', 90.0))
                }]

            # Kila mara soma hatua ya kwanza inayoratibiwa kwa sasa
            step = steps[0]
            limit = float(step.get('limit', 0.8))
            ang_limit = float(step.get('ang_limit', 90.0))
            spd = float(step.get('spd', 0.4))
            ang_spd = float(step.get('ang_spd', 50.0))

            direction = 1.0 if state == "opening" else -1.0
            needs_render = True

            # =====================================================================
            # 3. 🚀 UPIGAJI HESABU WA VELOCITY (Mtembeo wa Slide)
            # =====================================================================
            if a["type"] in ["slide", "both"]:
                v_step = spd * dt * direction
                val = float(a.get("val", 0.0)) + v_step
                # The Hard Clamp: Zuia mbao isivuke ukomo wa limit ya Workshop
                a["val"] = max(0.0, min(val, limit)) 
            else:
                a["val"] = 0.0

            # =====================================================================
            # 4. 🔄 UPIGAJI HESABU WA ROTATION (Mzunguko wa Nyuzi)
            # =====================================================================
            if a["type"] in ["rotate", "both"]:
                r_step = ang_spd * dt * direction
                ang = float(a.get("ang_val", 0.0)) + r_step
                # Zuia mbao isizunguke sarakasi kupita kiasi
                a["ang_val"] = max(0.0, min(ang, ang_limit))
            else:
                a["ang_val"] = 0.0

            # =====================================================================
            # 5. 🔀 THE TOGGLE: DAWA YA KERO (Mwelekeo wa Loop Mode)
            # =====================================================================
            cur_val = float(a.get("val", 0.0))
            cur_ang = float(a.get("ang_val", 0.0))
            loop_mode = a.get("loop_mode", "ping-pong")

            if state == "opening":
                # Kama ubao umefunguka kabisa ukagonga mwisho wa reli/limit
                if (a["type"] in ["slide", "both"] and cur_val >= limit) or \
                   (a["type"] in ["rotate", "both"] and cur_ang >= ang_limit):
                    if loop_mode == "ping-pong":
                        a["state"] = "paused_open"  # Subiri sekunde chache kabla ya kufunga yenyewe
                    else:
                        a["state"] = "paused_open"  # Mode ya 'once': baki wazi hadi mtumiaji akuguse tena
                    a["timer"] = 0.0
                    
            elif state == "closing":
                # Kama ubao umefunga kabisa ukarudi kwenye nafasi ya asili (0.0)
                if (a["type"] in ["slide", "both"] and cur_val <= 0.0) or \
                   (a["type"] in ["rotate", "both"] and cur_ang <= 0.0):
                    if loop_mode == "ping-pong":
                        a["state"] = "paused_closed" # Subiri sekunde chache ufunguke tena
                    else:
                        a["state"] = "paused_closed"
                    a["timer"] = 0.0

        # --- 6. LAZIMISHA UCHORAJI WA FRAME MPYA ---
        # Kama kuna ubao hata mmoja unatembea uwanjani, itwange render on-the-spot
        if needs_render:
            Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)









        # Injection ya ubao wa kwanza wa jaribio (Weka chini ya Clock uliyoongeza hapo juu)


    def draw_floating_labels(self):
        """Inachora majina yanayoelea (oy + 1.2) - No DP"""
        from kivy.graphics import Color, Rectangle
        from kivy.core.text import Label as CoreLabel
        for obj in self.scene_objects:
            p = [float(n) for n in obj.get('pos', [0,0,0])]
            p_2d = self.project(p[0], p[1] + 1.2, p[2])
            if p_2d:
                label = CoreLabel(text=str(obj.get('id', 'M1')), font_size=Window.height*0.01, bold=True)
                label.refresh(); tex = label.texture
                with self.canvas:
                    Color(1, 1, 1, 0.8)
                    Rectangle(texture=tex, pos=(p_2d[0] - tex.width/2, p_2d[1]), size=tex.size)




    def _preload_catalog(self, dt):
        """Inapakia mbao mapema kuzuia lag"""
        try:
            self.cached_menu_items = [{"text": str(m), "on_release": lambda c, x=str(m): self.set_wood(x)} 
                                      for m in BONGO_WOOD_CATALOG.keys()]
        except: pass

    def set_wood(self, jina):
        self.f_wood.text = jina
        self.m_wood.dismiss()#if hasattr(self, 'm_wood'): 
        #self.update_status(f"Vifaa: {jina} vimepakiwa.")

    def toggle_labels(self, *args):
        """Inawasha au kuzima majina ya mbao uwanjani"""
        from kivy.app import App
        app=App.get_running_app()
        
        self.show_labels = not self.show_labels
        Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)
        hali = "Zimeonekana" if self.show_labels else "Zimefichwa"
        self.update_status(f"Camera_man wetu {random.choice(app.fundi)} ame_move mpaka >>> Mahali: ({round(self.cam_x,0),round(self.cam_y,0),round(self.cam_z)}) | Uelekeo: ({round(self.cam_rx, 0),round(self.cam_ry, 0)})")

    # --- 1. MENU YA MHIMILI (AXIS) ---
    def open_axis_menu(self, instance, touch):
        if instance.collide_point(*touch.pos):
            chaguzi = ["X", "Y", "Z"]
            items = [{"text": i, "on_release": lambda x=i: self.set_axis(x)} for i in chaguzi]
            self.m_axis = MDDropdownMenu(caller=instance, items=items, width_mult=2)
            self.m_axis.open()
            return True

    def set_axis(self, x):
        self.f_axis.text = x
        self.m_axis.dismiss()#if hasattr(self, 'm_axis'): 

    # --- 2. MENU YA SLIDE AXIS ---
    def open_slide_axis_menu(self, instance, touch):
        if instance.collide_point(*touch.pos):
            chaguzi = ["X", "Y", "Z", "XY", "XZ", "YZ", "XYZ"]
            items = [{"text": i, "on_release": lambda x=i: self.set_slide_axis(x)} for i in chaguzi]
            self.m_slide = MDDropdownMenu(caller=instance, items=items, width_mult=3)
            self.m_slide.open()
            return True

    def set_slide_axis(self, x):
        self.f_slide_axis.text = x
        self.m_slide.dismiss()#if hasattr(self, 'm_slide'): 

    # --- 3. MENU YA ANIMATION TYPE ---
    def open_anim_menu(self, instance, touch):
        if instance.collide_point(*touch.pos):
            chaguzi = ["static", "rotate", "slide", "both"]
            items = [{"text": i, "on_release": lambda x=i: self.set_anim_type(x)} for i in chaguzi]
            self.m_anim = MDDropdownMenu(caller=instance, items=items, width_mult=3)
            self.m_anim.open()
            return True

    def set_anim_type(self, x):
        self.f_anim_type.text = x
        self.m_anim.dismiss()
        #if hasattr(self, 'm_anim'): 

    # --- 4. MENU YA LOOP MODE ---
    def open_loop_menu(self, instance, touch):
        if instance.collide_point(*touch.pos):
            chaguzi = ["once", "ping-pong"]
            items = [{"text": i, "on_release": lambda x=i: self.set_loop_mode(x)} for i in chaguzi]
            self.m_loop = MDDropdownMenu(caller=instance, items=items, width_mult=3)
            self.m_loop.open()
            return True

    def set_loop_mode(self, x):
        self.f_loop.text = x
        self.m_loop.dismiss()#if hasattr(self, 'm_loop'): 


    def show_workshop(self, *args):
        """Inafungua uwanja wa ujenzi na kutabiri jina la kipekee la mbao kwa ustaarabu"""
        try:
            # 1. PATA CONTENT (Ubao wa Workshop)
            content = getattr(self, 'workshop_scroll', None)
            if not content:
                ##print("⚠️ Kosa: workshop_scroll haikupatikana!")
                return

            # --- 2. RESCUE SYSTEM & GUARD (Kuzuia Recursion Error) ---
            if not hasattr(self, 'original_workshop_parent'):
                self.original_workshop_parent = content.parent
            
            if content.parent:
                content.parent.remove_widget(content)

            # Sensa ya kuzuia mzunguko usiokwisha
            self._is_dialog_closing = False 

            def finalize_restore(*args):
                """Inarudisha ubao nyumbani kistaarabu bila kukwama"""
                if self._is_dialog_closing:
                    return
                self._is_dialog_closing = True
                
                try:
                    # Ondoa content popote ilipo sasa hivi
                    if content.parent:
                        content.parent.remove_widget(content)
                    
                    # Rudisha content kwenye nyumba yake ya asili
                    if self.original_workshop_parent:
                        if content not in self.original_workshop_parent.children:
                            self.original_workshop_parent.add_widget(content)
                    
                    # Funga dialog kama bado ipo kioni
                    if hasattr(self, 'workshop_dialog') and self.workshop_dialog:

                        # Unbind kuzuia simu za kurudia
                        self.workshop_dialog.unbind(on_dismiss=finalize_restore)
                        self.workshop_dialog.dismiss()
                        self.workshop_dialog = None
                except Exception as e:
                    self.update_status(f"Restore Error: {traceback.format_exc()}",is_error=True)
                finally:
                    self._is_dialog_closing = False

            # --- 3. AKILI YA UTABIRI WA JINA (Unique ID Generator) ---
            import re
            def generate_unique_id(base_name):
                base = re.sub(r'_\d+$', '', base_name).strip() or "Ubao"
                existing_numbers = [-1]
                for obj in getattr(self, 'scene_objects', []):
                    obj_id = str(obj.get('id', ''))
                    if obj_id.startswith(base):
                        match = re.search(r'_(\d+)$', obj_id)
                        if match: existing_numbers.append(int(match.group(1)))
                        elif obj_id == base: existing_numbers.append(0)
                return f"{base}_{max(existing_numbers) + 1}"

            # --- 4. INITIALIZE FIELDS ---
            # Predict jina linalofuata kulingana na mbao iliyochaguliwa
            import sqlite3, json, os
            from kivy.app import App
            app = App.get_running_app()
            db_path = os.path.join(app.db_path, "BIM_Factory.sqlite")
            con=sqlite3.connect(db_path)
            csr=con.cursor() 
            kazi_id=f"{self.current_mteja_id}.{app.bidhaa_jina2.index(self.project_name)}_{self.project_name}"
            
            michoro=csr.execute(f"SELECT data_ya_mchoro FROM miradi_ya_fenicha").fetchall() 
            if len (michoro)>0:
                try:
                    data=csr.execute(f"SELECT data_ya_mchoro FROM miradi_ya_fenicha WHERE (mteja_id,kazi_namba) = (?,?)",(str(self.current_mteja_id),kazi_id)).fetchone()
                    last=json.loads(data[0])
                    mteja=csr.execute(f"SELECT jina_la_mteja FROM miradi_ya_fenicha WHERE mteja_id = ?",str(self.current_mteja_id)).fetchone()
                    self.update_status(f'Tumepata data za kazi ya {mteja[0]}')
                except:
                    try:
                        data=csr.execute(f"SELECT data_ya_mchoro FROM miradi_ya_fenicha WHERE status = ?",(int(len(michoro)),)).fetchone()
                        last=json.loads(data[0])
                        mteja=csr.execute(f"SELECT jina_la_mteja FROM miradi_ya_fenicha WHERE status = ?",(int(len(michoro)),)).fetchone()
                        self.update_status(f'Tumetumia data za kazi ya {mteja[0]}')
                    except:
                        ids=csr.execute(f"SELECT mteja_id FROM miradi_ya_fenicha").fetchall()
                        
                        ll=[]
                        for i in ids:
                            ll.append(i)
                        
                        chaguo=random.choice(ll)
                        data=csr.execute(f"SELECT data_ya_mchoro FROM miradi_ya_fenicha WHERE mteja_id = ?",chaguo).fetchone()
                        last=json.loads(data[0])
                        mteja=csr.execute(f"SELECT jina_la_mteja FROM miradi_ya_fenicha WHERE mteja_id = ?",chaguo).fetchone()
                        self.update_status(f'Tumetumia data za kazi ya {mteja[0]}')


                #last=last[-1]
                if len(last)>0:
                    last=last[-1]
                    aina_ya_mbao = last['id']
                    self.f_wood.text=last['wood_type']
                    self.f_parent.text=last["parent"]
                    self.f_asili.text=last["asili"]
                    self.halisi=last["halisi"]
                    print(f"whoooo {self.f_w.text,last['dim'][0]}")
            else:
                aina_ya_mbao=''
            con.close()   
            self.f_id.text = generate_unique_id(aina_ya_mbao)
            
            # Weka default values za ujenzi mpya
            ##print(f'ID---{self.f_id.text}')
            try:f_asili=self.scene_objects[self.f_id.text]['halisi']['jina']
            except:f_asili='Mbao'
            #self.f_asili.text=f_asili#, self.f_h.text, self.f_d.text = "0.6", "2.0", "0.02"
            #self.f_x.text, self.f_y.text, self.f_z.text = "0", "-1.45", "0"

            # --- 5. JENGA DIALOG UI ---
            from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText,MDDialogButtonContainer, MDDialogContentContainer
                
            from kivymd.uix.button import MDButton, MDButtonText

            self.workshop_dialog = MDDialog(
                MDDialogHeadlineText(text="Uchoraji"),
                MDDialogContentContainer(content, orientation="vertical"),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="Ghairi"), 
                        on_release=lambda x: finalize_restore()
                    ),
                    MDButton(
                        MDButtonText(text="Chora"), 
                        style="filled",
                        on_release=lambda x: [self.construct(), finalize_restore()]
                    ),
                ),
            )
            
            # Bind kitendo cha kugusa pembeni (outside touch) kifuate logic hiyo hiyo
            self.workshop_dialog.bind(on_dismiss=finalize_restore)
            self.workshop_dialog.open()

        except Exception as e:
            self.update_status(f"BIM Workshop Critical Error: {traceback.format_exc()}",is_error=True)

    def malizana(self,*args):
        ff=[
            [self.focal,self.f_fl],
            [self.cam_x,self.f_cx],
            [self.cam_y,self.f_cy],
            [self.cam_z,self.f_cz],
            [self.cam_rx,self.f_yaw],
            [self.cam_ry,self.f_ptch],
            [self.maboresho_sort,self.f_sort],
            [self.eneo_,self.f_eneo],
            [self.speed,self.f_speed]
        ]
        aa=[]
        for i in ff:
            try:
                a=i[1][0].text
                
            except:
                a=i[1].text
            aa.append(float(a))
        self.focal=aa[0]
        self.cam_x=aa[1]
        self.cam_y=aa[2]
        self.cam_z=aa[3]
        self.cam_rx=aa[4]
        self.cam_ry=aa[5]
        self.eneo_=aa[7]
        self.maboresho_sort=aa[6]
        self.speed=aa[8]
        
    def construct(self, *args):
        """Inasoma Workshop na kujenga mbao uwanjani (BIM Builder)"""
        try:
            # 1. Helper ya kugeuza text kuwa list ya namba (Gia)
            def t2l(text_val, default=0.0):
                txt = str(text_val).strip()
                if not txt: return [default]
                try: return [float(x.strip()) for x in txt.split(",")]
                except: return [default]

            # --- AKILI YA UTABIRI WA JINA (Unique ID Guard) ---
            import re
            base_input = self.f_id.text.strip() or "Mbao"
            # Safisha jina (Ondoa namba kama 'Mlango_1' iwe 'Mlango')
            base_clean = re.sub(r'_\d+$', '', base_input).strip()
            
            existing_numbers = [-1] 
            for obj in self.scene_objects:
                obj_id = str(obj.get('id', ''))
                if obj_id.startswith(base_clean):
                    match = re.search(r'_(\d+)$', obj_id)
                    if match: existing_numbers.append(int(match.group(1)))
                    elif obj_id == base_clean: existing_numbers.append(0)
            
            final_unique_id = f"{base_clean}_{max(existing_numbers) + 1}"
            self.final_id=final_unique_id

            # 2. Pata rangi halisi toka kwenye Catalog
            jina_la_vifaa = self.f_wood.text
            # Tunatumia Bongo Wood Catalog uliyoiandika awali
            # (Hakikisha BONGO_WOOD_CATALOG inapatikana global)
            wood_data = BONGO_WOOD_CATALOG.get(jina_la_vifaa, BONGO_WOOD_CATALOG["Mninga (Bloodwood)"])
            rangi_halisi = wood_data["color"]

            # 3. Jenga mnyororo wa miondoko (Animation Steps)
            s_speeds = t2l(self.f_speed.text, 0.4)
            s_limits = t2l(self.f_limit.text, 0.8)
            r_speeds = t2l(self.f_ang_speed.text, 50.0)
            r_limits = t2l(self.f_ang_limit.text, 90.0)
            
            b_s_speeds = t2l(self.f_back_speed.text, 0.4)
            b_s_limits = t2l(self.f_back_limit.text, 0.0)
            b_r_speeds = t2l(self.f_back_ang.text, 50.0)
            b_r_limits = t2l(self.f_back_ang_limit.text, 0.0)

            def build_sequence(spds, lims, r_spds, r_lims):
                seq = []
                for i in range(max(len(spds), len(r_spds))):
                    seq.append({
                        'spd': spds[i] if i < len(spds) else spds[-1],
                        'limit': lims[i] if i < len(lims) else lims[-1],
                        'ang_spd': r_spds[i] if i < len(r_spds) else r_spds[-1],
                        'ang_limit': r_lims[i] if i < len(r_lims) else r_lims[-1]
                    })
                return seq

            # 4. UNDA OBJECT KAMILI YA BIM
            s_axis = self.f_slide_axis.text.upper()
            def f_val(field, default=0.0):
                try: return float(field.text) if field.text.strip() else default
                except: return default
            new_obj = {
                "id": final_unique_id, # Imetumia jina la Unique sasa!
                "parent": self.f_parent.text.strip(),
                "asili":self.f_asili.text,
                "halisi":self.halisi,
                "dim": [f_val(self.f_w, 600),f_val(self.f_h, 2000),f_val(self.f_d, 20)],
                "pos": [f_val(self.f_x, 0),f_val(self.f_y, 0),f_val(self.f_z, 0)],
                "pivot": [float(self.f_px.text or 0), float(self.f_py.text or 0), float(self.f_pz.text or 0)],
                "color": rangi_halisi,
                "visible": True,
                "wood_type": self.f_wood.text,
                "axis": self.f_axis.text.upper() or "Y",
                "mipaka":{
                    'x':[f_val(self.f_x, 0), f_val(self.f_x, 0)+f_val(self.f_w, 600)],
                    'y':[f_val(self.f_y, 0), f_val(self.f_y, 0)+f_val(self.f_h, 2000)],
                    'z':[f_val(self.f_z, 0), f_val(self.f_z, 0)+f_val(self.f_d, 20)]
                },
                "slide_vec": [1.0 if "X" in s_axis else 0.0, 
                              1.0 if "Y" in s_axis else 0.0, 
                              1.0 if "Z" in s_axis else 0.0],
                "anim": {
                    "type": self.f_anim_type.text.lower(),
                    "state": "paused_closed",
                    "val": 0.0, "ang_val": 0.0, "timer": 0.0,
                    "opening_steps": build_sequence(s_speeds, s_limits, r_speeds, r_limits),
                    "closing_steps": build_sequence(b_s_speeds, b_s_limits, b_r_speeds, b_r_limits),
                    "time_before_start": float(self.f_t_start.text or 0),
                    "time_before_return": float(self.f_t_return.text or 2),
                    "loop_mode": self.f_loop.text.lower()
                },
                "hit_area": []
            }
            self.scene_objects.append(new_obj)
            
            '''if 'duara' in final_unique_id:
                self.scene_objects.remove(new_obj)
            
                vibox=self.duara(new_obj['pos'],new_obj['dim'])
                for i in vibox:
                    obj=new_obj
                    obj['id']=f"{new_obj['id']}_{vibox.index(i)}"
                    obj['pos']=i[1]
                    obj['dim']=i[0]
                    self.scene_objects.append(obj)'''

            # 5. WEKA KWENYE SITE NA CHORA
            self.is_constructed = True
            raangee=int(self.f_marudio.text)
            if raangee > 0:
                self.single_axis_multiply(new_obj,axis=self.f_marudio_axis.text,interval=self.f_marudio_interval.text,raange=raangee)
                
            
            # --- TRIGGER AUTO-SAVE (Akili ya Database) ---
            #if hasattr(self, 'trigger_auto_save'):
            self.trigger_auto_save()
            
            # Funga workshop dialog
            #if hasattr(self, 'workshop_dialog'):
            try:self.workshop_dialog.dismiss()
            except:pass
            #self.update_status(f"BIM: {new_obj['id']} ({jina_la_vifaa}) imejengwa!")
            #self.smam_solid_subtraction_engine()
            
            
            Clock.schedule_once(lambda dt: self.kamilisha(), 0)
                
                

        except Exception as e:
            self.update_status(f"Construct Error: {traceback.format_exc()}",is_error=True)


    def kamilisha(self):
        self.mavituz={}
        indx=0
        for i in self.scene_objects_mrudio:
            jina=i['id']
            kt={}
            if jina in self.rudia.keys():
                self.scene_objects_mrudio[indx]['pos'][self.mhimili]=i['pos'][self.mhimili]=self.rudia[jina]
                if i['pos'][self.mhimili]==self.rudia[jina]:
                    for ii in i:
                        kt[ii]=i[ii]
                        if ii=='hit_area':
                            self.mavituz[jina]=kt
                            self.mavituz[jina]['pos'][self.mhimili]=self.rudia[jina]+self.poss
                            self.hamsha_popo(jina,kt)
                                
                            print(indx)
                            print(self.scene_objects_mrudio[indx])
                            #print(self.scene_objects[self.scene_objects.index(kt)])
                    
                    print(self.mhimili,kt)
                    
                    #self.scene_objects.append(kt)
                    if self.scene_objects_mrudio.index(i)==len(self.scene_objects_mrudio)-1:
                        Clock.schedule_once(lambda dt: self.soma(), 30)
                        print(self.scene_objects)
            indx+=1
        self.trigger_auto_save()
        print(self.scene_objects_mrudio)
        

    def hamsha_popo(self,p_id,data):
        import sqlite3, json, os
        app = App.get_running_app()
        mteja=self.current_mteja_id
        db_path = os.path.join(app.db_path, "Multiple__partS.sqlite")
        kazi=f"{self.current_mteja_id}.{self.kazi.index(self.project_name)}_{self.project_name}"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        mchoro_json= json.dumps(data)
        # --- 🛠️ JENGA TABLE KWA MPANGILIO MPYA ---
        cursor.execute('''CREATE TABLE IF NOT EXISTS Multiple__parts (id INTEGER PRIMARY KEY AUTOINCREMENT, mteja_id TEXT , part_id TEXT, data_ya_mchoro TEXT, namba_ya_kazi TEXT)''')
        #self.vyote=cursor.execute('SELECT * FROM Multiple__parts').fetchall()
        # Jaribu kuongeza column ya kamera kama database ni ya kizamani
        
        cursor.execute('''INSERT INTO Multiple__parts 
            (mteja_id,part_id, data_ya_mchoro, namba_ya_kazi) VALUES (?, ?, ?, ?) ''', (mteja, p_id, mchoro_json, kazi))
        conn.commit()
        conn.close()   
        print('tayaaari')
        print(self.mavituz)
    
    def soma(self):
        import sqlite3, json, os, ast
        from kivy.app import App
        from kivy.clock import Clock

        mteja=self.current_mteja_id
        # 1. Tafuta database ilipo
        app = App.get_running_app()
        db_path = os.path.join(app.db_path, "Multiple__partS.sqlite")
        kazi=f"{self.current_mteja_id}.{self.kazi.index(self.project_name)}_{self.project_name}"
        if not os.path.exists(db_path): 
            self.update_status("❌ Database haipatikani!")
            return False

        # 2. Fungua mawasiliano na SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 3. Vuta data kwa kutumia 'mteja_id' ya mteja uliyem-click kwenye menu
        #try:
        cursor.execute("SELECT data_ya_mchoro FROM Multiple__parts WHERE (mteja_id , namba_ya_kazi) = (? , ?)", (str(mteja),str(kazi)))
        row = cursor.fetchall()
            
        '''except sqlite3.OperationalError:
            # Kinga kwa ajili ya database za zamani zisizo na column ya kamera
            cursor.execute("SELECT data_ya_mchoro FROM Multiple__parts WHERE mteja_id = ?", (str(mteja_id),))
            try:
                cursor.execute("ALTER TABLE miradi_ya_fenicha ADD COLUMN kazi_namba TEXT")
                cursor.execute(f"UPDATE miradi_ya_fenicha SET kazi_namba = ? WHERE mteja_id = ?",(str(kazi),str(mteja_id)))
            except:
                cursor.execute(f"UPDATE miradi_ya_fenicha SET kazi_namba = ? WHERE mteja_id = ?",(str(kazi),str(mteja_id)))
            
            row = cursor.fetchone()
            print(kazi,"---")
            if row: 
                row = (row[0], None) # Tengeneza row ya uongo ya kamera'''
        
         # Funga mawasiliano ya database mapema

        # 4. Kama data imepatikana, anza mchakato wa kuipakia
        print(row[0][0])
        if row and row[0]:
            
            # [DAWA YA TATIZO]: Ita uwanja usafishwe kwanza hapa!
            #self.safisha_uwanja() 

            # 5. Lock ID ya mteja huyu sasa hivi kwenye mfumo
            #self.current_mteja_id = str(mteja_id) 

            # 6. Pakia data ya mbao (Mchoro wa fenicha) ya huyu mteja pekee yake
            matokeo = []
            for i in row:
                dct=i[0]
                #dctt=ast.literal_eval(dct)
                matokeo.append(json.loads(dct))
                if row.index(i)==len(self.scene_objects_mrudio)-1:
                    self.scene_objects.extend(matokeo)
                    if self.f_render.text!='0':
                        self.f_render.text='0'
                        Clock.schedule_once(lambda dt: self.render_arch_scene(), 3)
                    Clock.schedule_once(lambda dt: cursor.execute(f"DELETE FROM Multiple__parts"), 5)
                    Clock.schedule_once(lambda dt: conn.commit(), 7)
                    Clock.schedule_once(lambda dt: conn.close(), 10)
                    Clock.schedule_once(lambda dt: self.trigger_auto_save(), 10)
                    

            print('    haya hapa \n',matokeo)
            
            # 8. Lipua upya kioni kwa kutumia Clock ili Kivy isikwame (asynchronous rendering)
            #Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)
            
            ##print(f"✅ Kazi ya mteja ID: {mteja_id} imerejeshwa ikiwa safi peke yake!")
            return matokeo
            
        ##print("⚠️ Hakuna data iliyopatikana kwa ID hii.")
        return False

    
    def move_eye(self, direction):
        """
        Relative Navigation Hub: Inamwezesha mtumiaji kutembea uwanjani.
        Inazingatia mzunguko wa dunia (Orbit) na uelekeo wa jicho (Yaw).
        """
        try:
            spd = self.speed
            # 1. TAFUTA ANGLE HALISI (Fidia mzunguko wa dunia)
            w_rot = float(getattr(self, 'world_rot_y', 0))
            # Hapa tunapata mwelekeo wa kweli wa 'Mbele' machoni pako
            total_ry = math.radians(float(self.cam_ry) - w_rot) 

            # 2. DECISION MATRIX (Z-Axis & X-Axis Relative)
            if direction == "forward":
                self.cam_x += math.sin(total_ry) * spd
                self.cam_z += math.cos(total_ry) * spd
            elif direction == "backward":
                self.cam_x -= math.sin(total_ry) * spd
                self.cam_z -= math.cos(total_ry) * spd
            elif direction == "left":
                # Kushoto ni nyuzi 90 kutoa kwenye mwelekeo wa mbele
                self.cam_x -= math.cos(total_ry) * spd
                self.cam_z += math.sin(total_ry) * spd
            elif direction == "right":
                # Kulia ni nyuzi 90 kuongeza
                self.cam_x += math.cos(total_ry) * spd
                self.cam_z -= math.sin(total_ry) * spd
            
            # 3. ELEVATION (Mhimili wa Y - Hauna uhusiano na Orbit)
            elif direction == "up":
                self.cam_y += spd
            elif direction == "down":
                self.cam_y -= spd

            # 4. RE-RENDER (Chora frame mpya papo hapo)
            Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)

        except Exception as e:
            self.update_status(f"Move Error: {traceback.format_exc()}",is_error=True)

    def open_wood_menu(self, caller,badili=False):
        from kivy.core.window import Window
        marangi={}
        if badili:        
            for key in BONGO_WOOD_CATALOG.keys():
                if BONGO_WOOD_CATALOG[key]['color'] in self.makundi_ya_mwonekano()[0]:
                    marangi[key]=BONGO_WOOD_CATALOG[key]
            self.update_status(f"Hayo ndo majina ya rangi {len(marangi)} zilizotumika kupendezesha kazi ya {self.current_mteja.upper()}\nChagua sasa rangi ipi tuibadilishe ili {self.current_mteja.upper()} apate mwonekano mwingine wa tofauti!")
        else: marangi=BONGO_WOOD_CATALOG
        menu_items = [
            {
                "text": jina_la_mbao,
                "on_release": lambda c=caller, x=jina_la_mbao, b=badili: self.set_wood(x,b,caller=c,rangi=marangi[x]['color']),
            } for jina_la_mbao in marangi
        ]
        
        self.m_wood = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
            # DAWA: Inachukua 50% ya kimo cha kioo chochote kile
            max_height=Window.height * 1 
        )
        self.m_wood.open()
        

    def set_wood(self, jina,badili,rangi=[],caller=None):
        
        self.m_wood.dismiss()
        if badili:
            self.open_wood_menu(caller)
            self.previous_color=[jina,rangi]
        else:
            self.f_wood.text = jina
            self.current_color=[jina,rangi]
            try:
                aa=self.previous_color
                self.badilisha_sasa(jina,rangi)
            except:
                pass       
            self.update_status(f"Rangi ya sasa inafanana na {jina}")
        

    def open_asili_menu(self, caller):
        from kivy.core.window import Window
        mk=self.mahesabu
        #.chagua_mbao=
        menu_items = [
            {
                "text": asili_ya_kitu,
                "on_release": lambda itm=self, x=asili_ya_kitu: mk.Set__mbao(itm,x),
            } for asili_ya_kitu in ['Mbao','Board','Plywood','Pvc','Kioo','Chuma','Kitu','Sakafu','Ukuta','Dari']
        ]
        
        self.m_asili = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
            # DAWA: Inachukua 50% ya kimo cha kioo chochote kile
            max_height=Window.height * 0.5 
        )
        self.m_asili.open()

    def set_asili(self, jina):
        self.f_asili.text = jina
        if hasattr(self, 'm_wood'):
            self.m_asili.dismiss()
        self.update_status(f"Vifaa: {jina} vimepakiwa tayari kwa ujenzi.")

    def open_slide_axis_menu(self, instance, touch):
        if instance.collide_point(*touch.pos):
            from kivy.core.window import Window
            if hasattr(self, 'm_slide') and self.m_slide.parent:
                return True
                
            chaguzi = ["X", "Y", "Z", "XY", "XZ", "YZ", "XYZ"]
            menu_items = [{"text": i, "on_release": lambda x=i: self.set_slide_axis(x)} for i in chaguzi]
            
            self.m_slide = MDDropdownMenu(
                caller=instance,
                items=menu_items,
                width_mult=3,
                max_height=Window.height * 1, # 40% ya kioo
                position="bottom"
            )
            self.m_slide.open()
            return True

    def open_axis_menu(self, instance, touch):
        if instance.collide_point(*touch.pos):
            from kivy.core.window import Window
            chaguzi = ["X", "Y", "Z"]
            items = [{"text": i, "on_release": lambda x=i: self.set_axis(x)} for i in chaguzi]
            
            self.m_axis = MDDropdownMenu(
                caller=instance, 
                items=items, 
                width_mult=2,
                max_height=Window.height * 0.3 # Menu fupi ya axis
            )
            self.m_axis.open()

    def set_axis(self, x):
        self.f_axis.text = x
        if hasattr(self, 'm_axis'): self.m_axis.dismiss()

    def set_anim(self, x):
        self.f_anim_type.text = x
        if hasattr(self, 'm_anim'): self.m_anim.dismiss()

    # ==========================================
    # 🎯 INTERACTIVE PICKING & TOUCH SAFETY
    # ==========================================
    def on_touch_down(self, touch):
        # 1. Zuia fujo na UI nyingine (Buttons za pembeni)
        if super().on_touch_down(touch):
            return True

        target_obj = None
        min_depth = 9999.0

        # 2. PITIA MBAO ZOTE
        if hasattr(self, 'scene_objects'):
            for obj in self.scene_objects:
                # Kagua kila uso ambao ulichorwa kwenye frame hii
                for area in obj.get('hit_area', []):
                    # Je, kidole kiko ndani ya polygon ya uso huu?
                    if self.is_point_inside(touch.x, touch.y, area['pts']):
                        # 3. ECLIPSE TIE-BREAKER
                        # Tumia depth solver yako kujua nani yuko mbele ya mwenzake
                        d = self.get_face_radial_depth(obj, area['f_idx'])
                        
                        if d < min_depth:
                            min_depth = d
                            target_obj = obj

        # 4. TEKELEZA SELECTION
        if target_obj:
            self.highlight_selection(target_obj)
            # Fungua Workshop kistaarabu (Piga delay kidogo kwa ajili ya blink)
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.open_edit_workshop(target_obj), 0.015)
            return True
            
        return False

    def is_point_in_poly(self, x, y, poly):
        """Jordan Curve Theorem - Ray Casting"""
        n = len(poly)
        inside = False
        if n < 3: return False
        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def open_edit_workshop(self, obj):
        """Inafungua ubao wa uhariri ukiwa na adabu ya hali ya juu"""
        try:
            content = getattr(self, 'workshop_scroll', None)
            if not content: return
            
            # --- RESCUE SYSTEM ---
            if not hasattr(self, 'original_workshop_parent'):
                self.original_workshop_parent = content.parent
            if content.parent: content.parent.remove_widget(content)

            def finalize_restore(*args):
                if getattr(self, '_dialog_closing', False): return
                self._dialog_closing = True
                if content.parent: content.parent.remove_widget(content)
                if self.original_workshop_parent:
                    if content not in self.original_workshop_parent.children:
                        self.original_workshop_parent.add_widget(content)
                if hasattr(self, 'edit_dialog') and self.edit_dialog:
                    self.edit_dialog.dismiss()

            # --- SAFE DATA MAPPING (Dawa ya Attribute Error) ---
            def set_text(attr, val):
                field = getattr(self, attr, None)
                if field: field.text = str(val)

            # Jaza data kwa usalama
            ##print(f"ID---{obj.get('wood_type', '')}")
            try:f_asili=obj.get('asili', '')
            except:f_asili='Mbao'
            #self.f_asili.text=f_asili
            self.halisi=obj.get('halisi', '')
            set_text('f_id', obj.get('id', ''))
            set_text('f_wood', obj.get('wood_type', ''))
            set_text('f_asili', obj.get('asili', ''))
            set_text('f_parent', obj.get('parent', ''))
            dim, pos = obj.get('dim', [0,0,0]), obj.get('pos', [0,0,0])
            set_text('f_w', dim[0]); set_text('f_h', dim[1]); set_text('f_d', dim[2])
            set_text('f_x', pos[0]); set_text('f_y', pos[1]); set_text('f_z', pos[2])
            
            piv = obj.get('pivot', [0,0,0])
            set_text('f_px', piv[0]); set_text('f_py', piv[1]); set_text('f_pz', piv[2])
            
            sv = obj.get('slide_vec', [0,0,0])
            axis=''
            vc=['X','Y','Z']
            vcc=[]
            for i in sv:
                if i:
                    if vc[sv.index(i)] not in vcc:
                        vcc.append(vc[sv.index(i)])
            
            axis=''.join(vcc)
            print(axis)
            # Hapa ndipo ilikuwa inafeli - sasa hivi itapita hata kama f_svx haipo
            #set_text('f_svx', sv[0]); set_text('f_svy', sv[1]); set_text('f_svz', sv[2])
            set_text('f_slide_axis',axis)
            obj['anim']['type']=self.f_anim_type.text

            from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, \
                MDDialogButtonContainer, MDDialogContentContainer
            from kivymd.uix.button import MDButton, MDButtonText
            from kivymd.uix.boxlayout import MDBoxLayout

            # --- BUILD UI IKIWA NA HIDE NA DELETE ---
            hali_ficha = "ONYESHA" if not obj.get('visible', True) else "FICHA"

            self.edit_dialog = MDDialog(
                MDDialogHeadlineText(text=f"Maboresho ya {obj.get('id')}"),
                MDDialogContentContainer(content, orientation="vertical"),
                MDDialogButtonContainer(
                    MDButton(MDButtonText(text="FUTA"), style="text",
                             on_release=lambda x: self.delete_obj(obj, finalize_restore)),
                    #MDBoxLayout(), # Spacer
                    MDButton(MDButtonText(text="GHAIRI"), on_release=lambda x: finalize_restore()),
                    MDButton(MDButtonText(text="HIFADHI"), style="filled",
                             on_release=lambda x: self.tekeleza_hifadhi(obj, finalize_restore)),
                ),
            )
            self.edit_dialog.bind(on_dismiss=lambda x: finalize_restore())
            self._dialog_closing = False
            self.edit_dialog.open()
            self.update_status(obj.get('wood_type'))
        except Exception as e:
            self.update_status(f"CRITICAL UI ERROR: {traceback.format_exc()}",is_error=True)

    def highlight_selection(self, obj):
        """Inatoa blink ya rangi ya dhahabu kuonyesha mbao imeguswa"""
        try:
            # 1. Hifadhi rangi ya asili ya mbao
            orig_color = list(obj.get('color', [0.8, 0.8, 0.8, 1]))
            
            # 2. Badilisha iwe rangi ya 'Gold/Selection'
            obj['color'] = [1, 0.8, 0, 1] 
            Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)
            
            # 3. Rudisha rangi ya asili baada ya nusu sekunde (Blink effect)
            def reset_color(dt):
                obj['color'] = orig_color
                Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)
            
            Clock.schedule_once(reset_color, 0.5)
            
        except Exception as e:
            print(f"Highlight Error: {e}")

    def tekeleza_hifadhi(self, zamani_obj, callback_funga):
        """Update Engine: Inasoma Catalog na kubadili rangi ya mbao kitalamu"""
        try:
            global BONGO_WOOD_CATALOG 
            mpya_id = self.f_id.text.strip()
            aina_ya_mbao = self.f_wood.text.strip()
            
            try:
                wood_data = BONGO_WOOD_CATALOG.get(aina_ya_mbao)
                mpya_rangi = wood_data["color"] if wood_data else zamani_obj.get('color', [0.8, 0.8, 0.8, 1])
            except:
                mpya_rangi = zamani_obj.get('color', [0.8, 0.8, 0.8, 1])

            def f_val(field, default=0.0):
                try: return float(field.text) if field.text.strip() else default
                except: return default

            target_id = zamani_obj.get('id')
            s_axis=self.f_slide_axis.text
            for i in range(len(self.scene_objects)):
                if self.scene_objects[i].get('id') == target_id:
                    self.scene_objects[i] = {
                        "id": mpya_id,
                        "asili":self.f_asili.text,
                        "halisi":self.halisi,
                        "parent": self.f_parent.text.strip(),
                        "dim": [f_val(self.f_w, 600),f_val(self.f_h, 2000),f_val(self.f_d, 20)],
                        "pos": [f_val(self.f_x, 0),f_val(self.f_y, 0),f_val(self.f_z, 0)],
                        "mipaka":{
                            'x':[f_val(self.f_x, 0), f_val(self.f_x, 0)+f_val(self.f_w, 600)],
                            'y':[f_val(self.f_y, 0), f_val(self.f_y, 0)+f_val(self.f_h, 2000)],
                            'z':[f_val(self.f_z, 0), f_val(self.f_z, 0)+f_val(self.f_d, 0.02)]
                        },
        
                        "wood_type": self.f_wood.text,
                        "pivot": [f_val(self.f_px, 0), f_val(self.f_py, 0), f_val(self.f_pz, 0)],
                        "color": mpya_rangi,
                        "axis": self.f_axis.text.upper() or "Y",
                        "slide_vec": [1.0 if "X" in s_axis else 0.0, 
                                    1.0 if "Y" in s_axis else 0.0, 
                                    1.0 if "Z" in s_axis else 0.0],
                        "anim": {
                            "type": self.f_anim_type.text.lower(),
                            "state": zamani_obj.get("anim", {}).get("state", "paused_closed"),
                            "val": 0.0, "ang_val": 0.0,
                            "opening_steps": zamani_obj.get("anim", {}).get("opening_steps", []),
                            "closing_steps": zamani_obj.get("anim", {}).get("closing_steps", []),
                            "loop_mode": self.f_loop.text.lower()
                        },
                        "hit_area": [] 
                    }
                    new_obj=self.scene_objects[i]
                    break

            # --- KETE YA USHINDI ---
            #self.smam_solid_subtraction_engine()
            #self.trigger_auto_save()
            from kivy.clock import Clock
            raangee=int(self.f_marudio.text)
            if raangee > 0:
                self.single_axis_multiply(new_obj,axis=self.f_marudio_axis.text,interval=self.f_marudio_interval.text,raange=raangee)

            Clock.schedule_once(self.trigger_auto_save,0) # Lazimisha save kwenye database baada ya kuedit
            Clock.schedule_once(lambda dt: self.kamilisha(), 0)
            #self.canvas.clear()
            #Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)
            
            #self.update_status(f"BIM: {mpya_id} imesasishwa kitalamu!")
            callback_funga() 

        except Exception as e:
            print(f"BIM Update Error: {e}")
            self.update_status(f"Hifadhi Error: {str(e)[:15]}", is_error=True)

    def delete_obj(self, obj,*arg):
        """Inafuta mbao uwanjani kabisa"""
        try:
            if obj in self.scene_objects:
                self.scene_objects.remove(obj)
            
            if hasattr(self, 'edit_dialog'):
                self.edit_dialog.dismiss()
                
            Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)
            self.update_status(f"Mbao {obj.get('id')} imefutwa!")
            
            if hasattr(self.parent, 'auto_save'):
                self.parent.auto_save()
        except Exception as e:
            self.update_status(f"Delete Error: {traceback.format_exc()}",is_error=True)

 
    def is_point_inside(self, tx, ty, poly):
        """Standard Ray-Casting algorithm ya 2D"""
        n = len(poly)
        inside = False
        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if ty > min(p1y, p2y):
                if ty <= max(p1y, p2y):
                    if tx <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (ty - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or tx <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def toggle_hide_obj(self, obj, callback_funga):
        """Inaficha mbao kioni bila kuifuta kwenye kumbukumbu"""
        try:
            # Badilisha hali: kama haipo au ni True, iwe False
            obj['visible'] = not obj.get('visible', True)
            
            self.canvas.clear()
            Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)
            
            hali = "imefichwa" if not obj['visible'] else "inaonekana"
            self.update_status(f"BIM: {obj.get('id')} {hali} kitalamu.")
            
            # Funga dialog baada ya kuficha
            callback_funga()
        except Exception as e:
            self.update_status(f"Hide Error: {traceback.format_exc()}",is_error=True)


    def trigger_auto_save(self, *args):
        """Inahifadhi kila kitu na kutengeneza columns mpya kiatomatiki"""
        import sqlite3, json, os
        from kivy.app import App

        try:
            if not hasattr(self, 'scene_objects') or len(self.scene_objects) == 0:
                return

            app = App.get_running_app()
            db_path = os.path.join(app.db_path, "BIM_Factory.sqlite")
            
            m_id, m_jina,kazi_id = str(getattr(self, 'current_mteja_id', 'N/A')), str(getattr(self, 'current_mteja', 'Mteja_Mpya')),f"{self.current_mteja_id}.{self.kazi.index(self.project_name)}_{self.project_name}"
                        # --- SULUHISHO LA UHAKIKA KUZUIA MAXIMUM RECURSION ---
            
            def safisha_data_salama(data_nzima):
                """Inasafisha data bila kutumia recursion ili kuzuia kabisa Maximum Recursion Error"""
                import collections
                
                # Aina za data zinazoruhusiwa kwenye JSON
                aina_safi = (int, float, str, bool, type(None))
                
                # Set ya kufuatilia vitu ambavyo tayari tumevipitia (Kuzuia mzunguko)
                tayari_vimepitiwa = set()
                
                # Kama data kubwa sio dict au list, irudishe ikiwa hivyo hivyo
                if not isinstance(data_nzima, (dict, list)):
                    return data_nzima if isinstance(data_nzima, aina_safi) else None

                # Hakikisha tunaanza na nakala mpya kabisa
                if isinstance(data_nzima, dict):
                    matokeo_makuu = {}
                    foleni = collections.deque([(data_nzima, matokeo_makuu)])
                    tayari_vimepitiwa.add(id(data_nzima))
                else:
                    matokeo_makuu = []
                    foleni = collections.deque([(data_nzima, matokeo_makuu)])
                    tayari_vimepitiwa.add(id(data_nzima))

                while foleni:
                    chanzo, lengo = foleni.popleft()

                    if isinstance(chanzo, dict):
                        for k, v in chanzo.items():
                            k_str = str(k)
                            if k_str.startswith('_'):  # Ruka internal variables za Kivy
                                continue
                                
                            if isinstance(v, aina_safi):
                                lengo[k_str] = v
                            elif isinstance(v, (dict, list)):
                                if id(v) in tayari_vimepitiwa:
                                    lengo[k_str] = "[Mzunguko_Umekatwa]"  # Imezuia loop hapa!
                                    continue
                                tayari_vimepitiwa.add(id(v))
                                
                                if isinstance(v, dict):
                                    lengo[k_str] = {}
                                    foleni.append((v, lengo[k_str]))
                                else:
                                    lengo[k_str] = []
                                    foleni.append((v, lengo[k_str]))
                            else:
                                lengo[k_str] = str(v)[:100]  # Badili Kivy objects kuwa string ya kawaida

                    elif isinstance(chanzo, list):
                        for item in chanzo:
                            if isinstance(item, aina_safi):
                                lengo.append(item)
                            elif isinstance(item, (dict, list)):
                                if id(item) in tayari_vimepitiwa:
                                    lengo.append("[Mzunguko_Umekatwa]")
                                    continue
                                tayari_vimepitiwa.add(id(item))
                                
                                if isinstance(item, dict):
                                    mpya = {}
                                    lengo.append(mpya)
                                    foleni.append((item, mpya))
                                else:
                                    mpya = []
                                    lengo.append(mpya)
                                    foleni.append((item, mpya))
                            else:
                                lengo.append(str(item)[:100])

                return matokeo_makuu

            # --- IWEKE HIVI NDANI YA trigger_auto_save ---
            #safi_scene_objects = safisha_data_salama(self.scene_objects)
            #mchoro_json = json.dumps(safi_scene_objects)

            mchoro_json = json.dumps(self.scene_objects)
            kamera_json = json.dumps({"x":self.cam_x,"y":self.cam_y,"z":self.cam_z,"rx":self.cam_rx,"ry":self.cam_ry})

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # --- 🛠️ JENGA TABLE KWA MPANGILIO MPYA ---
            cursor.execute('''CREATE TABLE IF NOT EXISTS miradi_ya_fenicha 
                (mteja_id TEXT PRIMARY KEY, jina_la_mteja TEXT, aina_ya_fenicha TEXT, 
                data_ya_mchoro TEXT, data_ya_kamera TEXT, status INTEGER, tarehe_ya_kazi TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            self.vyote=cursor.execute('SELECT * FROM miradi_ya_fenicha').fetchall()
            # Jaribu kuongeza column ya kamera kama database ni ya kizamani
            try: cursor.execute("ALTER TABLE miradi_ya_fenicha ADD COLUMN kazi_namba TEXT")
            except: pass # Inamaanisha column tayari ipo
            cursor.execute('''INSERT INTO miradi_ya_fenicha 
                (mteja_id, jina_la_mteja, data_ya_mchoro, data_ya_kamera,kazi_namba) VALUES (?, ?, ?, ?,?)
                ON CONFLICT(mteja_id) DO UPDATE SET
                    kazi_namba = excluded.kazi_namba,
                    data_ya_mchoro = excluded.data_ya_mchoro,
                    data_ya_kamera = excluded.data_ya_kamera,
                    tarehe_ya_kazi = CURRENT_TIMESTAMP
                ''', (m_id, m_jina, mchoro_json, kamera_json,kazi_id))

            try:
                cursor.execute("ALTER TABLE miradi_ya_fenicha ADD COLUMN status TEXT")
                All_ids=cursor.execute("SELECT mteja_id FROM miradi_ya_fenicha").fetchall()
                if len(All_ids)>1:
                    for i in range (len(All_ids)-1):
                        i=i+1
                        cursor.execute(f"UPDATE miradi_ya_fenicha SET status = ? WHERE mteja_id = ?",(i,f"{All_ids[i][0]}"))
                        print(f"ssss {All_ids[i][0]}")
                elif len(All_ids)==1:
                    cursor.execute(f"UPDATE miradi_ya_fenicha SET status = ? WHERE mteja_id = ?",(1,f"1"))
                        
            except:
                #cursor.execute("ALTER TABLE miradi_ya_fenicha ADD COLUMN status INTEGER")
                pass
            All_ids=cursor.execute("SELECT mteja_id FROM miradi_ya_fenicha").fetchall()
            try:
                crnt=cursor.execute("SELECT status FROM miradi_ya_fenicha WHERE mteja_id = ?", (m_id,)).fetchone()
                #self.update_status(f"Kazi ya {m_jina} ni kazi inayoendelea kudesigniwa")
            except:
                try:
                    cursor.execute(f"UPDATE miradi_ya_fenicha SET status = ? WHERE mteja_id = ?",(len(All_ids)+1,m_id,))
                    self.update_status(f"Kazi ya {m_jina} ni kazi inayoanza kudesigniwa")
                except:
                    cursor.execute("ALTER TABLE miradi_ya_fenicha ADD COLUMN status INTEGER")
                    All_ids=cursor.execute("SELECT mteja_id FROM miradi_ya_fenicha").fetchall()
                    for i in range (len(All_ids)-1):
                        i=i+1
                        cursor.execute(f"UPDATE miradi_ya_fenicha SET status = ? WHERE mteja_id = ?",(i,f"{All_ids[i][0]}"))
                        self.update_status(f"{All_ids[i][0]}")
                    

            All_ids=cursor.execute(f"SELECT mteja_id FROM miradi_ya_fenicha WHERE status > ?", (crnt[0],) ).fetchall()
            
            badiliko=[]
            next=0
            for i in range(len(All_ids)-1):
                sts=cursor.execute("SELECT status FROM miradi_ya_fenicha WHERE mteja_id = ?", (All_ids[i+1][0],)).fetchone()
                sts1=cursor.execute("SELECT jina_la_mteja FROM miradi_ya_fenicha WHERE mteja_id = ?", (All_ids[i+1][0],)).fetchone()
                sts2=cursor.execute("SELECT mteja_id FROM miradi_ya_fenicha WHERE mteja_id = ?", (All_ids[i+1][0],)).fetchone() 
                               
                try:
                    next=sts[0]+1    
                    if sts[0] > crnt[0]:
                        
                        badiliko.append(sts2)
                        
                except:
                    #cursor.execute(f"UPDATE miradi_ya_fenicha SET status = ? WHERE mteja_id = ?",(next,All_ids[i+1][0]))
                    badiliko.append(sts2)
                    self.update_status (f"Kazi ya {sts1[0]} haifahamiki ni ya ngapi!")
            for i in All_ids:
                sts=cursor.execute("SELECT status FROM miradi_ya_fenicha WHERE mteja_id = ?", i).fetchone()
                sts1=cursor.execute("SELECT jina_la_mteja FROM miradi_ya_fenicha WHERE mteja_id = ?", i).fetchone()
                cursor.execute(f"UPDATE miradi_ya_fenicha SET status = ? WHERE mteja_id = ?",(int(sts[0])-1,i[0]))
                cursor.execute(f"UPDATE miradi_ya_fenicha SET status = ? WHERE mteja_id = ?",(int(len(All_ids)),str(m_id)))
            

            conn.commit()
            conn.close()
            self.f_cx.text=f"{self.cam_x}"
            self.f_cy.text =f"{self.cam_y}"
            self.f_cz.text =f"{self.cam_z}"
            self.f_yaw.text=f"{self.cam_rx}"
            self.f_ptch.text=f"{self.cam_ry}"
            
        except Exception as e:
            self.update_status(f"Save Error: {traceback.format_exc()}",is_error=True)


    def safisha_uwanja(self):
        """
        [KIPENGELE CHA 1: USAFISHAJI MKUU]
        Inafuta kabisa kila kitu kwenye kumbukumbu na skrini kabla ya kupakia kazi mpya.
        """
        self.scene_objects = []  # Safisha list ya mbao/vitu vya 3D kuwa tupu kabisa
        self.canvas.clear()      # Safisha michoro yote ya zamani kwenye Kivy Canvas
        
        # Reset majina na ID ili auto-save isivuruge wateja wengine
        #self.current_mteja_id = 'N/A'
        #self.current_mteja = 'Mteja_Mpya'
        
        # Kama unatumia widgets kama alama za vipimo au vidude vya kushika (handles), vifute
        if hasattr(self, 'clear_widgets'):
            self.clear_widgets()
            
        ##print("🧹 Uwanja umesafishwa kikamilifu! Hakuna mabaki ya mteja aliyepita.")

    def rejesha_kumbukumbu(self, mteja_id,listi,kazi):
        """
        [KIPENGELE CHA 2: UVUTAJI WA DATA NA REJESHO]
        Inavuta data ya mteja mmoja mahususi kutoka kwenye SQLite na kuilipua kioni yenyewe pekee.
        """
        import sqlite3, json, os
        from kivy.app import App
        from kivy.clock import Clock

        try:
            # 1. Tafuta database ilipo
            app = App.get_running_app()
            db_path = os.path.join(app.db_path, "BIM_Factory.sqlite")
            kazi=f"{mteja_id}.{listi.index(kazi)}_{kazi}"
            if not os.path.exists(db_path): 
                self.update_status("❌ Database haipatikani!")
                return False

            # 2. Fungua mawasiliano na SQLite
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 3. Vuta data kwa kutumia 'mteja_id' ya mteja uliyem-click kwenye menu
            #try:
            cursor.execute("SELECT data_ya_mchoro, data_ya_kamera FROM miradi_ya_fenicha WHERE (mteja_id , kazi_namba) = (? , ?)", (str(mteja_id),str(kazi)))
            row = cursor.fetchone()
                
            '''except sqlite3.OperationalError:
                # Kinga kwa ajili ya database za zamani zisizo na column ya kamera
                cursor.execute("SELECT data_ya_mchoro, data_ya_kamera FROM miradi_ya_fenicha WHERE mteja_id = ?", (str(mteja_id),))
                try:
                    cursor.execute("ALTER TABLE miradi_ya_fenicha ADD COLUMN kazi_namba TEXT")
                    cursor.execute(f"UPDATE miradi_ya_fenicha SET kazi_namba = ? WHERE mteja_id = ?",(str(kazi),str(mteja_id)))
                except:
                    cursor.execute(f"UPDATE miradi_ya_fenicha SET kazi_namba = ? WHERE mteja_id = ?",(str(kazi),str(mteja_id)))
                
                row = cursor.fetchone()
                print(kazi,"---")
                if row: 
                    row = (row[0], None) # Tengeneza row ya uongo ya kamera'''
            
            conn.close() # Funga mawasiliano ya database mapema

            # 4. Kama data imepatikana, anza mchakato wa kuipakia
            print(row)
            if row and row[0]:
                
                # [DAWA YA TATIZO]: Ita uwanja usafishwe kwanza hapa!
                self.safisha_uwanja() 

                # 5. Lock ID ya mteja huyu sasa hivi kwenye mfumo
                self.current_mteja_id = str(mteja_id) 

                # 6. Pakia data ya mbao (Mchoro wa fenicha) ya huyu mteja pekee yake
                self.scene_objects = json.loads(row[0])
                
                # 7. Pakia data ya kamera (Jicho/Muonekano wa 3D) kama ipo
                if len(row) > 1 and row[1]:
                    try:
                        c = json.loads(row[1])
                        self.cam_x, self.cam_y, self.cam_z = c.get('x', 0), c.get('y', 0), c.get('z', 8)
                        self.f_cx.text=f"{c.get('x', 0)}"
                        self.f_cy.text =f"{c.get('y', 0)}"
                        self.f_cz.text =f"c.get('z', 0)"
                        self.f_yaw.text=f"{c.get('rx', 0)}"
                        self.f_ptch.text=f"{c.get('ry', 0)}"
                        self.cam_rx, self.cam_ry = c.get('rx', 0), c.get('ry', 0)
                    except Exception as e:
                        self.update_status(f"Camera Error: {traceback.format_exc()}",is_error=True)

                # 8. Lipua upya kioni kwa kutumia Clock ili Kivy isikwame (asynchronous rendering)
                Clock.schedule_once(lambda dt: self.render_arch_scene(), 0.01)
                
                ##print(f"✅ Kazi ya mteja ID: {mteja_id} imerejeshwa ikiwa safi peke yake!")
                return True
                
            ##print("⚠️ Hakuna data iliyopatikana kwa ID hii.")
            return False
            
        except Exception as e:
            self.update_status(f"BIM Recovery Error: {traceback.format_exc()}\n{kazi}>>{listi}",True)
            return False



    def get_unique_wood_id(self, base_name):
        """Inakagua scene_objects na kutoa jina la kipekee (e.g., Mlango_1)"""
        if not base_name: base_name = "Mbao"
        
        # 1. Safisha jina (Ondoa namba za mwisho kama mteja aliandika Mlango_1 kwa mkono)
        import re
        base_name = re.sub(r'_\d+$', '', base_name).strip()
        
        # 2. Tafuta namba ya juu kabisa iliyopo uwanjani kwa jina hili
        existing_numbers = [0]
        for obj in self.scene_objects:
            obj_id = str(obj.get('id', ''))
            if obj_id.startswith(base_name):
                # Jaribu kuvuta namba baada ya '_'
                match = re.search(r'_(\d+)$', obj_id)
                if match:
                    existing_numbers.append(int(match.group(1)))
                elif obj_id == base_name:
                    # Kama kuna 'Mlango' pekee, tuchukulie ni namba 0
                    existing_numbers.append(0)
        
        # 3. Namba mpya ni namba ya juu + 1
        next_number = max(existing_numbers) + 1
        return f"{base_name}_{next_number}"

    def sawazisha(self,kipimo,kigao):
        #kigao=1/kigao
        kipimo1=kipimo//kigao
        if kipimo%kigao>0:
            kipimo1+1
        kipimo1=kipimo1*kigao
        return float(kipimo1)

    
    def makundi_ya_mwonekano(self):
        makundi=[]
        marangi={}
        #eneo_m2 = 0
            
        if len (self.scene_objects):      
            for obj in self.scene_objects:
                w, h, d = [float(n) for n in obj['dim']]
                eneo_m2 = 2 * (w*h + w*d + h*d)
                
                if obj.get('asili').lower() == 'mbao' or obj.get('asili').lower() == 'board':
                    color=obj.get('color')
                    if color not in makundi:
                        makundi.append(color)
                    try:
                        marangi[str(color)]['eneo']+=eneo_m2
                        marangi[str(color)]['color']=color
                        for ke in BONGO_WOOD_CATALOG:
                            if BONGO_WOOD_CATALOG[ke]['color'] == color:
                                marangi[str(color)]['jina']=ke
                                #print(f'yes {obj["id"]} >>> {ke}')
                    except:
                        marangi[str(color)]={}
                        try:marangi[str(color)]['eneo']+=eneo_m2
                        except:
                            marangi[str(color)]['eneo']=eneo_m2
                        marangi[str(color)]['color']=color
                        for ke in BONGO_WOOD_CATALOG:
                            if BONGO_WOOD_CATALOG[ke]['color'] == color:
                                marangi[str(color)]['jina']=ke
                                #print(f'yeah {obj["id"]} >>> {ke}')
                                
                    
            self.rangi_zote=marangi
            
        return makundi,marangi

    def badili_rangi(self,button):
        marangi=self.makundi_ya_mwonekano()[0]
        def chagua_rangi():
            self.open_wood_menu(button,True)
        rangi=chagua_rangi()
        
    def badilisha_sasa(self,jina,rangi):
        kutoka=self.previous_color
        for obj in self.scene_objects:
            color=obj.get('color')
            if color == kutoka[1]:
                obj['color']=rangi
                
                #print(obj['id'],kutoka,">>>",rangi)
                self.update_status(f"Vitu vyoote vilivoykuwa vinafanana na rangi ya {kutoka[0]} sasa vinafanana na rangi ya {jina}")
        self.render_arch_scene()
        

    def smam_9zone_perspective_solver(self, obj):
        """
        THE TRUE SPATIAL SOLVER (OPTIMIZED): 
        Inachambua 3D Sector ya Jicho dhidi ya Ubao kwa kutumia Direct Lookups.
        Inarudisha TU nyuso zinazoonekana (Max 3 faces) kuzuia zilizojificha zisionekane!
        """
        try:
            # 1. VUTA DATA ZA KAMERA NA JICHO (Local variables kwa ajili ya speed)
            usawa_wa_jicho = float(self.cam_y)   # cam_y (kimo)
            upande_wa_jicho = float(self.cam_x)  # cam_x (upande)
            mahali_pa_jicho = float(self.cam_z)  # cam_z (kina)
            
            # 2. VUTA MIPAKA HALISI YA UBAO
            dim, pos = obj['dim'], obj['pos']
            w, h, d = float(dim[0]), float(dim[1]), float(dim[2])
            ox, oy, oz = float(pos[0]), float(pos[1]), float(pos[2])

            kushoto = ox 
            kulia = ox + w 
            chini = oy
            juu = oy + h
            nyuma = oz 
            mbele = oz + d 

            # Fallback Default
            face_order = [0]
            sorting_type = "8" 

            # =====================================================================
            # ⚙️ MATRIX KALI YA CHUMA: NYUSO ZINAZOONEKANA TU (HAKUNA STRING ALLOCATIONS)
            # =====================================================================
            
            # -----------------------------------------------------------------
            # SECTOR A: JICHO LIKO JUU YA UBAO (usawa_wa_jicho > juu)
            # -----------------------------------------------------------------
            if usawa_wa_jicho > juu:
                if kushoto < upande_wa_jicho < kulia:
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 4]  # Mbele na Juu tu!
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [1]     # Nyuma tu!
                    else:
                        face_order = [1, 4]  # Nyuma na Juu tu!
                    sorting_type = "7"
                elif upande_wa_jicho > kulia:
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 3, 4]  # Mbele, Kulia, na Juu tu!
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [1, 2, 3]  # Nyuma, Kushoto, na Kulia tu!
                    else:
                        face_order = [1, 3, 4]  # Nyuma, Kulia, na Juu tu!
                    sorting_type = "2"
                else: # upande_wa_jicho < kushoto
                    if mahali_pa_jicho < nyuma:
                        face_order = [4, 0, 2]  # Juu, Mbele, na Kushoto tu!
                        sorting_type = "1"
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [1, 2, 3]  # Nyuma, Kushoto, na Juu tu!
                    else:
                        face_order = [1, 2, 4]  # Nyuma, Kulia, na Juu tu!

            # -----------------------------------------------------------------
            # SECTOR B: JICHO LIKO CHINI YA UBAO (usawa_wa_jicho < chini)
            # -----------------------------------------------------------------
            elif usawa_wa_jicho < chini:
                sorting_type = "-y"
                if kushoto < upande_wa_jicho < kulia:
                    if mahali_pa_jicho < nyuma:
                        face_order = [1]
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [1]
                    else:
                        face_order = [1, 5]  # Nyuma na Chini tu!
                elif upande_wa_jicho > kulia:
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 3, 5]  # Nyuma na Kushoto tu!
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [0, 3, 5]
                    else:
                        face_order = [0, 3, 5]  # Nyuma, Kulia, na Chini tu!
                else: # upande_wa_jicho < kushoto
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 2, 5]  # Mbele, Kushoto, na Chini tu!
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [1, 2, 3]
                    else:
                        face_order = [1, 2, 5]  # Nyuma, Kushoto, na Chini tu!

            # -----------------------------------------------------------------
            # SECTOR C: JICHO LIKO KATIKATI YA KIMO (juu > usawa_wa_jicho > chini)
            # -----------------------------------------------------------------
            else:
                if kushoto < upande_wa_jicho < kulia:
                    sorting_type = "7" if mahali_pa_jicho >= mbele else "8"
                    if mahali_pa_jicho < nyuma:
                        face_order = [0]     # Mbele tu!
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [2]     # Nyuma tu!
                    else:
                        face_order = [1]     # Nyuma tu!
                elif upande_wa_jicho > kulia:
                    sorting_type = "5"
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 3]  # Mbele na Kulia tu!
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [2]     # Kushoto tu!
                    else:
                        face_order = [1, 3]  # Nyuma na Kulia tu!
                else: # upande_wa_jicho < kushoto
                    sorting_type = "6"
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 2]  # Mbele na Kushoto tu!
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [2]     # Kushoto tu!
                    else:
                        face_order = [1, 2]  # Nyuma na Kushoto tu!

            return face_order, sorting_type
            
        except Exception as e:
            import traceback
            self.update_status(f"3d Error: {traceback.format_exc()}", is_error=True)
            return [0], "8"
      
    def smam_9zone_perspective_solver(self, obj):
        """
        THE TRUE SPATIAL SOLVER: Inachambua 3D Sector ya Jicho dhidi ya Ubao,
        inarudisha TU nyuso zinazoonekana (Max 3 faces) kuzuia zilizojificha zisionekane kimakosa!
        """
        try:
            import math
            # 1. VUTA DATA ZA KAMERA NA JICHO (3D World Space)
            usawa_wa_jicho = float(self.cam_y)   # cam_y yako ni usawa/kimo
            upande_wa_jicho = float(self.cam_x)  # cam_x yako ni upande
            mahali_pa_jicho = float(self.cam_z)  # cam_z yako ni kina
            
            # 2. VUTA MIPAKA HALISI YA UBAO (3D Box Bounds)
            dim, pos = obj['dim'], obj['pos']
            w, h, d = float(dim[0]), float(dim[1]), float(dim[2])
            ox, oy, oz = float(pos[0]), float(pos[1]), float(pos[2])

            # Piga rula ya dynamic bounds (Kushoto, Kulia, Juu, Chini, Mbele, Nyuma)
            kushoto = ox 
            kulia = ox + w 
            chini = oy
            juu = oy + h
            nyuma = oz 
            mbele = oz + d 

            # Fallback (Kama jicho lipo sehemu isiyoeleweka chora mbele tu)
            face_order = [0]
            

            # =====================================================================
            # ⚙️ MATRIX KALI YA CHUMA: ILE KODI YAKO HALISI YA TKINTER (Zinazoonekana TU)
            # =====================================================================
            
            # -----------------------------------------------------------------
            # SECTOR A: JICHO LIKO JUU YA UBAO (usawa_wa_jicho > juu)
            # -----------------------------------------------------------------
            if usawa_wa_jicho > juu:
                #ipo chini
                if kushoto < upande_wa_jicho < kulia:
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 4]  # Mbele na Juu tu!
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [1]     # Nyuma tu!
                    else:
                        face_order = [1, 4]  # Nyuma na Juu tu!
                    
                elif upande_wa_jicho > kulia:
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 3, 4]  # Mbele, Kulia, na Juu tu!
                        
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [1, 2, 3]  # Nyuma, Kushoto, na Kulia tu!
                        
                    else:
                        face_order = [1, 3, 4]  # Nyuma, Kulia, na Juu tu!
                    
                else: # upande_wa_jicho < kushoto
                    if mahali_pa_jicho < nyuma:
                        face_order = [4, 0, 2]  # Juu, Mbele, na Kushoto tu!
                        
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [1, 2, 3]  # Nyuma, Kushoto, na Juu tu!
                        
                    else:
                        face_order = [1, 2, 4]  # Nyuma, Kulia, na Juu tu!
                        mipaka={'x':mahali_pa_jicho,'y':usawa_wa_jicho}
                        

            # -----------------------------------------------------------------
            # SECTOR B: JICHO LIKO CHINI YA UBAO (usawa_wa_jicho < chini)
            # -----------------------------------------------------------------
            elif usawa_wa_jicho < chini:
                sorting_type = "-y"
                if kushoto < upande_wa_jicho < kulia:
                    if mahali_pa_jicho < nyuma:
                        face_order = [1]
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [1]
                    else:
                        face_order = [1, 5]  # Nyuma na Chini tu!
                elif upande_wa_jicho > kulia:
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 3, 5]  # Nyuma na Kushoto tu!
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [0, 3, 5]
                    else:
                        face_order = [0, 3, 5]  # Nyuma, Kulia, na Chini tu!
                else: # upande_wa_jicho < kushoto
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 2, 5]  # Mbele, Kushoto, na Chini tu!
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [1, 2, 3]
                    else:
                        face_order = [1, 2, 5]  # Nyuma, Kushoto, na Chini tu!

            # -----------------------------------------------------------------
            # SECTOR C: JICHO LIKO KATIKATI YA KIMO (juu > usawa_wa_jicho > chini)
            # -----------------------------------------------------------------
            else:
                if kushoto < upande_wa_jicho < kulia:

                    sorting_type = "7" if mahali_pa_jicho >= mbele else "8"
                    if mahali_pa_jicho < nyuma:
                        face_order = [0]     # Mbele tu!
                        sorting=f"Tunaanza na zenye nyuso za mbele zenye zilizo mbali (z kubwa)"
                        #print(f"Mbele na Kushoto tu!")
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [2]     # Nyuma tu!
                        sorting=f"Tunaanza na zenye nyuso za mbele zenye zilizo karibu (z ndogo)"
                        #print(f"Mbele na Kushoto tu!")
                    else:
                        #print(f"Sorting yake ni Z mbele yako")
                        face_order = [1]     # Nyuma tu!
                        #print(f"Nyuma tu!")
                elif upande_wa_jicho > kulia:
                    sorting_type = "5"
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 3]  # Mbele na Kulia tu!
                        #print(f"Mbele na Kulia tu!")
                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [2]     # Kushoto tu!
                        #print(f"Kushoto tu!")
                    else:
                        face_order = [1, 3]  # Nyuma na Kulia tu!
                        #print(f"Nyuma na Kulia tu!")
                        
                else: # upande_wa_jicho < kushoto
                    sorting_type = "6"
                    if mahali_pa_jicho < nyuma:
                        face_order = [0, 2]  # Mbele na Kushoto tu!
                        #print(f"Mbele na Kushoto tu!")

                    elif mbele > mahali_pa_jicho > nyuma:
                        face_order = [2]     # Kushoto tu!
                        #print(f"Kushoto tu!")

                    else:
                        face_order = [1, 2]  # Nyuma na Kushoto tu!
                        #print(f"Nyuma na Kushoto tu!")

            return face_order
        except Exception as e:
            self.update_status(f"3d Error: {traceback.format_exc()}",is_error=True)
            return [0]

 
    def render_arch_scene(self, *args):
        """
        THE UNYAMA CAD PIPELINE (PART 1 & 2 - MOBILE ULTRA OPTIMIZED):
        Inabakisha architecture yako yote vilevile lakini inakaza msumari:
        1) Parent-Child Inheritance kupitia parent_id kutoka scene_objects halisi.
        2) Uhakika wa miondoko thabiti (X iwe X, Y iwe Y, Z iwe Z) kwa Sliding na Rotation.
        3) Reference points thabiti kutoka kwenye object kuu pekee.
        """
        if not self.is_constructed: return
        
        try:
            self.canvas.clear()
            from kivy.graphics import Color, Mesh
            
            # Architecture Yako Imetunzwa: Kona 8 na ramani ya nyuso 6 (Kasi ya Tuple)
            v_u = ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),
                   (0, 0, -1), (1, 0, -1), (1, 1, -1), (0, 1, -1))

            shade_factors = {0: 1.0, 1: 0.50, 2: 0.70, 3: 0.70, 4: 0.90, 5: 0.60}
            faces_map = {
                0: (5, 4, 7, 6), 1: (0, 1, 2, 3), 2: (4, 0, 3, 7),
                3: (1, 5, 6, 2), 4: (2, 3, 7, 6), 5: (0, 1, 5, 4)
            }
            
            # 🔥 ENGINE SPEED UP: Local Caching za Variables za Ndani
            cam_x, cam_y, cam_z = self.cam_x, self.cam_y, self.cam_z
            rotate_3d = self.rotate_3d
            project = self.project
            smam_9zone_solver = self.smam_9zone_perspective_solver

            # O(1) Optimization: Ramani ya object zote kwa ID zake kutoka scene_objects kuu
            self.obj_lookup = {obj.get('id'): obj for obj in self.scene_objects if obj.get('id')}

            # 🛠️ KITUO CHA MBINU: Kukokotoa Miondoko kwa Urithi (X, Y, Z Verification)
            def get_transformed_state(object_item):
                pos = object_item['pos']
                dim = object_item['dim']
                
                # Miondoko ya sasa ya object yenyewe (Sliding)
                a = object_item.get("anim", {})
                val = float(a.get("val", 0.0))
                s_vec = object_item.get("slide_vec", (0.0, 0.0, 0.0))
                #print(s_vec)
                # Uhakika wa Miondoko 100%: X iwe X, Y iwe Y, Z iwe Z
                ox = float(pos[0]) + (val * float(s_vec[0]))
                oy = float(pos[1]) + (val * float(s_vec[1]))
                oz = float(pos[2]) + (val * float(s_vec[2]))
                
                # Miondoko ya Mzunguko (Rotation)
                s_rot = object_item.get("static_rot", (0.0, 0.0, 0.0))
                ang = float(a.get("ang_val", 0.0))
                axis = object_item.get("axis", "Y").upper()

                rot_x = float(s_rot[0]) + (ang if axis == "X" else 0.0)
                rot_y = float(s_rot[1]) + (ang if axis == "Y" else 0.0)
                rot_z = float(s_rot[2]) + (ang if axis == "Z" else 0.0)
                
                # PARENT-CHILD INHERITANCE: Mtoto kurithi miondoko yote ya mzazi kwa mzunguko na mteremko
                parent_id = object_item.get('parent')
                if object_item['id'] != parent_id and parent_id !='':
                    current_parent = self.obj_lookup.get(parent_id)
                    while current_parent:
                        print(f"{object_item['id']} != {parent_id}")
                        p_pos=current_parent.get("pos", (0.0, 0.0, 0.0))
                        ox += float(p_pos[0])
                        oy +=float(p_pos[1])
                        oz +=float(p_pos[2])
                        current_parent = self.obj_lookup.get(current_parent.get('parent')) 
                    
                else:
                    current_parent=False
                
                while current_parent:
                    p_a = current_parent.get("anim", {})
                    p_val = float(p_a.get("val", 0.0))
                    p_s_vec = current_parent.get("slide_vec", (0.0, 0.0, 0.0))
                    
                    # 1. Slide ya mzazi inajumlishwa kwenye coordinate zote tatu kulingana na mhimili
                    print(f"Mzazi wa {object_item['id']} ni {parent_id} >>> {ox,oy,oz}")
                    ox += (p_val * float(p_s_vec[0]))
                    oy += (p_val * float(p_s_vec[1]))
                    oz += (p_val * float(p_s_vec[2]))
                    print(f"Mzazi wa {object_item['id']} ni {parent_id} >>> {ox,oy,oz}")
                    
                    # 2. Rotation ya mzazi inajumlishwa kwenye mihimili husika
                    p_s_rot = current_parent.get("static_rot", (0.0, 0.0, 0.0))
                    p_ang = float(p_a.get("ang_val", 0.0))
                    p_axis = current_parent.get("axis", "Y").upper()
                    
                    rot_x += float(p_s_rot[0]) + (p_ang if p_axis == "X" else 0.0)
                    rot_y += float(p_s_rot[1]) + (p_ang if p_axis == "Y" else 0.0)
                    rot_z += float(p_s_rot[2]) + (p_ang if p_axis == "Z" else 0.0)
                    
                    # Tafuta mzazi wa juu zaidi (Kama yupo)
                    current_parent = self.obj_lookup.get(current_parent.get('parent'))
                    if current_parent == '' and current_parent == parent_id:
                        break
                    
                return ox, oy, oz, rot_x, rot_y, rot_z

            # =====================================================================
            # 🛠️ HATUA YA 1: DYNAMIC NON-UNIFORM 3D GRID GENERATION
            # =====================================================================
            g_lines_x = [0.0, cam_x]
            g_lines_y = [0.0, cam_y]
            g_lines_z = [0.0, cam_z]
            self.ii=0
            for obj in self.scene_objects:
                    
                if not obj.get('visible', True): continue
                dim = obj['dim']
                
                # Miondoko iliyonyooka yenye urithi inasomwa hapa kwa ajili ya grid
                ox, oy, oz, _, _, _ = get_transformed_state(obj)
                w_g, h_g, d_g = float(dim[0]), float(dim[1]), float(dim[2])
                
                g_lines_x.extend((ox, ox + w_g))
                g_lines_y.extend((oy, oy + h_g))
                g_lines_z.extend((oz, oz + d_g))
                #self.nextt()
                    
            g_line_z = sorted(g_lines_z)
            grid_groups = {str(i): [[], [], []] for i in range(1, 9)}
            
            # Jaza X (Logic yako ya asili imebaki 100%)
            print(g_lines_y)
            for xx in g_lines_x:
                is_less = xx <= cam_x
                is_greater = xx >= cam_x
                for i in ('1', '4', '5', '8'):
                    if is_less and xx not in grid_groups[i][0]:
                        grid_groups[i][0].append(xx)
                for i in ('2', '3', '6', '7'):
                    if is_greater and xx not in grid_groups[i][0]:
                        grid_groups[i][0].append(xx)

            # Jaza Y (Logic yako ya asili imebaki 100%)
            for yy in g_lines_y:
                is_less = yy <= cam_y
                is_greater = yy >= cam_y
                for i in ('1', '2', '5', '6'):
                    if is_less and yy not in grid_groups[i][1]:
                        grid_groups[i][1].append(yy)
                for i in ('3', '4', '7', '8'):
                    if is_greater and yy not in grid_groups[i][1]:
                        grid_groups[i][1].append(yy)

            # Jaza Z (Logic yako ya asili imebaki 100%)
            for zz in g_lines_z:
                cam__z = cam_z
                is_greater = -1*zz > cam__z  
                is_less = -1*zz <= cam__z
                
                for i in ('1', '2', '3', '4'):
                    if is_greater and zz not in grid_groups[i][2]:
                        grid_groups[i][2].append(zz)
                for i in ('5', '6', '7', '8'):
                    if is_less and zz not in grid_groups[i][2]:
                        grid_groups[i][2].append(zz)

            # Ita sorter kupata mpangilio sahihi wa maboksi
            self.s_sub = self.sorter(self.scene_objects, grid_groups)

            # =====================================================================
            # 🛠️ HATUA YA 2: RENDERING LOOP (KIVY GPU BATCHED)
            # =====================================================================
            with self.canvas:
                for obj in self.s_sub:
                    if not obj.get('visible', True): continue
                    obj['hit_area'] = []
                    dim = obj['dim']
                    
                    w, h, d = float(dim[0]), float(dim[1]), -float(dim[2])
                    
                    # Piga hesabu ya miondoko iliyonyooka yenye urithi kutoka scene_objects kuu
                    ox, oy, oz, rot_cx, rot_cy, rot_cz = get_transformed_state(obj)
                    
                    piv = obj.get('pivot', (0.0, 0.0, 0.0))
                    piv_cx, piv_cy, piv_cz = float(piv[0]), float(piv[1]), float(piv[2])
                    base_color = obj.get('color', [0.8, 0.8, 0.8, 1.0])

                    # Jenga pointi 8 za duniani (World Space Space)
                    world_pts = []
                    for i in range(8):
                        v_u_i = v_u[i]
                        vx = v_u_i[0] * w - piv_cx
                        vy = v_u_i[1] * h - piv_cy
                        vz = -v_u_i[2] * d + piv_cz
                        
                        tx, ty, tz = rotate_3d(vx, vy, vz, rot_cx, rot_cy, rot_cz)
                        world_pts.append((tx + ox + piv_cx, ty + oy + piv_cy, -tz + oz + piv_cz))

                    # 3D Zone & Solver Architecture
                    chora_order = smam_9zone_solver(obj)
                    
                    for f_idx in chora_order:
                        if f_idx not in faces_map: continue
                        indices = faces_map[f_idx]
                        
                        # Projection ya haraka ya pointi 4 za uso (Face)
                        screen_pts_2d = []
                        for idx in indices:
                            pt3d = world_pts[idx]
                            p2d = project(pt3d[0], pt3d[1], pt3d[2])
                            if p2d: screen_pts_2d.append(p2d)
                        
                        # Guard ya Kiume: Chora tu pale Quad inapokamilika pointi zote 4
                        if len(screen_pts_2d) != 4: continue
                        
                        # Shading na Rangi (In-line Float Math)
                        s_factor = shade_factors.get(f_idx, 0.8)
                        c_r = float(base_color[0]) * s_factor
                        c_g = float(base_color[1]) * s_factor
                        # (Hapa chini weka code zako za mwisho za Color na Mesh ya Kivy...)
                        c_b = float(base_color[2]) * s_factor
                        c_a = float(base_color[3]) if len(base_color) > 3 else 1.0
                        
                        # Pakia vertices moja kwa moja kwenye orodha ngumu
                        pt0, pt1, pt2, pt3 = screen_pts_2d[0], screen_pts_2d[1], screen_pts_2d[2], screen_pts_2d[3]
                        block_vertices = [
                            float(pt0[0]), float(pt0[1]), 0.0, 0.0,
                            float(pt1[0]), float(pt1[1]), 0.0, 0.0,
                            float(pt2[0]), float(pt2[1]), 0.0, 0.0,
                            float(pt3[0]), float(pt3[1]), 0.0, 0.0
                        ]
                        obj['hit_area'] = block_vertices
                        
                        # Triangulated indices thabiti bila dynamic extension
                        block_indices =(0,1,2,2,3,0)
                        
                        # Tupa data GPU kwa mpigo mmoja wa Color na Mesh
                        Color(rgba=[c_r, c_g, c_b, c_a])
                        Mesh(vertices=block_vertices, indices=block_indices, mode='triangles')
            self.makundi_ya_mwonekano()
            self.trigger_auto_save()                
        except Exception as e:
            import traceback
            self.update_status(f"Render Error: {traceback.format_exc()}", is_error=True)


  


    def grid_sorter(self, grid, x, y, z):
        """
        THE PRECISION 3D GRID SORTER:
        Inapanga mwelekeo wa gridi dynamic na kusafisha micro-chambers 
        zilizo karibu na x==0 au cam_x ili kuzuia mbao kupotea wakati wa kusogeza jicho.
        """
        x_key = f"x{x}"
        y_key = f"y{y}"
        z_key = f"z{z}"
        
        # 1. Toa data asili za mipaka ya gridi
        g_lines_x = grid[0]
        g_lines_y = grid[1]
        g_lines_z = grid[2]
        
        # 🛠️ AMRI YA DHAHABU: Safisha gridi dhidi ya "Micro-gaps" karibu na 0
        # Kama kuna namba mbili zimekaribiana sana chini ya 0.001, tunaunganisha ili kuzuia mbao kupotea
        def safisha_micro_gaps(lines):
            if len(lines) <= 1: return lines
            s_lines = sorted(list(set([round(n, 4) for n in lines])))
            safi = [s_lines[0]]
            for n in s_lines[1:]:
                if abs(n - safi[-1]) > 0.001:  # Micro-chamber guard clause
                    safi.append(n)
            return safi

        g_lines_x = safisha_micro_gaps(g_lines_x)
        g_lines_y = safisha_micro_gaps(g_lines_y)
        g_lines_z = safisha_micro_gaps(g_lines_z)

        # 2. 🔥 UPANGAJI WA MWLEKEO KULINGANA NA AMRI ZA MHIMILI
        # z1: Descending (Mbali kuja Karibu), z2: Ascending (Karibu kwenda Mbali)
        z1 = sorted(g_lines_z, reverse=False)
        z2 = sorted(g_lines_z, reverse=True)

        # x1: Descending (Kulia kwenda Kushoto), x2: Ascending (Kushoto kwenda Kulia)
        x1 = sorted(g_lines_x, reverse=True)
        x2 = sorted(g_lines_x, reverse=False)

        # y1: Descending (Juu kwenda Chini), y2: Ascending (Chini kwenda Juu)
        y1 = sorted(g_lines_y, reverse=True)
        y2 = sorted(g_lines_y, reverse=False)

        # 3. Jenga Registry ya mwelekeo uliopangwa vizuri
        sortedd = {
            'x1': x1, 'x2': x2, 
            'y1': y1, 'y2': y2, 
            'z1': z1, 'z2': z2
        }
        
        # Inarudisha mfumo ule ule unaotegemewa na sorter_1: [[amri], [data_zilizopangwa]]
        return [[x_key, y_key, z_key], [sortedd[x_key], sortedd[y_key], sortedd[z_key]]]



    def sorter(self, objects, gridi):
        """
        THE AUTO-ADAPTIVE UNIVERSAL 3D CAD SORTER:
        Inapokea sorting_type kutoka smam solver na kupanga gridi dynamic
        ili maboksi ya nyuma/mbali yachorwe kwanza (Painters Algorithm auto-pilot).
        """
        # 1. Nakili data asili za gridi bila kuziharibu

        
        
        # 2. 🔥 AKILI YA BANDIA YA AUTO-GEOMETRY:
        # Panga mwelekeo wa kusafiri kwa loops kulingana na amri ya Solver
        
        # Mhimili wa Z (Kina): Kama kuna '+z' nenda Mbali kuja Karibu (Reverse)
        
        sorting_type=''
        lx = []
        eps = 0.001  # Epsilon guard clause kuzuia float corruption ya maboksi kupotea
        for key in gridi:
            if key == '1':
                #print(f"Mbele kushoto chini {len(gridi[key][0]),len(gridi[key][1]),len(gridi[key][2])}")
                grid=self.grid_sorter(gridi[key],2,2,1)
                ##print(f"sorted grid namba {key} = {grid}")
                objects=self.sorter_1(self.scene_objects,grid[1],grid[0],key)
                
                lx.extend(objects)
                #print(f"\nObjects za  kundi namba {key} ni {list([obj['id'],obj['pos'],obj['dim']] for obj in objects)}\n")
                
            if key == '2':
                #print(f"Mbele kulia chini {len(gridi[key][0]),len(gridi[key][1]),len(gridi[key][2])}")
                grid=self.grid_sorter(gridi[key],1,2,1)
                #print(f"sorted grid namba {key} = {grid}")
                objects=self.sorter_1(self.scene_objects,grid[1],grid[0],key)
                
                lx.extend(objects)
                #print(f"\nObjects za  kundi namba {key} ni {list(obj['id'] for obj in objects)}\n")
            if key == '3':
                #print(f"Mbele kulia juu {len(gridi[key][0]),len(gridi[key][1]),len(gridi[key][2])}")
                grid=self.grid_sorter(gridi[key],1,1,1)
                #print(f"sorted grid namba {key} = {grid}")
                objects=self.sorter_1(self.scene_objects,grid[1],grid[0],key)
                
                lx.extend(objects)
                
                #print(f"\nObjects za  kundi namba {key} ni {list(obj['id'] for obj in objects)}\n")
            if key == '4':
                #print(f"Mbele kushoto juu {len(gridi[key][0]),len(gridi[key][1]),len(gridi[key][2])}")
                grid=self.grid_sorter(gridi[key],2,1,1)
                #print(f"sorted grid namba {key} = {grid}")
                objects=self.sorter_1(self.scene_objects,grid[1],grid[0],key)
                
                lx.extend(objects)
                #print(f"\nObjects za  kundi namba {key} ni {list(obj['id'] for obj in objects)}\n")
            if key == '5':
                #print(f"Nyuma kushoto chini {len(gridi[key][0]),len(gridi[key][1]),len(gridi[key][2])}")
                grid=self.grid_sorter(gridi[key],2,2,2)
                #print(f"sorted grid namba {key} = {grid}")
                objects=self.sorter_1(self.scene_objects,grid[1],grid[0],key)
                
                lx.extend(objects)
                #print(f"\nObjects za  kundi namba {key} ni {list(obj['id'] for obj in objects)}\n")
            if key == '6':
                #print(f"Nyuma kulia chini {len(gridi[key][0]),len(gridi[key][1]),len(gridi[key][2])}")
                grid=self.grid_sorter(gridi[key],1,2,2)
                #print(f"sorted grid namba {key} = {grid}")
                objects=self.sorter_1(self.scene_objects,grid[1],grid[0],key)
                
                lx.extend(objects)
                #print(f"\nObjects za  kundi namba {key} ni {list(obj['id'] for obj in objects)}\n")
            if key == '7':
                #print(f"Nyuma kulia juu {len(gridi[key][0]),len(gridi[key][1]),len(gridi[key][2])}")
                grid=self.grid_sorter(gridi[key],2,1,2)
                #print(f"sorted grid namba {key} = {grid}")
                objects=self.sorter_1(self.scene_objects,grid[1],grid[0],key)
                
                lx.extend(objects)
                #print(f"\nObjects za  kundi namba {key} ni {list(obj['id'] for obj in objects)}\n")
            if key == '8':
                #print(f"Nyuma kushoto juu {len(gridi[key][0]),len(gridi[key][1]),len(gridi[key][2])}")
                grid=self.grid_sorter(gridi[key],1,1,2)
                #print(f"sorted grid namba {key} = {grid}")
                objects=self.sorter_1(self.scene_objects,grid[1],grid[0],key)
                
                lx.extend(objects)
                #print(f"\nObjects za  kundi namba {key} ni {list(obj['id'] for obj in objects)}\n")
                                            
        return lx


    def smam_9zone_helper_call(self, obj, solver_ref):
        """Helper ya haraka kupata zone bila kuathiri mtiririko wako."""
        return solver_ref(obj)


    def sorter_1(self,objects,grid,lst,grp):
        xx,yy,zz=lst
        sub=[]
        g_lines_z=grid[2]
        g_lines_y=grid[1]
        g_lines_x=grid[0]
        lx=[]
        
        for z in range(len(g_lines_z)-1):#(2):
            #z=-z-2
            if zz == 'z1':
                zzz0, zzz1 = z, z+1  
            else:
                zzz0, zzz1 = z+1, z 
            
            z_face=False
            z_0=g_lines_z[zzz0]
            z_1=g_lines_z[zzz1]
            kina=z_1-z_0
            #kina=z_1-z_0 if kina>0 else z_0-z_1
            #if kina<0: z_0=z_1
            #print('                                                     ')
            
            for x in range(len(g_lines_x )-1):
                #x=-x-2
                x_face=False
                if xx == 'x2':
                    xxx0, xxx1 = x, x+1  
                else:
                    xxx0, xxx1 = x+1, x
                x_0=g_lines_x[xxx0]
                x_1=g_lines_x[xxx1]
                upana=x_1-x_0
                upana=x_1-x_0 if upana > 0 else x_0-x_1
                if x_0>x_1:print(f"xx = {xx}\n    x0 = {x_0}\n    x1 = {x_1}\n    upana = {upana}")
                                
                for y in range(len(g_lines_y )-1):
                    y_face=False
                    if yy == 'y2':
                        yyy0, yyy1 = y, y+1  
                    else:
                        yyy0, yyy1 = y+1, y 
                    y_0=g_lines_y[yyy0]
                    y_1=g_lines_y[yyy1]
                    urefu=y_1-y_0
                    urefu=y_1-y_0 if urefu > 0 else y_0-y_1
                    
                    for obj in objects:
                        #print(obj['id'])
                        parent_id = obj['parent']
                        #print(sub_['id'],sub_['parent'])
                        if obj['id'] != parent_id and parent_id !='':
                            current_parent = self.obj_lookup[parent_id]
                            ox,oy,oz=0,0,0
                            posp={}
                            while current_parent:
                                p_pos=current_parent.get("pos", (0.0, 0.0, 0.0))
                                posp[current_parent.get("id")]=p_pos
                                
                                print('+++++++',obj,'\n    ',current_parent)
                                if current_parent['parent'] != '':
                                    current_parent = self.obj_lookup[current_parent.get('parent')]
                                else:
                                    print('zuuummmmm',posp) 
                                    break
                            for p in posp:
                                ox += float(posp[p][0])
                                oy +=float(posp[p][1])
                                oz +=float(posp[p][2])
                            print(ox,oy,oz)
                            #sub_['pos']=[x_0+ox,y_0+oy,z_0+oz]
                            '''if obj['pos'][2]+oz<=z_0 and obj['pos'][2]+oz+obj['dim'][2]>=z_1:#
                                if obj['pos'][0]+ox<=x_0 and obj['pos'][0]+ox+obj['dim'][0]>=x_1:#
                                    if obj['pos'][1]+oy<=y_0 and obj['pos'][1]+oy+obj['dim'][1]>=y_1:# '''
                            print(obj['pos'],obj['dim'],x_0,x_1,y_0,y_1,z_0,z_1)
                            if obj['pos'][2]+oz<=z_0 and obj['pos'][2]+oz+obj['dim'][2]>=z_1:#
                                if obj['pos'][0]+ox<=x_0 and obj['pos'][0]+ox+obj['dim'][0]>=x_1:#
                                    if obj['pos'][1]+oy<=y_0 and obj['pos'][1]+oy+obj['dim'][1]>=y_1:            
                                        if obj not in lx:
                                            sub_={}
                                            for i in obj:
                                                sub_[i]=obj[i]
                                            sub_['id']=f"{obj['id']}.{len(lx)+1}"
                                            
                                            
                                            sub_['pos']=[x_0-ox,y_0-oy,z_0-oz]
                                            sub_['dim']=[upana,urefu,kina]
                                            print('\n',sub_['id'],'>>>',sub_)
                                            lx.append(sub_)
                        else:
                            if obj['pos'][2]<=z_0 and obj['pos'][2]+obj['dim'][2]>=z_1:#
                                if obj['pos'][0]<=x_0 and obj['pos'][0]+obj['dim'][0]>=x_1:#
                                    if obj['pos'][1]<=y_0 and obj['pos'][1]+obj['dim'][1]>=y_1:# 
                                        #print('\n',obj['id'])
                                        if obj not in lx:
                                            sub_={}
                                            for i in obj:
                                                sub_[i]=obj[i]
                                            sub_['id']=f"{obj['id']}.{len(lx)+1}"
                                            
                                            
                                            sub_['pos']=[x_0,y_0,z_0]
                                            sub_['dim']=[upana,urefu,kina]
                                            lx.append(sub_)
        '''obj=self.objct
        self.lx=[
            {'id':f"{obj['id']}.{len(lx)+1}",'pos':[x_0,y_0,z_0],'dim':[upana,urefu,kina] for obj in self.objct() }
        ]                                
        def objct(self,obj):
            if obj['pos'][2]<=z_0 and obj['pos'][2]+obj['dim'][2]>=z_1:#
                if obj['pos'][0]<=x_0 and obj['pos'][0]+obj['dim'][0]>=x_1:#
                    if obj['pos'][1]<=y_0 and obj['pos'][1]+obj['dim'][1]>=y_1:# 
                        if obj not in self.lx
            return obj '''                               
                                        #print(grp,lst,z_0,z_1,self.cam_z-z_0)
        #print('\n')                   
                                    
                    
                    
                                
        #for obj in lx:print(obj['id'])                   
        return   lx            

    def piga_picha(self, *args):
        """
        THE CAD SCREENSHOT ENGINE:
        Inachukua kile kilichochorwa sasa hivi kwenye kioo na kukihifadhi
        kwenda kwenye faili la picha (.png) tayari kwa kumtumia mteja.
        """
        import os
        from kivy.app import App
        from datetime import datetime
        from PIL import Image as img
        from PIL import ImageChops

        try:
            # 1. Pata folder salama la kuhifadhia picha kwenye simu
            app = App.get_running_app()
            
            # Unaweza kutumia folder lile lile la database yako
            folder_la_picha = app.db_path 
            
            # 2. Tengeneza jina la picha kwa kutumia jina la mteja na muda halisi
            jina_la_mteja = getattr(self, 'current_mteja', 'Mteja_Mpya').replace(" ", "_")
            muda_sasa = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            jina_la_faili = f"Mchoro_wa_kazi_ya_{jina_la_mteja}_{self.project_name}_{muda_sasa}.png"
            njia_kamili = os.path.join(folder_la_picha, jina_la_faili)
            

            # 3. AMRI YA UNYAMA: export_to_png inafanya kazi kwenye widget yenyewe (self)
            # Inachukua pixel zote za canvas na kuzisave kiatomatiki
            self.export_to_png(njia_kamili)
            try:
                im=img.open(njia_kamili)
                im.convert('RGB')
                b_g=img.new(im.mode,im.size,im.getpixel((0,0)))
                dff=ImageChops.difference(im,b_g)
                dff=ImageChops.add(dff,dff,2.0,-100)
                box = im.getbbox()
                picha=im.crop(box)
                picha.save(njia_kamili)
                self.camera.append(njia_kamili)
            except:
                import traceback
                error_kamili = traceback.format_exc()
                self.update_status(f"Imeshindikana kucrop picha mchoro!{error_kamili}", is_error=True)
                self.camera.append(njia_kamili)


            # 4. Toa ujumbe kwenye screen kuwa picha imehifadhiwa
            ujumbe = f"Mchoro wako ameuhifadhi hapo >>>\nJina: {njia_kamili}\n\n\n"
            
            self.update_status(f"{random.choice(app.fundi)} ametwanga picha ya huo mchoro tayari!!!\n {ujumbe}\n")
            
            # Kama una ile popup ya error, unaweza kuitumia hata hapa kuonyesha mafanikio!
            if hasattr(self, 'onyesha_error_popup'):
                # Tunaiita tu kuonyesha ujumbe wa kawaida
                self.onyesha_error_popup(f"🎉 MAFANIKIO!\n\nMchoro wa mteja umepigwa picha na kuhifadhiwa kikamilifu.\n\nNjia: {njia_kamili}\n\nSasa unaweza kwenda kwenye File Manager na kumtumia mteja.")

        except Exception as e:
            import traceback
            error_kamili = traceback.format_exc()
            
            self.update_status(f"Imeshindikana kupiga picha mchoro!{error_kamili}", is_error=True)

        
    def tengeneza_pdf_quotation(self, njia_ya_picha_3d=None, *args):
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.utils import ImageReader
        """
        THE UNYAMA QUOTATION & PDF ENGINE:
        Inachukua vipimo, bei za mbao, na picha ya mchoro wa 3D,
        kisha inatengeneza faili la PDF la quotation kitaalamu sana.
        """
        import os
        from kivy.app import App
        from datetime import datetime
        
        # Vuta ReportLab components
        

        try:
            app = App.get_running_app()
            jina_la_mteja = getattr(self, 'current_mteja', 'Mteja_Mpya')
            muda_sasa = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 1. Njia ya kuhifadhi PDF (Kwenye folder salama la app)
            jina_la_pdf = f"Quotation_{jina_la_mteja.replace(' ', '_')}_{muda_sasa}.pdf"
            njia_kamili_pdf = os.path.join(app.db_path, jina_la_pdf)
            
            # 2. Set up Document
            doc = SimpleDocTemplate(
                njia_kamili_pdf, 
                pagesize=A4,
                rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20
            )
            
            story = []
            styles = getSampleStyleSheet()
            
            # Styles za Maandishi
            kichwa_style = ParagraphStyle(
                'TitleStyle', parent=styles['Heading1'], 
                fontSize=12, textColor=colors.HexColor(0xD2691E), spaceAfter=10,alignment=1
            )
            kawaida_style = styles['Normal']
            kawaida_style.fontSize = 11
            
            # --- TANDIKA HEADER YA QUOTATION ---
            upan,uref=ImageReader('smam_wood_logo.png').getSize()
            uref_mpya=100
            upan_mpya=(upan/uref)*uref_mpya
            logo=Image('smam_wood_logo.png',width=upan_mpya,height=uref_mpya)
            story.append(logo)
            story.append(Paragraph(f"<b>QUOTATION YA KAZI YA {jina_la_mteja.upper()}!!!</b>", kichwa_style))
            
            for njia in njia_ya_picha_3d:
                if njia and os.path.exists(njia):
                    prgf=Paragraph(f"<b>MUONEKANO WA {self.project_name}</b> \nMCHORO NAMBA_{njia_ya_picha_3d.index(njia)+1}", styles['Heading2'])
                    story.append(prgf)
                    story.append(Spacer(1, 5))                
                    upana,urefu=ImageReader(njia).getSize()
                    urefu_mpya=800 - 40 -sum([p.wrap(doc.width,doc.height)[1] for p in story[0:story.index(prgf)]]) #canvas._pageTemlate.frames[0]._getAvilableWidthAndHeight()[1]
                    print(uref_mpya)
                    if urefu_mpya>400:
                        if urefu>upana:
                            upana_mpya=(upana/urefu)*urefu_mpya
                        else:
                            upana_mpya=(urefu/upana)*urefu_mpya
                    else:
                        urefu_mpya= 700
                        upana_mpya=(upana/urefu)*urefu_mpya
                    #logo=
                    # ReportLab Image (Njia ya picha, upana wa picha, kimo cha picha)
                    # Tunapunguza width hadi 450 ili itoshee vizuri ndani ya ukurasa wa PDF bila kuvuka mipaka
                    picha_pdf = Image(njia, width=upana_mpya, height=urefu_mpya)
                    picha_pdf.preserveAspectRatio = True  # Inalinda height isibonyezwe
                    picha_pdf.mask = 'auto'                # Inazuia rangi za background kuvurugika

                    story.append(picha_pdf)
                else:
                    story.append(Paragraph("<i>(Picha ya mchoro haikuambatishwa)</i>", kawaida_style))
            table_data = [
                ["No:","Malighafi", "Kiasi/idadi", "@_Thamani", "Gharama (TSH)"],
            ]
            
            jumla_ya_bei = 0
            mahitaji=self.mahesabu.mahitaji
            for indx,hitaji in enumerate(mahitaji):
                kiasi=mahitaji[hitaji]['idadi']
                thamani=mahitaji[hitaji]['thamani']
                gharama=mahitaji[hitaji]['gharama']
                jumla_ya_bei += gharama
                table_data.append([indx+1,hitaji, kiasi, thamani, gharama])
                
            # Mstari wa mwisho wa Jumla kuu
            table_data.append(["","Jumla ya mahitaji:", ">>>>>>", "", f"{round(jumla_ya_bei,0):,} TSH"])
            table_data.append(["","UFUNDI:", f"{round(jumla_ya_bei/3,0):,} TSH", "JUMLA KUU:", f"{round(jumla_ya_bei*4/3,0):,} TSH"])
            
            if self.eneo_>1.75:rpot=f"Hapo juu ni mwonekano wa {self.project_name} na ni kazi ya {jina_la_mteja} kutoka {self.project_location} yenye thamani ya shilingi {round(jumla_ya_bei*4/3,0):,} kulingana na tathmini iliyofanyika tarehe {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            else:rpot=f"Hapo juu ni mwonekano wa {self.project_name} na ni kazi ya {jina_la_mteja} kutoka {self.project_location} yenye thamani ya shilingi {round(jumla_ya_bei*4/3,0):,} kulingana na tathmini iliyofanyika tarehe {datetime.now().strftime('%d/%m/%Y %H:%M')}\nLakini Fundi Stany anasema kiwango cha kupulizia rangi ni kidogo kiasi kwamba mwonekano wa  rangi hautokolea sana, hivyo basi yeye anakushauri  uongeze kiasi cha rangi ili kuweza kupulizia angalau coat 2 ili kupata mwonekano wa rangi uliokolea"
            story.append(Paragraph(rpot, kawaida_style))
            
            story.append(Spacer(3, 15))
            
            # --- TANDIKA TABLE YA BEI NA MBAO (SAMPLE DATA) ---
            # Hapa unaweza kuvuta data halisi kutoka kwenye self.scene_objects yako!
            
            # Jenga Table yenyewe yenye muonekano wa kisasa
            quoter_table = Table(table_data, colWidths=[30,240, 70, 100, 110])
            quoter_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(0xD2691E)), # Rangi ya bluu juu ya table
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -3), colors.HexColor("#F5F5F5")), # Kivuli kwenye data
                ('GRID', (0, 1), (-1, -3), 0.5, colors.grey),
                ('FONTNAME', (0, -2), (1, -1), 'Helvetica-Bold'), # Bold kwenye Jumla Kuu
                ('TEXTCOLOR', (0, -2), (1, -1), colors.HexColor(0x008000)), # Jumla iwe nyekundu
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor(0xD2691E)), # Rangi ya bluu juu ya table
                ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'), # Bold kwenye Jumla Kuu
                ('TEXTCOLOR', (-2, -1), (-1, -1), colors.HexColor(0x00BFFF)), # Jumla iwe nyekundu
            ]))
            
            story.append(quoter_table)
            #story.append(Spacer(1, 20))
            
            # --- 🔥 AMRI YA DHAHABU: AMBATISHA PICHA YA MCHORO WA 3D ---
                
            # 5. Jenga faili la PDF kabisa
            story.append(Paragraph("<i>Maximum Quality - Minimum price!</i>", kawaida_style))
            #story.append(Paragraph("<i>()</i>", kawaida_style))
            doc.build(story)
            
            # Toa popup ya mafanikio
            if hasattr(self, 'update_status'):
                self.update_status(
                    f"🎉 QUOTATION TAYARI!\n\nPDF imetengenezwa na picha imeambatishwa kikamilifu.\n\n"
                    f"Njia: {njia_kamili_pdf}\n\nSasa unaweza kwenda kuituma kwa mteja."
                )
                
        except Exception as e:
            import traceback
            error_kamili = traceback.format_exc()
            print(error_kamili)
            self.update_status(f"Kosa la PDF Engine:\n{error_kamili}")


    def bonyeza_tengeneza_quotation(self, *args):
        """Inaitwa na kitufe cha App kufanya kila kitu kwa mpigo"""
        import os
        from kivy.app import App
        
        # 1. Piga kwanza picha ya canvas ya 3D sasa hivi na uipate njia yake (path)
        app = App.get_running_app()
        jina_la_mteja = getattr(self, 'current_mteja', 'Mteja').replace(" ", "_")
        
        # Hii lazima ifuate muundo ule ule ulioamua kusave picha yako kule juu
        picha_path = os.path.join(app.db_path, f"Mchoro_Sasa_{jina_la_mteja}.png")
        
        # Save picha ya sasa hivi juu ya kioo
        self.export_to_png(picha_path)
        
        # 2. Pasha hii picha kwenda kwenye engine ya PDF ili iambatanishwe chini ya table!
        self.tengeneza_pdf_quotation(self.camera)

    def duara(self,pos,dim,axis='y', microbox=100):
        bx,by,bz=pos
        up,ur,un=dim
        step=microbox
        micro_dim=(step,step,step)

        vibox=[]
        if axis.upper()=='Y':
            center_x=bx + (up/2)
            center_z=bz + (un/2)
            radius=min(up,ur)/2

            x_steps=int(up/step)
            z_steps=int(un/step)
            y_steps=max(1,int(ur/step))

            for xi in range(x_steps):
                x_pos= bx + (xi * step) + (step /2)
                for zi in range(z_steps):
                    z_pos= bz + (zi * step) + (step /2)
                    if ((x_pos - center_x) ** 2 + (z_pos - center_z) ** 2)<= (radius ** 2):
                        for yi in range(y_steps):
                            y_pos = by + (yi * step)
                            pos_xyz=(x_pos - step/2,y_pos,z_pos - step/2)
                            vibox.append((micro_dim,pos_xyz))
        return vibox

    def single_axis_multiply(self,object,axis=0,interval=1000,raange=7):
        axis=int(axis)
        self.mhimili=axis
        import re
        def generate_unique_id(base_name):
            base = re.sub(r'_\d+$', '', base_name).strip() or "Ubao"
            existing_numbers = [-1]
            for obj in getattr(self, 'scene_objects', []):
                obj_id = str(obj.get('id', ''))
                if obj_id.startswith(base):
                    match = re.search(r'_(\d+)$', obj_id)
                    if match: existing_numbers.append(int(match.group(1)))
                    elif obj_id == base: existing_numbers.append(0)
            return (f"{base}_{max(existing_numbers) + 1}")
        pos=0
        mm={}
        self.rudia={}
        self.i=1
        self.scene_objects_mrudio=[]
        def zalisha(obj,ax,intv):
            kt={}
            
            obj['id']=generate_unique_id(id)
            for k in obj:
                kt[k]=obj[k]
                
            self.scene_objects_mrudio.append(kt)
            self.rudia[obj['id']]=intv
            self.is_constructed=True
            print(kt)
            self.i+=1
        id=object['id']
        self.poss=object['pos'][axis]
        i=1
        '''while self.i <= raange:
            zalisha(object,axis,interval)#Clock.schedule_once(lambda dt:zalisha(object,axis,interval,self.i),0)
            i+=1
            if self.i > raange:
                break
                self.i=0
        '''
        for ii in range (raange):
            pos = (ii+1)*int(interval)
            zalisha(object,axis,pos)#Clock.schedule_once(lambda dt:zalisha(object,axis,interval,self.i),0)
            
        
        self.f_marudio.text='0'    
        print(self.rudia)