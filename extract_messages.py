import polars as pl

df = pl.read_json("results.json")

df = (
    df.with_columns(
        pl.col("commit").struct.field("committer", "message"),
        pl.col("repository").struct.field("full_name").alias("repo_name"),
    )
    .with_columns(
        pl.col("committer").struct.field("date").str.to_datetime().alias("timestamp")
    )
    .select("timestamp", "repo_name", "message")
)

df.write_csv("commits.csv", quote_style="always")
df.write_parquet("commits.parquet")
