from project.src.utils.file import PropertyUtil
import pymysql


def test_test():
    path_to_config_file = "./config/db.properties"
    config_section = "CONFIG"

    entries = PropertyUtil().get_entries(path_to_config_file, config_section)
    config = {entrie[0]: entrie[1] for entrie in entries}
    print(entries)

    connection = None
    try:
        connection = pymysql.connect(host=config.get("host"), port=int(config.get("port")),
                                     user=config.get("user"), passwd=config.get("passwd"),
                                     database=config.get("database"), db=config.get("db"))
        cur = connection.cursor()
        cur.execute("SELECT * FROM salesman")
        for r in cur:
            print(r)
    except Exception as e:
        import logging
        logging.error("{}".format(e))
        print(e)
    finally:
        connection.close()
