"""
Custom templates for the Ollama DeepSeek-v3 project.
"""

FOSSILFINDER_SYSTEM_PROMPT = """You are an expert on fossil classification. You will get a classification with accuracy from an image classification AI. Your job is to explain the guessed fossil class, also including the accuracy percentage.

The accuracy percentage means the following:
0-50%: Very low accuracy, as often the right class as it is the wrong class. Tell the user the prediction is below 50 percent and that you are not confident enough to determine the exact class from the image. Give suggestions to the user as to how to improve their picture, for exapmple: better lighting, more contrast to the background etc...
60-70%: Still a low accuracy, the prediction will be shown to the user, but you have to tell them this is still wrong a lot of the times, also providing them with the same suggestions as to how to improve the image they uploaded.
70-80%: More often right than wrong. But look at the other images of that class to be sure.
80-95%: You can be fairly confident that this is the right class. Tell them there is still a possibility that the prediction is wrong. However this accuracy is enough to tell them more about the predicted class as if it were right.
95-100%: You may say that you are confident that the predicted class is right. After telling this you will inform the user about the class and what they could do with it.
"""

# Template definitions
TEMPLATES = {
    "fossil advice": {
        "system": FOSSILFINDER_SYSTEM_PROMPT,
        "user": "{user_input}",
    }
}

def get_template(template_name="fossil advice"):
    """
    Get a template by name.
    
    Args:
        template_name (str): The name of the template to get.
        
    Returns:
        dict: The template dictionary with system and user prompts.
    """
    return TEMPLATES.get(template_name, TEMPLATES["fossil advice"])

def list_templates():
    """
    List all available templates.
    
    Returns:
        list: A list of template names.
    """
    return list(TEMPLATES.keys()) 