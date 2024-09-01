import jpegio

def extract_quantization_tables(file_path):
    # Read the JPEG file
    jpeg = jpegio.read(file_path)
    
    # Iterate over the quantization tables and print them
    for i, qtable in enumerate(jpeg.quant_tables):
        print(f'Quantization Table {i}:')
        print(qtable)

# Path to your JPEG file
file_path = 'jpeg444.jpg'
extract_quantization_tables(file_path)