from database import DataBase
from bigdata import BigData
from datetime import datetime


class Events(DataBase):
    def __init__(self) -> None:
        super().__init__("metric.db")

    def createTable(self):
        cursor = self.getCursor()
        sql_create_avg_events_table = """CREATE TABLE IF NOT EXISTS avgEvents (
                                    event_id INTEGER PRIMARY KEY NOT NULL,
                                    hour INTEGER,
                                    FOREIGN KEY (event_id) REFERENCES events (event_id),
                                    UNIQUE(event_id)
                                )
        """
        self.execute(cursor, sql_create_avg_events_table)
        print(sql_create_avg_events_table)

    def insertTable(self, shift, device=None, locale=None):
        bd = BigData()
        bd.open()
        res = bd.execute(bd.getCursor(), """SELECT event_name,
                                                    clicked_date,
                                                    event_id
                                            FROM events
                                            INNER JOIN persons
                                            ON persons.person_id = events.person_id
                            """)
        events = bd.fetchAll(res)
        bd.close()
        res = []
        for event in events:
            time = datetime.fromisoformat(event[1].replace('Z', shift))
            time += time.utcoffset()
            res.append((event[2], time.hour))
        SQL = "INSERT INTO avgEvents (event_id, hour) VALUES (?, ?)"
        self.executeMany(self.getCursor(), SQL, res)
        self.commit()
        print("Inserted into eventsAvg")


if __name__ == "__main__":
    e = Events()
    e.open()
    # e.drop("avgEvents")
    e.createTable()
    e.insertTable(shift="-08:00")
    e.close()
