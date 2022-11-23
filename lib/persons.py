from database import DataBase
from bigdata import BigData
from datetime import datetime



class Persons(DataBase):
    def __init__(self) -> None:
        super().__init__('metric.db')

    def createTable(self):
        cursor = self.getCursor()
        sql_create_persons_table = """CREATE TABLE IF NOT EXISTS persons_metric (
                                    person_id INTEGER PRIMARY KEY,
                                    clicksToConvert INTEGER,
                                    clicksToShare INTEGER,
                                    timeToConvert INTEGER,
                                    timeToShare INTEGER,
                                    FOREIGN KEY (person_id) REFERENCES persons (person_id),
                                    UNIQUE(person_id)
                                )
        """
        self.execute(cursor, sql_create_persons_table)
        print(sql_create_persons_table)

    def insertPersons(self):
        bd = BigData()
        bd.open()
        bd_cursor = bd.getCursor()
        res = bd.execute(bd_cursor, """SELECT persons.person_id,
                                                events.clicked_date,
                                                persons.master_id,
                                                persons.device,
                                                persons.locale,
                                                events.event_name
                                        from events
                                        INNER JOIN persons
                                        ON persons.person_id = events.person_id
                                        ORDER BY events.clicked_date ASC""")
        
        # Creating person_id_dict in order to group the query by person_id
        events = bd.fetchAll(res)
        person_id_dict = {}
        for event in events:
            person_id = event[0]
            master_id = event[2]
            time = event[1]
            device = event[3]
            locale = event[4]
            event_name = event[5]

            if person_id not in person_id_dict:
                person_id_dict[person_id] = [[master_id, time, device, locale, event_name]]
            else:
                person_id_dict[person_id].append([master_id, time, device, locale, event_name])

        # Computing all the metrics
        persons_list = []
        for person_id in person_id_dict.keys():
            events = person_id_dict[person_id]
            master_id = events[0][0]
            device = events[0][2]
            locale = events[0][3]

            ctc = None
            ttc = None
            counter = 0
            start = datetime.fromisoformat(events[0][1].replace('Z', '+00:00'))
            for event in events:
                counter += 1
                if event[4] == 'conversion':
                    ctc = counter
                    ttc = round((datetime.fromisoformat(event[1].replace('Z', '+00:00')) - start).total_seconds())
                    break

            cts = None
            tts = None
            counter = 0
            start = datetime.fromisoformat(events[0][1].replace('Z', '+00:00'))
            for event in events:
                counter += 1
                if event[4] == 'share_experience':
                    cts = counter
                    tts = round((datetime.fromisoformat(event[1].replace('Z', '+00:00')) - start).total_seconds())
                    break
            
            persons_list.append([person_id, ctc, ttc, cts, tts])

        SQL = "INSERT INTO persons_metric (person_id, clicksToConvert, timeToConvert, clicksToShare, timeToShare) VALUES (?, ?, ?, ?, ?)"
        self.executeMany(self.getCursor(), SQL, persons_list)
        self.commit()
        print("inserted persons into ", self.path)
        bd.close()

if __name__ == "__main__":
    p = Persons()
    p.open()
    p.createTable()
    p.insertPersons()
    p.close()

