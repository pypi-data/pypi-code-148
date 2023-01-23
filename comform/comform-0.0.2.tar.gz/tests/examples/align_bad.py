from unittest.mock import Mock

my_func = Mock()
arg1 = woah_another_arg = wow_its_really_unclear_what_each_arg_does = arg4 = Mock()

thing = my_func(
    arg1,  # this is a comment
    woah_another_arg,  # this arg is really important
    wow_its_really_unclear_what_each_arg_does,  # people should implement kwargs :/
    arg4,  # last but not least
)
