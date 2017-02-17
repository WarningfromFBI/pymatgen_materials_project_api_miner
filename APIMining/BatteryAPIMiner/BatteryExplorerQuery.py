
#queries for the battery explorer API on Materials Project
def get_battery_data(formula_or_batt_id):
    """Returns batteries from a batt id or formula
    Examples:
        get_battery("mp-300585433")
        get_battery("LiFePO4")
    """
    return mpr._make_request('/battery/%s' % formula_or_batt_id)