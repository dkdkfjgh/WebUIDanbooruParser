import re

from modules import script_callbacks, shared

import gradio as gr

import re

import re

def parse_tags(tags: str) -> str:
    """
    This function takes an unrefined string of tags from either sankakucomplex or danbooru,
    and returns a refined string of tags without any extra characters or information.

    For sankakucomplex, the tags are separated by "(?)" and any "original" tag in the input is ignored.
    For danbooru, the tags are separated by "?" and only certain tabs (Artist, Copyright, Characters,
    General, Meta) are considered. Any "original" tag in the Copyright tab is ignored.

    Parameters:
    tags (str): The unrefined string of tags from either sankakucomplex or danbooru.

    Returns:
    A refined string of tags without any extra characters or information.
    """

    # Check if the input is from sankakucomplex
    if "(?)" in tags:
        # Remove the "(?)" characters and split the string into a list of tags
        tag_list = [tag.replace("(?)", "").strip() for tag in tags.splitlines()]

        # Remove any "original" tags from the list
        tag_list = [tag for tag in tag_list if tag != "original"]

        # Remove any count information from the tags
        tag_list = [re.sub(r"\s*\d+(\.\d+)?[KM]?(\s|$)", " ", tag).strip() for tag in tag_list]

    # Check if the input is from danbooru
    elif "?" in tags:
        # Split the string into a list of lines
        lines = tags.splitlines()

        # Define a set of tabs that we're interested in
        tabs = {"Artist", "Copyright", "Characters", "General", "Meta"}

        # Initialize an empty list to store the tags
        tag_list = []

        # Loop through each line in the input
        for line in lines:
            # Check if the line starts with "?"
            if line.startswith("?"):
                # Split the line into the tag and its count
                tag = line.split()[1]
                tag_list.append(line.split()[1])
                # Check if the tag's tab is in the set of tabs we're interested in
                if tag.split(":")[0] in tabs:
                    # Check if the tag is "original" and in the "Copyright" tab
                    if tag == "Copyright:original":
                        continue
                    # Otherwise, append the tag to the list
                    tag_list.append(line.split()[1])


    # If the input is not recognized, raise an exception
    else:
        raise ValueError("Unrecognized input format")

    # Return the refined tag list as a string
    output = ", ".join(tag_list)
    output = output.replace("(", "\(")
    output = output.replace(")", "\)")

    return output

def add_tab():
    css = ""
    with gr.Blocks(analytics_enabled=False, css=css) as ui:
        gr.HTML(f"""
            <style>{css}</style>
            <h2>
            Please Copy-Paste danbooru or sankakucomplex tags from left!
            </h2>
        """)

        with gr.Tabs() as tabs:
            with gr.Tab("Text input", id="input_text"):
                Tags= gr.Textbox(label="Prompt", elem_id="prompt", show_label=False, lines=8, placeholder="Put Danbooru tags here")
                go = gr.Button(value="Parse", variant="primary")
                Output = gr.HTML(elem_id="output_text")
                go.click(
                    fn=parse_tags,
                    inputs=[Tags],
                    outputs=[Output],
                )



    return [(ui, "Danbooru Parser", "Danbooru Parser")]

script_callbacks.on_ui_tabs(add_tab)
