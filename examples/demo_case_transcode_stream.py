import io
import os

import Chamaeleo
from Chamaeleo.methods.flowed import YinYangCode
from Chamaeleo.utils.data_handle import save_model, load_model
from Chamaeleo.utils.pipelines import TranscodePipeline


def encode(model_path, input_stream, output_stream):
    coding_scheme = YinYangCode()
    pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=None, need_logs=True)
    pipeline.transcode(direction="t_c", input_stream=input_stream, output_stream=output_stream,
                       segment_length=120, index=True)
    save_model(path=model_path, model=coding_scheme, need_logs=True)
    print()
    pipeline.output_records(type="string")
    print()


def decode(model_path, input_stream, output_stream):
    coding_scheme = load_model(path=model_path, need_logs=True)
    pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=None, need_logs=True)
    pipeline.transcode(direction="t_s", input_stream=input_stream, output_stream=output_stream, index=True)
    print()
    pipeline.output_records(type="string")
    print()


if __name__ == "__main__":
    root_path = os.path.dirname(Chamaeleo.__file__)
    current_path = os.path.dirname(os.path.realpath(__file__))
    generated_file_path = os.path.join(current_path, "generated_files")

    read_file_path = os.path.join(root_path, "data", "pictures", "Mona Lisa.jpg")
    write_file_path = os.path.join(generated_file_path, "target.jpg")
    temp_model_path = os.path.join(generated_file_path, "model.pkl")
    dna_path = os.path.join(generated_file_path, "target.dna")

    original_stream = io.BytesIO(open(read_file_path, "rb").read())
    dna_stream = io.BytesIO()
    encode(model_path=temp_model_path, input_stream=original_stream, output_stream=dna_stream)
    dna_stream.seek(0)
    decoded_stream = io.BytesIO()
    decode(model_path=temp_model_path, input_stream=dna_stream, output_stream=decoded_stream)
