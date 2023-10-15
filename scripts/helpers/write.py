def write_exists_in_kv_format(
        file_path: str,
        **key_value_pairs,
):
    formatted_string = "\n".join([f'{key}={value}' for key, value in key_value_pairs.items()])
    print(f'writing {formatted_string} to file {file_path}')
    with open(file_path, 'w') as f:
        f.write(formatted_string)
