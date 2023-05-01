import glob
import os

import streamlit as st

from clarifai_utils.modules.css import ClarifaiStreamlitCSS

st.set_page_config(layout="wide")

ClarifaiStreamlitCSS.insert_default_css(st)

st.markdown("Please select a specific page by adding it to the url")

cols = st.columns(10)

qp = st.experimental_get_query_params()
qpstr = ""
for k, v in qp.items():
  qpstr += "{}={}&".format(k, v[0])

d = os.path.dirname(__file__)
for fi, f in enumerate(glob.glob(os.path.join(d, "pages", "*.py"))):
  name = os.path.splitext(os.path.basename(f))[0]
  ClarifaiStreamlitCSS.buttonlink(cols[fi % len(cols)], name, "/" + name + '?' + qpstr)
