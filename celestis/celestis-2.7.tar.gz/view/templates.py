import os
import re

# |name| |surname|

def evaluate_expressions(template, context):
    matches = re.finditer(r"\|(.+?)\|", template)
    for match in matches:
        evaluation = eval(match.group(1), context)
        template = template.replace(match.group(), str(evaluation))

    return template

def evaluate_if_statements(template, context):
    matches = re.finditer(r"(\d+) \[if (.+)\]", template)
    for match in matches:
        identifier = match.group(1)
        condition = match.group(2)

        evaluation = eval(condition, context)
        if not evaluation:
            start_pos = match.end() + 1
            end_pos = template.index(f"{identifier} [terminate]")
            template = template[:start_pos] + template[end_pos:]
        
    return template

def evaluate_for_loops(template, context):
    matches = re.finditer(r"(\d+) \[for (.+)\]", template)
    # 1 [for index,item in users]
    for match in matches:
        identifier = match.group(1)
        expression_chunks = match.group(2).split(" in ")
        iterator, value = expression_chunks[0].split(",")
        # iterator = idx, value=item
        array = eval(expression_chunks[1], context)

        loop_section = template[match.end() + 1:template.index(f"{match.group(1)} [terminate]")]
        loop_output = ""
        
        for idx, item in enumerate(array):
            new_context = {
                f"{iterator}": idx,
                f"{value}": item
            }

            print(new_context)

            loop_output += evaluate_expressions(loop_section, new_context)
        
        template = template.replace(loop_section, loop_output)

    return template

def evaluate_external_templates(request, template, context):
    matches = re.finditer(r"(\d+) \[include template\]", template)
    for match in matches:
        identifier = match.group(1)
        start_pos = match.end() + 1
        end_pos = template.index(f"{identifier} [terminate]")
        external_template_path = template[start_pos:end_pos].strip()
        external_template = render_template(request, external_template_path, context)

        template = template.replace(external_template_path, external_template)

    return template

def evaluate_css_files(request, template, context):
    css_matches = re.finditer(r"(\d+) \[include (.+)\]", template)
    for match in css_matches:
        identifier = match.group(1)

        start_pos = match.end() + 1
        end_pos = template.index(f"{identifier} [terminate]")
        css_file_path = template[start_pos:end_pos].strip()
        abs_file_path = request["project"] + "/css/" + css_file_path

        file_type = match.group(2)

        if file_type == "css":
            css_code = ""

            if os.path.exists(abs_file_path):
                with open(abs_file_path, "r") as f:
                    css_code = f.read()
            
                styles = f'''
                    <style>
                        {css_code}
                    </style>
                '''

                template = template.replace(css_file_path, styles)
    
    return template

def decode_template(request, template, context):
    # Evaluating for loops
    template = evaluate_for_loops(template, context)

    # Evaluating expressions
    template = evaluate_expressions(template, context)

    # Evaluating if statements
    template = evaluate_if_statements(template, context)

    # Linking other templates
    template = evaluate_external_templates(request, template, context)

    # Linking css files
    template = evaluate_css_files(request, template, context)

    # Clean up
    template = re.sub(r"\d+ \[.+\]", "", template)

    return template

def render_template(request, relative_file_path, context={}):
    template = ""
    abs_file_path = request["project"] + "/templates/" + relative_file_path

    if not os.path.exists(abs_file_path):
        template = "<h1>File not found</h1>"
    
    else:
        with open(abs_file_path, "r") as f:
            template = f.read()
        
    template = decode_template(request, template, context)
    return template