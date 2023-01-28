from negate import Negator

negator = Negator(fail_on_unsupported=True)

ns = negator.negate_sentence("A piece with no moving parts.")

print(ns)

