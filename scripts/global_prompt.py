import modules.scripts as scripts
import gradio as gr
import re
import random

from modules.processing import StableDiffusionProcessing


class ExtensionTemplateScript(scripts.Script):

    def title(self):
        return "Global Prompts"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion('Global Prompts', open=False):
            with gr.Row():
                enabled = gr.Checkbox(False, label="Enable")

            with gr.Row():
                prePositive = gr.Textbox(
                    info="Inserted before the main prompt",
                    label="Positive Prefix",
                    lines=3,
                    value=""
                )
                postPositive = gr.Textbox(
                    info="Inserted after the main prompt",
                    label="Positive Postfix",
                    lines=3,
                    value=""
                )

            with gr.Row():
                preNegative = gr.Textbox(
                    info="Inserted before the main negative prompt",
                    label="Negative Prefix",
                    lines=3,
                    value=""
                )
                postNegative = gr.Textbox(
                    info="Inserted after the negative prompt",
                    label="Negative Postfix",
                    lines=3,
                    value=""
                )

            with gr.Row():
                replaceRandomValues = gr.Checkbox(
                    False, label="Replace @x with random value between 0 and x")

        return [enabled, prePositive, postPositive, preNegative, postNegative, replaceRandomValues]

    def process(self, p: StableDiffusionProcessing, enabled, prePositive, postPositive, preNegative, postNegative, replaceRandomValues):

        if not enabled:
            return

        prompt = p.prompt
        negative_prompt = p.negative_prompt

        if prePositive:
            prompt = prePositive + ", " + prompt
        if postPositive:
            prompt = prompt + ", " + postPositive

        if preNegative:
            negative_prompt = preNegative + ", " + negative_prompt
        if postNegative:
            negative_prompt = negative_prompt + ", " + postNegative

        p.all_prompts[0] = prompt
        p.all_negative_prompts[0] = negative_prompt

        if replaceRandomValues:
            # Replaces @x with a random value between 0 and x
            # e.g. @2 will be replaced with a random value between 0 and 2
            def replace_random(match):
                # Create a random float between 0 and the matched number
                random_value = random.uniform(0, int(match.group(1)))
                # Return the random value formatted to 2 decimal places
                return f"{random_value:.2f}"

            for i in range(len(p.all_prompts)):
                p.all_prompts[i] = re.sub(
                    r'@(\d+)', replace_random, p.all_prompts[i])
        else:
            # Replaces @x with x
            # e.g. @2 will be replaced with 2
            for i in range(len(p.all_prompts)):
                p.all_prompts[i] = re.sub(r'@(\d+)', r'\1', p.all_prompts[i])
