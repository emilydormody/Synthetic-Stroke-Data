from mesa import Agent, Model


class CTScan(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = unique_id
        self.model = model
        self.treatment_time = 30
        self.current_patient = None

    def step(self):
        if self.current_patient is None and len(self.model.ct_patients) != 0:
            patient = self.model.ct_patients.pop(0)
            patient.ct_time = self.model.current_time
            patient.last_treatment = self.model.current_time
        elif self.current_patient.ct_time < self.model.current_time - 30:
                self.current_patient = None