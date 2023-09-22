import streamlit as st
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.client.auth import create_stub
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2
from clarifai.client.user import User

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
stub = create_stub(auth)
userDataObject = auth.get_user_app_id_proto()

st.title("Simple example to list inputs")

with st.form(key="data-inputs"):
  mtotal = st.number_input(
      "Select number of inputs to view in a table:", min_value=10, max_value=100)
  submitted = st.form_submit_button('Submit')

if submitted:
  if mtotal is None or mtotal == 0:
    st.warning("Number of inputs must be provided.")
    st.stop()
  else:
    st.write("Number of inputs in table will be: {}".format(mtotal))

  # Stream inputs from the app. list_inputs give list of dictionaries with inputs and its metadata .
  input_obj = User(user_id=userDataObject.user_id).app(app_id=userDataObject.app_id).inputs()  
  all_inputs=input_obj.list_inputs()

#added "data_url" which gives the url of the input.
  data = []
  for inp in all_inputs:
    data.append({
        "id": inp.id,
        "data_url":inp.data.text.url,
        "status": inp.status.description,
        "created_at": timestamp_pb2.Timestamp.ToDatetime(inp.created_at),
        "modified_at": timestamp_pb2.Timestamp.ToDatetime(inp.modified_at),
        "metadata": json_format.MessageToDict(inp.data.metadata),
    })

  st.dataframe(data)
