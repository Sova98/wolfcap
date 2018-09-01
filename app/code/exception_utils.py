import traceback


def traceback_to_str(err) -> str:
    return 'ERROR:\n' + str(err) + '\n\nStack:\n' + traceback.format_exc(); #''.join(traceback.format_stack())
