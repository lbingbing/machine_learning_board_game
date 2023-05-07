from ..model import swapped_q_table_model

class GMCCTableModel(swapped_q_table_model.SwappedQTableModel):
    def get_model_algorithm(self):
        return 'gmcc'
