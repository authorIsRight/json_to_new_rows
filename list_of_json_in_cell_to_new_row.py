import json

import pandas as pd


def process_json_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Process a JSON column in the DataFrame by loading JSON data,
    exploding the DataFrame, and dropping the original JSON column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column_name (str): Name of the JSON column in the DataFrame.

    Returns:
        pd.DataFrame: Processed DataFrame after exploding the JSON column.
    """
    try:

        df[column_name] = df[column_name].apply(lambda x: json.loads(x)
                                                if isinstance(x, str) else [])
        df[column_name] = df[column_name].apply(lambda x: [x]
                                                if isinstance(x, dict) else x)
        df_exploded = df.explode(column_name)
        df_processed = pd.concat([df_exploded.drop([column_name], axis=1),
                                 df_exploded[column_name].apply(pd.Series)],
                                 axis=1)

    except Exception as e:
        print(f"Warning: Failed to process the JSON column. {e}")
        return df

    else:
        return df_processed


if __name__ == "__main__":
    """
    Main block to demonstrate the usage of the 'process_json_column' function.

    This block is executed when the script is run as a standalone program.
    It reads data from a CSV file ('example.csv'),
    processes a JSON column named 'Some JSON column'
    using the 'process_json_column' function,
    and saves the processed DataFrame to another CSV file ('output.csv').
    After running the script, the 'output.csv' file will contain
    the processed DataFrame with the JSON data exploded into new rows.

    Note:
        - The input CSV file ('example.csv') should be in the same directory
          as the script, or you should provide the full path to the file.
    """

    input_file = "example.csv"
    output_file = "output.csv"
    json_column_name = 'Some JSON column'

    df = pd.read_csv(input_file)

    processed_data_frame = process_json_column(df, json_column_name)
    processed_data_frame.to_csv(output_file, index=False)
