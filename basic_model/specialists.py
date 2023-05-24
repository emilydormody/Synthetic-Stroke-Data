from mesa import Agent


class CTScan(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = unique_id
        self.model = model
        self.treatment_time = 30
        self.current_patient = None

    def step(self):
        if self.current_patient is None:
            if len(self.model.ct_patients) != 0:
                self.current_patient = self.model.ct_patients.pop(0)
                self.current_patient.ct_time = self.model.current_time
                self.current_patient.last_treatment = self.model.current_time
                print(self.current_patient.unique_id, ' ct start ', self.model.current_time, ' with ', self.name)
        elif self.current_patient.ct_time < self.model.current_time - 30:
            print(self.current_patient.unique_id, ' ct end ', self.model.current_time, ' with ', self.name)
            self.current_patient = None

