# SigmaGPT

The ChatGPT Sigma Conversion script is a Python script that allows you to generate Sigma rules using the OpenAI GPT-3.5 language model and convert them to different target formats using the sigmac tool.

Prerequisites
Before using the ChatGPT Sigma Conversion script, you will need to have the following software installed on your system:

Python 3
requests
openai
cryptography
pycryptodome
PyYAML
pySigma
openai==0.27.0
keyring==23.2.1
sigmatools==0.20.0
gitpython

In addition, you will need to have an API key for the OpenAI GPT-3.5 language model. You can sign up for an API key on the OpenAI website.

Installation

To install the ChatGPT Sigma Conversion script, follow these steps:

Clone or Copy/Paste chatgpt_sigma_conversion.py

Install the Python dependencies:

Usage
To use the ChatGPT Sigma Conversion script, follow these steps:

Save your OpenAI API key using the save_api_key() function in the script.

Enter a prompt for the GPT-3.5 language model using the user_prompt_entry field in the GUI.

Click the "Generate Sigma Rule" button to generate a Sigma rule based on your prompt.

Select a target format from the drop-down menu using the conversion_target_menu field in the GUI.

Click the "Generate Target Rule" button to convert the generated Sigma rule to the selected target format.

The converted rule will be displayed in the target_rule_text field in the GUI.

# Problems:

# THERE ARE MANY!
Here's a few:
1. When you generate the script it takes time. Didn't have the time to create nice graphics so just wait for it.
2. ChatGPT generates a lot of metadat. Before converting to your favorite SIEM/XDR/WHATEVERDR you will have to remove the metadata first. Remove the following: 
* everything after assistant
* '''yml
* '''
* All the ChatGPT explenation at the buttom. Keep the Sigma Rule clean

This is how a normal Sigma Rule should look like:
```
title: Detect Rundll32 Execution
description: Detects the execution of the rundll32 command
references:
    - https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/rundll32
tags:
    - attack.execution
    - attack.t1085
    - attack.t1035
    - attack.t1059
logsource:
    product: windows
    service: security
detection:
    selection1:
        Image:
            - '*\rundll32.exe'
    selection2:
        CommandLine:
            - '* rundll32.exe *'
    condition: selection1 and selection2
falsepositives:
    - Legitimate use of rundll32
level: high
```
# Anything else ChatGPT is generating should be removed.
3. This is a pre-alpha release. It was meant for research purposeses only! 
4. Please don't hesitate to report problems/requests/ideas/improvments

License
The ChatGPT Sigma Conversion script is licensed under the GNU GPL V3 License. See LICENSE for more information.

Acknowledgements
The ChatGPT Sigma Conversion script was created by Nano Cyber Solutions and is based on the Sigma Rule Creator project by SigmaHQ. The GPT-3.5 language model is developed by OpenAI.




