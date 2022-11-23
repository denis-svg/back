from database import DataBase
from req import Json

class BigData(DataBase):
    def __init__(self) -> None:
        super().__init__("metric.db")

    def createTables(self):
        cursor = self.getCursor()
        # persons
        sql_create_persons = """
                                    CREATE TABLE IF NOT EXISTS persons (
                                        person_id INTEGER PRIMARY KEY,
                                        master_id INTEGER,
                                        locale TEXT,
                                        device TEXT,
                                        UNIQUE(person_id)
                                    )
        """
        print(sql_create_persons)
        self.execute(cursor, sql_create_persons)

        # events
        sql_create_events = """
                                    CREATE TABLE IF NOT EXISTS events (
                                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        person_id INTEGER,
                                        event_name TEXT,
                                        clicked_date TIMESTAMP,
                                        urL TEXT,
                                        FOREIGN KEY (person_id) REFERENCES persons (person_id),
                                        UNIQUE(event_id)
                                    )
        """
        print(sql_create_events)
        self.execute(cursor, sql_create_events)

    def insertTables(self, path):
        data = Json.load_json(path)
        cursor = self.getCursor()

        # Insert into persons
        self.__insertPersons(cursor, data)
        # Insert into events
        self.__insertEvents(cursor, data)
    
    def __insertPersons(self, cursor, data):
        person_dict = {}
        person_list = []
        for entry in data:
            person = entry['device_profile_id']
            if person not in person_dict:
                person_dict[person] = True

                locale = entry['locale']
                device = entry['device_type']
                master = entry['master_person_id']

                if master:
                    person_list.append([person, master, locale, device])
                else:
                    person_list.append([person, None, locale, device])

        SQL = "INSERT INTO persons (person_id, master_id, locale, device) VALUES (?, ?, ?, ?)"
        self.executeMany(cursor, SQL , person_list)
        self.commit()
        print("Inserted into persons")

    def __insertEvents(self, cursor, data):
        event_list = []
        for entry in data:
            person_id = entry['device_profile_id']
            event_name = entry['event_name']
            time = entry['event_time']
            url = entry['url'].split('?')[0]
            event_list.append([person_id, event_name, url, time])

        SQL = "INSERT INTO events (person_id, event_name, url, clicked_date) VALUES (?, ?, ?, ?)"
        self.executeMany(cursor, SQL , event_list)
        self.commit()
        print("inserted into events")




if __name__ == "__main__":
    bd = BigData()
    bd.open()
    bd.createTables()
    bd.insertTables('Input_Records-rk946c2nlklj4dcwnhqm.json')
    bd.close()


        


