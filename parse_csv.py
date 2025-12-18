import pandas as pd

def load_csv(path):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    return df

if __name__ == "__main__":
    df = load_csv("sample.csv")
    print(df)
