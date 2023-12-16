import openai
import urllib.parse
import streamlit as st

openai.api_key = "EMPTY" # Key is ignored and does not matter
openai.api_base = "http://34.132.127.197:8000/v1"

# Report issues
def raise_issue(e, model, prompt):
    issue_title = urllib.parse.quote("[bug] Hosted Gorilla: <Issue>")
    issue_body = urllib.parse.quote(f"Exception: {e}\nFailed model: {model}, for prompt: {prompt}")
    issue_url = f"https://github.com/ShishirPatil/gorilla/issues/new?assignees=&labels=hosted-gorilla&projects=&template=hosted-gorilla-.md&title={issue_title}&body={issue_body}"
    print(f"An exception has occurred: {e} \nPlease raise an issue here: {issue_url}")

# Query Gorilla server 
def get_gorilla_response(prompt="I would like to translate from English to French.", api_provider="Huggingface"):
  try:
    model = "gorilla-7b-hf-v0"
    if api_provider == "Huggingface":
      model = "gorilla-7b-hf-v0"
    if api_provider == "Torch Hub":
      model = "gorilla-7b-th-v0"
    if api_provider == "TensorFlow Hub":
      model = "gorilla-7b-tf-v0"

    completion = openai.ChatCompletion.create(
      model=model,
      messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
  except Exception as e:
    raise_issue(e, model, prompt)

st.title("Try Gorilla 🦍")
st.write("Large Language Model Connected with Massive APIs")    
st.markdown('* Read about this demo here: [Medium](https://medium.com/@dan.avila7/try-gorilla-a-large-language-model-connected-with-massive-apis-442f3b554ffb)')
st.markdown('* All code was written with the help of CodeGPT (https://codegpt.co)')

st.write('---')
col1, col2 = st.columns(2)
with col1:
  api_provider = st.radio("Select an API Provider:", ("Huggingface", "Torch Hub", "TensorFlow Hub"))
with col2:
  input = st.text_input("Ask here:")
  st.write("Example: I would like to translate from English to French.")
  
if api_provider and input:
    if st.button("Run Gorilla"):
      with st.spinner('Loading...'):
        st.success(get_gorilla_response(input, api_provider))