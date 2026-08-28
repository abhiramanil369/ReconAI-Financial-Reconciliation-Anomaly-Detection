def create_ground_truth(
        case_id,
        fault_type
):
        """
            Create the hidden expected label for a benchmark case
        """

        if fault_type == "clean":
                return {
                        "case_id" : case_id,
                        "label" : "MATCH",
                        "is_clean" : True,
                        "fault_type" : None
                }
        return{
                        "case_id" : case_id,
                        "label" : fault_type.upper(),
                        "is_clean" : False,
                        "fault_type" : fault_type               
        }
