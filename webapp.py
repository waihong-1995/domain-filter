import gradio as gr
import tempfile
from processor import process_file

def process_excel(file_obj, column_name):
    if file_obj is None:
        return None

    # Handle Gradio file object properly
    input_path = file_obj.name

    # Create output file
    tmp_output = tempfile.NamedTemporaryFile(suffix="_processed.xlsx", delete=False)
    output_path = tmp_output.name
    tmp_output.close()

    try:
        process_file(input_path, output_path, column_name)
    except Exception as e:
        # Return a text file with error (so UI doesn't crash)
        error_file = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        with open(error_file.name, "w") as f:
            f.write(f"Error: {str(e)}")
        return error_file.name

    return output_path


with gr.Blocks() as demo:
    gr.Markdown("## NOC Domain Tool")
    gr.Markdown("Upload Excel with domains, extract Root Domain & Subdomain, and download processed Excel.")

    file_input = gr.File(label="Upload Excel File", file_types=[".xlsx", ".xls"])
    column_input = gr.Textbox(label="Column Name", value="Domain")
    output_file = gr.File(label="Download Processed File")

    submit_btn = gr.Button("Process")

    submit_btn.click(
        fn=process_excel,
        inputs=[file_input, column_input],
        outputs=output_file
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)