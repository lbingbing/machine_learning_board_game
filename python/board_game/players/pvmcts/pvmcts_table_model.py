from ..model import swapped_pv_table_model

class PVMctsTableModel(swapped_pv_table_model.SwappedPVTableModel):
    def get_model_algorithm(self):
        return 'pvmcts'
