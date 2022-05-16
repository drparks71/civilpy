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

import folium

m = folium.Map([40.151449, -82.595882], zoom_start=8)

folium.Marker(
    location=[39.967248, -83.006980],
    tooltip="Click me!",
    popup="Michael Baker Intl. - Columbus",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.Marker(
    location=[41.503252, -81.686686],
    tooltip="Click me!",
    popup="Michael Baker Intl. - Cleveland",
    icon=folium.Icon(color="green"),
).add_to(m)

folium.Marker(
    location=[40.799164, -81.376457],
    tooltip="Click me!",
    popup="Michael Baker Intl. - Canton",
    icon=folium.Icon(color="green"),
).add_to(m)

folium.Marker(
    location=[39.112037, -84.515471],
    tooltip="Click me!",
    popup="Michael Baker Intl. - Cincinnati",
    icon=folium.Icon(color="green"),
).add_to(m)

# full_run_time_start = time.time()
#
# url = 'https://services3.arcgis.com/6LvtIYUSMXW8Tb6o/ArcGIS/rest/services'
#
# # reference map service
# ags = restapi.ArcServer(url)
#
#
# metra_lines = ags.getService('metra_lines_2018/FeatureServer')
# lines = metra_lines.layer(0)
# featureSet = lines.query(exceed_limit=True)
#
# df = gpd.read_file(str(featureSet.json))
#
# m = df.explore(
#     column='LINE_NAME',
#     style_kwds={'weight':5},
#     legend='LINE_NAME',
#     legend_kwds={
#         "caption": "Metra Lines"
#     }
# )
