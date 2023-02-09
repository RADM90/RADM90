import pymysql

USER = 'USER_ID'
PASSWORD = 'USER_PASSWORD'
HOST_NAME = 'DBMS_URL'
PORT = 3306  # Default Port
DB = 'DB_'
CHARSET = 'utf8'


def connect_database():
    try:
        Connection = pymysql.connect(user=USER, password=PASSWORD, host=HOST_NAME, port=PORT, database=DB,
                                     charset=CHARSET)
        Connection.autocommit = False
        return Connection
    except pymysql.Error as e:
        print(f"Error Connecting to Database: {e}")
        Connection = pymysql.connect(user=USER, password=PASSWORD, host=HOST_NAME, port=PORT, charset=CHARSET)
        create_database(Connection, DB, CHARSET)
        # cursor = Connection.c
        # create_tables()
        return Connection


def create_database(Connection, db_name, char_set):
    sql = f"CREATE SCHEMA IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET {char_set} ;"
    cursor = Connection.cursor()
    cursor.execute(sql)
    Connection.commit()


def create_tables(Connection, cursor, db_name, table_name):
    sql = f"""CREATE TABLE IF NOT EXISTS `{db_name}`.`{table_name}` (
                              `IMG_INFO_IDX` INT NOT NULL,
                              `IDX` INT NOT NULL AUTO_INCREMENT,
                              `SHOT_DATE` DATE NULL,
                              `SHOT_TIME` TIME NULL,
                              `CONTOURED_IMAGE_PATH` VARCHAR(255) NULL,
                              `CLUSTER_CENTROID_PIXEL` VARCHAR(255) NULL,
                              `CLUSTER_CENTROID_GEO` VARCHAR(255) NULL,
                              `CLUSTER_CENTROID_GEO_LATITUTDE` DECIMAL NULL,
                              `CLUSTER_CENTROID_GEO_LONGITUDE` DECIMAL NULL,
                              `CLUSTER_WIDTH` DECIMAL NULL,
                              `CLUSTER_LENGTH` DECIMAL NULL,
                              `CONTOUR_BOUNDARY_PIXELS` LONGTEXT NULL,
                              `CONTOUR_BOUNDARY_GEO` LONGTEXT NULL,
                              `SARGASSUM_DENSITY` DECIMAL NULL,
                              `SARGASSUM_PREDICTION_GEO` VARCHAR(255) NULL DEFAULT 'Not Predicted',
                              PRIMARY KEY (`IDX`),
                              CONSTRAINT `fk_sarg_info_img_info`
                                FOREIGN KEY (`IMG_INFO_IDX`)
                                REFERENCES `SARGASSUM_DETECTION`.`IMG_INFO` (`IDX`)
                                ON DELETE NO ACTION
                                ON UPDATE NO ACTION);"""
    cursor.execute(sql)
    Connection.commit()


def dictcursor():
    return pymysql.cursors.DictCursor
