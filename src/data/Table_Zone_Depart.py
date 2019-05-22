from data.Palet_Zone_Depart import Palet_Zone_Depart


class Table_Zone_Depart:

    def __init__(self):
        self.zone_depart = [Palet_Zone_Depart("R", "red"), Palet_Zone_Depart("G", "red"), Palet_Zone_Depart("B", "green")]

    def to_json(self):
        return {"zone_depart": [Palet_Zone_Depart.to_json() for Palet_Zone_Depart in self.zone_depart],
                }
