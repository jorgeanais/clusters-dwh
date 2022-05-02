import glob
import pandas as pd
import sqlalchemy as sa

from src.settings import Config


class Uploader:
    def __init__(self):
        self.engine: sa.engine.Engine = sa.create_engine(Config.CONN_STRING)
        self.schema = Config.TARGET_SCHEMA
        self.csv_files = glob.glob(Config.DATAPATH + "*.csv")

    def csv_files_to_df(self):
        """Convert csv files to a single dataframe"""
        dfs = []
        for f in self.csv_files:
            df = pd.read_csv(f)
            df = df.drop(columns=["Unnamed: 0"], axis=1, errors="ignore")
            df.columns = df.columns.str.lower()
            dfs.append(df)

        return pd.concat(dfs)

    def get_clusters_names(self, df: pd.DataFrame):
        """Get cluster names from dataframe"""
        return pd.DataFrame(data=df.cluster.unique(), columns=["cluster"])

    def upsert(self, df: pd.DataFrame, target_table: str):
        """Upsert star table from pandas dataframe"""

        staging_table = f"{target_table}_staging"

        # Create staging table
        df.to_sql(
            staging_table,
            self.engine,
            schema=self.schema,
            index=False,
            chunksize=1000,
            if_exists="replace",
        )

        upsert_star = f"""
        INSERT INTO {self.schema}.{target_table}
        (ra, dec, pmra, epmra, pmdec, epmdec, mz, ez, my, ey, mj, ej, mh, eh, mk, ek, probability, cluster, plx, eplx)
        SELECT ST.ra,
               ST.dec,
               ST.pmra, 
               ST.epmra, 
               ST.pmdec, 
               ST.epmdec,
               ST.mz,
               ST.ez,
               ST.my,
               ST.ey,
               ST.mj,
               ST.ej,
               ST.mh,
               ST.eh,
               ST.mk,
               ST.ek,
               ST.probability,
               ST.cluster,
               ST.plx,
               ST.eplx
        FROM {self.schema}.{staging_table} ST
            LEFT JOIN {self.schema}.{target_table} T ON ST.ra = T.ra AND ST.dec = T.dec
        WHERE T.ra IS NULL;
        """

        upsert_cluster = f"""
        INSERT INTO {self.schema}.{target_table}
        (cluster)
        SELECT ST.*
        FROM {self.schema}.{staging_table} ST
            LEFT JOIN {self.schema}.{target_table} T ON ST.cluster = T.cluster
        WHERE T.cluster IS NULL;
        """

        match target_table:
            case "star":
                upsert_query = upsert_star
            case "cluster":
                upsert_query = upsert_cluster
            case _:
                raise ValueError(f"Unknown target table: {target_table}")

        # Do upsert
        self.engine.execute(upsert_query)

        # Clean up staging table
        self.engine.execute(f"DROP TABLE {self.schema}.{staging_table}")
        
    def run(self):
        """Run uploader"""
        stars = self.csv_files_to_df()
        clusters = self.get_clusters_names(stars)
        self.upsert(clusters, "cluster")
        self.upsert(stars, "star")
