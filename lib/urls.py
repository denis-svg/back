from database import DataBase
from bigdata import BigData
from datetime import datetime
import filters as flt
from statistics import median, mean


class Urls(DataBase):
    def __init__(self) -> None:
        super().__init__('metric.db')

    def createTable(self):
        cursor = self.getCursor()
        sql_create_urls_table = """CREATE TABLE IF NOT EXISTS urls_metric (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    url TEXT,
                                    unique_clicks INTEGER,
                                    total_clicks INTEGER,
                                    timeOnPage INTEGER,
                                    timeOnPage_filtered INTEGER,
                                    pageBeforeConversion INTEGER,
                                    pageBeforeShare INTEGER,
                                    ratio_clicks REAL GENERATED ALWAYS AS (CAST(unique_clicks AS REAL) / CAST(total_clicks AS REAL)) STORED,
                                    ratio_time REAL GENERATED ALWAYS AS (CAST(timeOnPage_filtered AS REAL) / CAST(timeOnPage AS REAL)) STORED,
                                    device TEXT,
                                    locale TEXT,
                                    UNIQUE(id)
                                )
        """
        self.execute(cursor, sql_create_urls_table)
        print(sql_create_urls_table)

    def insertUrls(self, device=None, locale=None):
        bd = BigData()
        bd.open()

        if not device and not locale:
            res = bd.execute(bd.getCursor(), f"""SELECT  events.person_id,
                                                        events.url,
                                                        events.clicked_date,
                                                        events.event_name
                                                FROM events
                                                ORDER BY events.clicked_date ASC""")
        elif device and locale:
            res = bd.execute(bd.getCursor(), f"""SELECT  events.person_id,
                                                        events.url,
                                                        events.clicked_date,
                                                        events.event_name
                                                FROM events
                                                INNER JOIN persons
                                                ON persons.person_id = events.person_id
                                                WHERE persons.device = '{device}' and persons.locale = '{locale}'
                                                ORDER BY events.clicked_date ASC""")
        elif device:
            res = bd.execute(bd.getCursor(), f"""SELECT  events.person_id,
                                                        events.url,
                                                        events.clicked_date,
                                                        events.event_name
                                                FROM events
                                                INNER JOIN persons
                                                ON persons.person_id = events.person_id
                                                WHERE persons.device = '{device}'
                                                ORDER BY events.clicked_date ASC""")
        elif locale:
            res = bd.execute(bd.getCursor(), f"""SELECT  events.person_id,
                                                        events.url,
                                                        events.clicked_date,
                                                        events.event_name
                                                FROM events
                                                INNER JOIN persons
                                                ON persons.person_id = events.person_id
                                                WHERE persons.locale = '{locale}'
                                                ORDER BY events.clicked_date ASC""")
        
        events = bd.fetchAll(res)
        person_id_dict = {}
        for event in events:
            person_id = event[0]
            url = event[1]
            time = event[2]
            name = event[3]
            if person_id not in person_id_dict:
                person_id_dict[person_id] = [[url, time, name]]
            else:
                person_id_dict[person_id].append([url, time, name])

        urls_list = self.merge(person_id_dict, locale, device)
        SQL = "INSERT INTO urls_metric (url, total_clicks, unique_clicks, pageBeforeConversion, pageBeforeShare, timeOnPage, timeOnPage_filtered, locale, device) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.executeMany(self.getCursor(), SQL, urls_list)
        self.commit()
        bd.close()

    def insertAllTypes(self):
        bd = BigData()
        bd.open()
        res = bd.execute(bd.getCursor(), """SELECT DISTINCT locale
                                                        FROM persons""")
        locales = bd.fetchAll(res)
        res = bd.execute(bd.getCursor(), """SELECT DISTINCT device
                                                        FROM persons""")
        devices = bd.fetchAll(res)
        bd.close()
        self.insertUrls(device=None, locale=None)
        for device in devices:
            self.insertUrls(device=device[0], locale=None)
            for locale in locales:
                self.insertUrls(device=device[0], locale=locale[0])
                self.insertUrls(device=None, locale=locale[0])
                print(device[0], locale[0])

    def merge(self, person_id_dict, locale, device):
        total_clicks = self.__totalClicks(person_id_dict)
        unique_clicks = self.__uniqueClicks(person_id_dict)
        pbc = self.__pageBefore(person_id_dict, 'conversion')
        pbs = self.__pageBefore(person_id_dict, 'share_experience')
        top = self.__top(person_id_dict)
        top_filtered = self.__top(person_id_dict, filter=True)
        
        out = []
        for url in total_clicks.keys():
            url_total_clicks = total_clicks[url]
            url_unique_clicks = unique_clicks[url]
            url_pbc = None
            url_pbs = None
            url_top = None
            url_top_filtered = None

            if url in pbc:
                url_pbc = pbc[url]
            if url in pbs:
                url_pbs = pbs[url]
            if url in top:
                url_top = top[url]
            if url in top_filtered:
                url_top_filtered = top_filtered[url]

            out.append([url, url_total_clicks, url_unique_clicks, url_pbc, url_pbs, url_top, url_top_filtered, locale, device])

        return out

    def __totalClicks(self, person_id_dict):
        urls = {}
        for person_id in person_id_dict.keys():
            for event in person_id_dict[person_id]:
                url = event[0]
                if url not in urls:
                    urls[url] = 1
                else:
                    urls[url] += 1

        return urls

    def __uniqueClicks(self, person_id_dict):
        urls = {}
        for person_id in person_id_dict.keys():
            already_accesed = {}
            for event in person_id_dict[person_id]:
                url = event[0]
                if url not in already_accesed:
                    if url not in urls:
                        urls[url] = 1
                    else:
                        urls[url] += 1
                already_accesed[url] = True

        return urls

    def __pageBefore(self, person_id_dict, event_name):
        urls = {}
        for person_id in person_id_dict.keys():
            previous_url = None
            for event in person_id_dict[person_id]:
                url = event[0]
                name = event[2]
                if name == event_name and previous_url is not None:
                    if previous_url not in urls:
                        urls[previous_url] = 1
                    else:
                        urls[previous_url] += 1
                previous_url = url

        return urls

    def __top(self, person_id_dict, filter=False):
        urls = {}
        for person_id in person_id_dict.keys():
            previous = None
            for event in person_id_dict[person_id]:
                time = datetime.fromisoformat(event[1].replace('Z', '+00:00'))
                if previous is not None:
                    p_url = previous[0]
                    p_time = datetime.fromisoformat(previous[1].replace('Z', '+00:00'))
                    if p_url not in urls:
                        urls[p_url] = [ (time - p_time).total_seconds() ]
                    else:
                        urls[p_url].append ( (time - p_time).total_seconds() )
                previous = event

        for url in urls.keys():
            # filter
            if filter:
                urls[url] = flt.filter2(urls[url])
            urls[url] = round(mean(urls[url]))
        return urls

if __name__ == "__main__":
    u = Urls()
    u.open()
    u.createTable()
    #u.insertUrls(device='Other', locale='cei')
    #.insertUrls(device='Other', locale='en-US')
    u.insertAllTypes()
    u.close()