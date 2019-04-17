def nothing():
    pass

def validInput(input_msg, error_msg, valid, preamble=nothing, cast=str, *error_args):
    while True:
        preamble()
        try:
            user_input = cast(input(input_msg))
            if valid(user_input):
                return user_input
        except ValueError:
            pass
        print(error_msg.format(*error_args))
