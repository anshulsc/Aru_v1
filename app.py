import openai
import streamlit as st
import subprocess
import urllib.parse

openai.api_key = "EMPTY" # Key is ignored and does not matter
openai.api_base = "http://34.132.127.197:8000/v1"

# Report issues
def raise_issue(e, model, prompt):
    issue_title = urllib.parse.quote("[bug] Hosted Gorilla: <Issue>")
    issue_body = urllib.parse.quote(f"Exception: {e}\nFailed model: {model}, for prompt: {prompt}")
    issue_url = f"https://github.com/ShishirPatil/gorilla/issues/new?assignees=&labels=hosted-gorilla&projects=&template=hosted-gorilla-.md&title={issue_title}&body={issue_body}"
    print(f"An exception has occurred: {e} \nPlease raise an issue here: {issue_url}")

#Query Gorilla Server
def get_gorilla_response(prompt="I would like to translate from English to French.", model="gorilla-7b-hf-v1"):
  try:
    completion = openai.ChatCompletion.create(
      model=model,
      messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
  except Exception as e:
    raise_issue(e, model, prompt)


def extract_code_from_output(output):
    if output:
        code = output.split("code>>>:")[1]
        return code
    else:
        return "No code found in output."

def run_generated_code(file_path):

    # Command to run the generated code using Python interpreter
    command = ["python3", file_path]

    try:
        # Execute the command as a subprocess and capture the output and error streams
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the subprocess ran successfully
        if result.returncode == 0:
            st.success("Generated code executed successfully.")
            # Display the output of the generated code
            st.code(result.stdout, language="python")
        else:
            st.error("Generated code execution failed with the following error:")
            # Display the error message
            st.code(result.stderr, language="bash")
    
    except Exception as e:
        st.error("Error occurred while running the generated code:", e)

st.set_page_config(layout="wide")

def main():
    st.title("LLM API CALLS")

    input_prompt = st.text_area("Enter your prompt below:")
    api_provider = st.radio("Select an API Provider:", ("Huggingface", "Torch Hub", "TensorFlow Hub"))
    option = ""
    if api_provider == "Huggingface":
        option = st.selectbox("Select a model:", ("gorilla-7b-hf-v1", "gorilla-mpt-7b-hf-v0"))
    elif api_provider == "Torch Hub":
        option = st.selectbox("Select a model:", ("gorilla-7b-th-v0", "gorilla-mpt-7b-th-v0"))
    elif api_provider == "TensorFlow Hub":
        option = st.selectbox("Select a model:", ("gorilla-7b-tf-v0", "gorilla-mpt-7b-tf-v0"))

    result = ""
    if st.button("Run Inference"):
        if len(input_prompt) > 0:
            col1, col2 = st.columns([1,1])
            with col1:
                if option in ["gorilla-7b-hf-v1", "gorilla-7b-th-v0", "gorilla-7b-tf-v0"]:
                    result = get_gorilla_response(prompt=input_prompt, model=option)
                    st.write(result)
                elif option in ["gorilla-mpt-7b-hf-v0", "gorilla-mpt-7b-th-v0", "gorilla-mpt-7b-tf-v0"]:
                    result = get_gorilla_response(prompt=input_prompt, model=option)
                    st.write(result)


            with col2:
                # pass
                if option in ["gorilla-7b-hf-v1", "gorilla-7b-th-v0", "gorilla-7b-tf-v0"]:
                    code_result = extract_code_from_output(result)
                    st.subheader("Generated Output")
                    st.code(code_result, language='python')
                    file_path = f"generated_code_{option.replace('-', '_')}.py"
                    with open(file_path, 'w') as file:
                        file.write(code_result)

                elif option in ["gorilla-mpt-7b-hf-v0", "gorilla-mpt-7b-th-v0", "gorilla-mpt-7b-tf-v0"]:
                    code_result = extract_code_from_output(result)
                    lines = code_result.split('\\n')
                    for i in range(len(lines)-1):
                        st.code(lines[i], language='python')
                    file_path = f"generated_code_{option.replace('-', '_')}.py"
                    with open(file_path, "w") as f:
                        for i in range(len(lines)-1):
                            f.write(lines[i].strip().replace('\\"', '"') + '\n')
                run_generated_code(file_path)

if __name__ == "__main__":
    main()
