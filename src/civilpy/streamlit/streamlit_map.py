"""
CivilPy
Copyright (C) 2019 - Dane Parks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Import necessary modules
import folium
import geopandas as gpd
import streamlit as st
from folium.plugins import Geocoder
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# Set filepath
fp = r"C:\Users\dane.parks\PycharmProjects\civilpy\Notebooks\res\MapData\Wetland.shp"

# Read file using gpd.read_file()
data = gpd.read_file(fp)

m = data.explore(
    marker_kwds=dict(
        radius=8,
        fill=True,
        icon=folium.map.Icon(color="black", prefix="fa", icon="building"),
    ),
    marker_type="marker",
)
Geocoder().add_to(m)
st_data = st_folium(m, width=1700, height=800)
