import tkinter as tk
from tkinter import ttk
import keyring
import webbrowser
import openai
import os
import tempfile
import subprocess
from sigma.config.collection import SigmaConfigurationManager
from sigma.configuration import SigmaConfiguration
import os
import platform
import git

def download_sigma_repo():
    home_dir = os.path.expanduser('~')
    sigma_dir = os.path.join(home_dir, 'sigma')

    if not os.path.exists(sigma_dir):
        print("Cloning Sigma repository...")
        git.Repo.clone_from('https://github.com/SigmaHQ/legacy-sigmatools', sigma_dir)
        print("Sigma repository cloned successfully")

    config_dir = os.path.join(sigma_dir, 'tools', 'config')
    return config_dir

config_path = download_sigma_repo()

def get_config_file(target):
    config_file_name = f"{target}.yml"
    config_file_path = os.path.join(config_path, config_file_name)

    if os.path.isfile(config_file_path):
        return config_file_path
    else:
        print(f"Configuration file not found for target '{target}'.")
        return None

def save_api_key():
    api_key = api_key_entry.get()
    keyring.set_password("SigmaRuleCreator", "OpenAI_API_Key", api_key)
    api_key_entry.delete(0, 'end')


def generate_sigma_rule():
    api_key = keyring.get_password("SigmaRuleCreator", "OpenAI_API_Key")
    openai.api_key = api_key

    user_input = user_prompt_entry.get()

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        n=1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate a Sigma Rule for {user_input}"},
        ])

    message = response.choices[0]['message']
    generated_rule = "{}: {}".format(message['role'], message['content'])

    sigma_rule_text.delete(1.0, tk.END)
    sigma_rule_text.insert(tk.END, generated_rule)


def get_conversion_targets():
    raw_targets = subprocess.check_output(["sigmac", "--lists"]).decode("utf-8").splitlines()
    targets = [t.split(':')[0].strip() for t in raw_targets]
    conversion_target_menu["values"] = targets

def generate_target_rule():
    target = conversion_target_menu.get()
    config_file = get_config_file(target)

    if not config_file:
        print(f"No configuration file found for target '{target}'.")
        return

    sigma_rule = sigma_rule_text.get(1.0, tk.END)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
        with open(temp_file_path, "w") as f:
            f.write(sigma_rule)

    try:
        target_rule = subprocess.check_output(["sigmac", temp_file_path, "-t", target, "--config", config_file]).decode("utf-8")
    finally:
        os.unlink(temp_file_path)

    target_rule_text.delete(1.0, tk.END)
    target_rule_text.insert(tk.END, target_rule)


root = tk.Tk()
root.title("Sigma Rule Creator")

api_key_label = tk.Label(root, text="OpenAI API Key:")
api_key_label.grid(column=0, row=0)
api_key_entry = tk.Entry(root)
api_key_entry.grid(column=1, row=0)

save_key_button = tk.Button(root, text="Save API Key", command=save_api_key)
save_key_button.grid(column=2, row=0)

user_prompt_label = tk.Label(root, text="Create a Sigma Rule that does:")
user_prompt_label.grid(column=0, row=1)
user_prompt_entry = tk.Entry(root)
user_prompt_entry.grid(column=1, row=1)

generate_button = tk.Button(root, text="Generate Sigma Rule", command=generate_sigma_rule)
generate_button.grid(column=2, row=1)

generated_rule_label = tk.Label(root, text="Generated Sigma Rule:")
generated_rule_label.grid(column=0, row=2)
sigma_rule_text = tk.Text(root, wrap=tk.WORD)
sigma_rule_text.grid(column=1, row=2)

conversion_target_label = tk.Label(root, text="Conversion Target:")
conversion_target_label.grid(column=0, row=3)
conversion_target_var = tk.StringVar(root)
conversion_target_menu = ttk.Combobox(root, textvariable=conversion_target_var)
conversion_target_menu.grid(column=1, row=3)
get_conversion_targets()

generate_target_button = tk.Button(root, text="Generate Target Rule", command=generate_target_rule)
generate_target_button.grid(column=2, row=3)

target_rule_label = tk.Label(root, text="Generated Target Rule:")
target_rule_label.grid(column=0, row=4)
target_rule_text = tk.Text(root, wrap=tk.WORD)
target_rule_text.grid(column=1, row=4)

def open_nano_cyber_solutions():
    webbrowser.open("https://nanocybersolutions.com")

footer = tk.Button(root, text="Nano Cyber Solutions", command=open_nano_cyber_solutions)
footer.grid(column=1, row=5)

# Run the GUI event loop
root.mainloop()
