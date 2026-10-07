import pandas as pd


def profile_data(file_path):

    df = pd.read_csv(file_path)

    profile = {}

    # Basic information
    profile["rows"] = len(df)
    profile["columns"] = list(df.columns)

    # Missing values
    missing = df.isnull().sum()
    profile["missing_values"] = {
        column: int(value)
        for column, value in missing.items()
        if value > 0
    }

    # Duplicate rows
    profile["duplicate_rows"] = int(df.duplicated().sum())

    # Data types
    profile["data_types"] = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    # Possible date columns
    date_columns = []

    for column in df.columns:
        if "date" in column.lower():
            date_columns.append(column)

    profile["date_columns"] = date_columns

    # Possible currency columns
    currency_columns = []

    for column in df.columns:
        if "currency" in column.lower():
            currency_columns.append(column)

    profile["currency_columns"] = currency_columns

    return profile


if __name__ == "__main__":

    result = profile_data("data/sales.csv")

    print("\n===== DATA PROFILE =====")

    print("\nRows:")
    print(result["rows"])

    print("\nColumns:")
    print(result["columns"])

    print("\nMissing Values:")
    print(result["missing_values"])

    print("\nDuplicate Rows:")
    print(result["duplicate_rows"])

    print("\nData Types:")
    print(result["data_types"])

    print("\nDate Columns:")
    print(result["date_columns"])

    print("\nCurrency Columns:")
    print(result["currency_columns"])