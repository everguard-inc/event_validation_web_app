def get_percentage_values(totals: dict):
    totals['fp_percent_internal'] = totals['fp_count_internal'] / totals['total'] * 100 if totals['total'] else 0
    totals['fn_percent_internal'] = totals['fn_count_internal'] / totals['total'] * 100 if totals['total'] else 0
    totals['tp_percent_internal'] = totals['tp_count_internal'] / totals['total'] * 100 if totals['total'] else 0
    totals['tn_percent_internal'] = totals['tn_count_internal'] / totals['total'] * 100 if totals['total'] else 0
    # Portal wise
    totals['fp_percent_portal'] = totals['fp_count_portal'] / totals['total'] * 100 if totals['total'] else 0
    totals['fn_percent_portal'] = totals['fn_count_portal'] / totals['total'] * 100 if totals['total'] else 0
    totals['tp_percent_portal'] = totals['tp_count_portal'] / totals['total'] * 100 if totals['total'] else 0
    totals['tn_percent_portal'] = totals['tn_count_portal'] / totals['total'] * 100 if totals['total'] else 0
    totals['not_validated_percent'] = totals['not_validated'] / totals['total'] * 100 if totals['total'] else 0
    return totals
